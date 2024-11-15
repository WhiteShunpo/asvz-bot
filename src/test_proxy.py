from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def test_selenium_proxy():
    # Set up ChromeOptions with the proxy
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=http://proxy.ethz.ch:3128")
    
    # Initialize ChromeDriver with the options
    driver = webdriver.Chrome(options=options)

    try:
        # Test the proxy by visiting an IP-checking site
        driver.get("https://httpbin.org/ip")
        driver.implicitly_wait(5)  # Wait for the page to load
        
        # Extract and print the page source to confirm the IP address
        print(driver.page_source)
        
    finally:
        # Clean up
        driver.quit()

# Run the test
test_selenium_proxy()
