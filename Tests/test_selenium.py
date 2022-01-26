"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import freecash_info

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

ayet = "https://www.ayetstudios.com/offers/web_offerwall/2693?external_identifier=fsid-2308045-607783a635"

@pytest.fixture(scope="class",autouse=True)
def setup_ayet_page(request):
    """
    Set Ayet page as fixture
    """
    ayet_page = freecash_info.set_driver_and_scrape_ayet()
    request.cls.ayet_page = ayet_page
    yield ayet_page
    ayet_page.close()

@pytest.mark.usefixtures("setup_ayet_page")

class TestAYET:
    """
    Full Ayet test suite
    """
    def test_access_ayet_offerwall(self):
        """
        Tests if able to successfully open Ayet Offerwall
        """
        full_ayet_page = self.ayet_page
        assert self.ayet_page.current_url == ayet

    def test_get_offerwall_content(self):
        """
        Tests if able to successfully get content from the Ayet Offerwall
        """
        full_ayet_page = self.ayet_page
        get_offers = freecash_info.get_current_ayet_offers(full_ayet_page)
        assert len(get_offers)>1

# def test_parse_offer_titles(setup_driver):
#     """
#     Tests if able to successfully parse titles from the offerwall text
#     """
#     full_ayet_page = freecash_info.open_ayet_offerwall(setup_driver)
#     get_offers = freecash_info.get_current_ayet_offers(full_ayet_page)
#     offer_titles = freecash_info.parse_offer_titles(get_offers)
#     assert len(offer_titles) > 0
