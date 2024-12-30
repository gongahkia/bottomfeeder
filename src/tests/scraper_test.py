import pytest
import caplog
import scraper
from unittest.mock import patch


def test_silly_generate_url_endpoint_current_year():
    """
    tests silly_generate_url_endpoint with current year
    """
    url_array = scraper.silly_generate_url_endpoint(2024)
    assert len(url_array) > 0


def test_silly_generate_url_endpoint_future_year_capped():
    """
    tests silly_generate_url_endpoint with future year capped
    """
    url_array = scraper.silly_generate_url_endpoint(2025)
    assert len(url_array) > 0
    for url in url_array:
        assert int(url.split("_")[0]) == 2024


@patch("scraper.sync_playwright")
def test_smart_find_url_endpoint_valid_number(mock_playwright):
    """
    tests smart_find_url_endpoint with valid number
    """
    url_array = scraper.smart_find_url_endpoint(100)
    assert len(url_array) == 100


def test_smart_find_url_endpoint_invalid_number(mock_playwright):
    """
    tests smart_find_url_endpoint with invalid number
    """
    with pytest.raises(ValueError):
        scraper.smart_find_url_endpoint(15)


@patch("scraper.sync_playwright")  # Mocking playwright library
def test_silly_scrape_success(mock_playwright):
    """
    tests silly_scrape with successful scraping (mocked)
    """
    mock_playwright.return_value.chromium.launch.return_value.new_page.return_value.query_selector.return_value.inner_text = (
        "Judge John Doe"
    )
    wrapper = scraper.silly_scrape("https://www.example.com")
    assert "coram" in wrapper["title"]


@patch("scraper.sync_playwright")
def test_silly_scrape_no_judges(mock_playwright):
    """
    tests silly_scrape when no judges are found
    """
    mock_playwright.return_value.chromium.launch.return_value.new_page.return_value.query_selector_all.return_value = (
        []
    )
    wrapper = scraper.silly_scrape("https://www.example.com")
    assert wrapper["title"]["coram"] == []
    assert "Error: No judges were found." in caplog.text


@patch("scraper.sync_playwright")
def test_silly_scrape_page_not_found(mock_playwright):
    """
    tests silly_scrape when the page is not found
    """
    mock_playwright.return_value.chromium.launch.return_value.new_page.return_value.goto.side_effect = Exception(
        "Page not found"
    )
    with pytest.raises(Exception, match="Page not found"):
        scraper.silly_scrape("https://www.example.com")


@patch("scraper.sync_playwright")
def test_silly_scrape_selector_not_found(mock_playwright):
    """
    tests silly_scrape when the required selector is not found
    """
    mock_playwright.return_value.chromium.launch.return_value.new_page.return_value.query_selector.side_effect = Exception(
        "Selector not found"
    )
    with pytest.raises(Exception, match="Selector not found"):
        scraper.silly_scrape("https://www.example.com")
