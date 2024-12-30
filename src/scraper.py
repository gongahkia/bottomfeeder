# ----- REQUIRED IMPORTS -----

import helper as h
from datetime import date
from playwright.sync_api import sync_playwright

# ----- HELPER FUNCTIONS -----


def silly_generate_url_endpoint(
    end_year,
    base_domain="https://www.elitigation.sg/gdviewer/s/",
    start_year=2000,
    start_int=1,
    end_int=100,
    courts=["sgca", "sghc", "sghci", "sghcf", "sgcai"],
):
    """
    naively generates all permutations of url endpoints
    """
    current_year = date.today().year
    url_endpoint_array = []
    if end_year:
        if end_year > current_year:
            print(
                "Error: End year cannot be greater than current year. Setting end year to be current year."
            )
            end_year = current_year
        else:
            pass
    else:
        end_year = current_year
    for year in range(start_year, end_year + 1):
        for court in courts:
            for integer in range(start_int, end_int + 1):
                url_endpoint_array.append(f"{base_domain}{year}_{court}_{integer}")
    return url_endpoint_array


def smart_find_url_endpoint(
    number=100, target_url="https://www.elitigation.sg/gd/Home/Index"
):
    """
    scrapes the specified ELIT url for all existing urls
    until the desired number of URLs is found
    """
    url_array = []
    if number % 10 != 0:
        print("Error: Number of URLs must be a multiple of 10.")
        return None
    else:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(target_url)
                print(f"Success: Accessed page URL {target_url}")
                while len(url_array) != number:
                    page.wait_for_selector("div.row")
                    url_array += [
                        f"https://www.elitigation.sg{item.get_attribute('href')}"
                        for item in page.query_selector_all(
                            "div.card.col-12 div.gd-card-body a.h5.gd-heardertext"
                        )
                    ]
                    next_page = page.query_selector(
                        "li.page-item.page-link.PagedList-skipToNext"
                    )
                    if next_page:
                        next_page.click()
                    else:
                        print("Error: Next page button not found.")
                        break
            except Exception as e:
                print(f"Error: Unable to process page URL {target_url}: {e}")
            finally:
                browser.close()
    return url_array


def silly_scrape(target_url, site_identifier="elit"):
    """
    scrapes specified ELIT url and returns the coram
    name(s), judgement date and number of paragraphs without
    differentiating material facts, obiter, ratio and final ruling
    """
    judge_array = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(target_url)
            print(f"Success: Accessed page URL {target_url}")
            page.wait_for_selector("div#divJudgement")
            title = page.query_selector("title").inner_text()
            date_year = title.split(" ")[0].strip("[]")
            court = title.split(" ")[1].strip()
            combined_judge_array = page.query_selector_all(
                '.Judg-Author, [id*="Judg-Author"]'
            )
            paragaph_count = len(
                page.query_selector_all(
                    'p[class*="Judg-"], div[class*="Judg-"], span[class*="Judg-"]'
                )
            )
            if len(combined_judge_array) > 0:
                for item in combined_judge_array:
                    judge_array.append(item.inner_text())
            else:
                print("Error: No judges were found.")
        except Exception as e:
            print(f"Error: Unable to process page URL {target_url}: {e}")
        finally:
            browser.close()
    wrapper = {
        title: {
            "coram": judge_array,
            "year": date_year,
            "court": court,
            "paragaph_count": paragaph_count,
        }
    }
    return wrapper


def smart_scrape(target_url):
    """
    scrapes specified ELIT filepath and returns the coram
    name(s), judgement date and number of paragraphs that also
    differentiates material facts, obiter, ratio and final ruling

    FUA might need to implement this by making calls to
    a locally trained LLM
    """
    pass
