import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.download_manager import WDMDownloadManager

class CustomHttpClient:
    def __init__(self, proxy=None, username=None, password=None):
        self.proxy = proxy
        self.username = username
        self.password = password

    def get(self, url):
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        if self.proxy:
            proxy_auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
            proxies = {
                "http": f"http://{proxy_auth}{self.proxy}",
                "https": f"http://{proxy_auth}{self.proxy}",
            }
        else:
            proxies = None

        response = session.get(url, proxies=proxies, allow_redirects=False)  # Test without redirects
        response.raise_for_status()
        return response


def test_custom_http_client():
    proxy_url = "http://129.132.202.155:3128"  # Use the resolved IP address
    custom_client = CustomHttpClient(proxy=proxy_url)
    response = custom_client.get("https://google.com")
    print(response)
    assert response is not None


def test_can_get_chrome_driver_with_custom_http_client():
    proxy_url = "http://129.132.202.155:3128"  # Use the resolved IP address
    http_client = CustomHttpClient(proxy=proxy_url)
    download_manager = WDMDownloadManager(http_client)
    path = ChromeDriverManager(download_manager=download_manager).install()
    assert os.path.exists(path)


def test_selenium_driver():
    proxy_url = "http://129.132.202.155:3128"  # Use the resolved IP address
    http_client = CustomHttpClient(proxy=proxy_url)
    download_manager = WDMDownloadManager(http_client)
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server={proxy_url}')
    path = ChromeDriverManager(download_manager=download_manager).install()
    driver = webdriver.Chrome(options=options)

    # Navigate to the Google homepage
    driver.get("https://www.google.com")

    # Wait for a few seconds to see the search results
    driver.implicitly_wait(5)

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    test_custom_http_client()
    test_can_get_chrome_driver_with_custom_http_client()
    test_selenium_driver()