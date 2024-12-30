# ----- REQUIRED IMPORTS -----

from playwright.sync_api import sync_playwright

# ----- HELPER FUNCTIONS -----


def silly_scrape(site_identifier, target_url):
    """
    scrapes specified ELIT filepath and returns the coram
    name(s), judgement date and number of paragraphs without
    differentiating material facts, obiter, ratio and final ruling

    FUA add scraping of date
    """
    judge_array = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(target_url)
            print(f"Success: Accessed page URL {target_url}")
            page.wait_for_selector("div#divJudgement")
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
                    print(item.inner_text())
                    judge_array.append(item.inner_text())
            else:
                print("Error: No judges were found.")
        except Exception as e:
            print(f"Error: Unable to process page URL {target_url}: {e}")
        finally:
            browser.close()
    wrapper = {
        site_identifier: {"coram": judge_array, "paragaph_count": paragaph_count}
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


# ----- TEST EXECUTION CODE -----

if __name__ == "__main__":
    print(
        silly_scrape(
            "Gay Choon Ing v Loh Sze Ti Terence Peter and Another Appeal",
            "https://www.elitigation.sg/gd/s/2009_SGCA_3",
        )
    )
