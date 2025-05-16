import time, sys, os, logging, platform
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# website to perform the looping for purchase
website = 'https://ippodotea.com/collections/matcha/products/sayaka-100g'
website = 'https://ippodotea.com/collections/matcha/products/uji-shimizu'
# Other defined variables for the script
poll_interval = 0.5
refresh_interval = 60 * 60
log_interval = 60
matcha_type = "sayaka-100g"
# For testing
matcha_type = "uji-shimizu"


# Initialize the driver and load the .env variables that will be utilized
def startup_process():
    # search for the .env file in the project dir
    load_dotenv()

    # Arguments for the chrome driver
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Chrome driver handling
    try:
        arch = platform.machine().lower()
        logging.info(f"Detected architecture: {arch}")


        # Webdriver does not play nice with ARM arch, this will default to install location of ChromeDriver
        if 'arm' in arch or 'aarch64' in arch:
            logging.warning("ARM architecture detected. Using manual chromedriver path.")
            # Adjust this path based on where you manually installed chromedriver
            chromedriver_path = "/usr/bin/chromedriver"
        else:
            # Default argument for webdriver-manager whenever it is not ARM based
            chromedriver_path = ChromeDriverManager().install()

        driver = webdriver.Chrome(service=Service(chromedriver_path))
        logging.info("ChromeDriver started successfully.")
        return driver
    except Exception as e:
        logging.error(f"Failed to start ChromeDriver: {e}")
        sys.exit(1)



driver = startup_process()
driver.get(website)
wait = WebDriverWait(driver, 15, poll_frequency=poll_interval)
start_time = time.time()
last_refresh = time.time()
last_log_time = time.time()


while True:
    # Refreshes the webpage every refresh_interval so that the bot stays fresh
    now = time.time()
    if now - last_refresh >= refresh_interval:
        logging.info(f"It has been 1 hour since the last refresh. Refreshing the webpage at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        driver.refresh()
        last_refresh = now
        # Give the driver some time to refresh the webpage before beginning the loop again
        time.sleep(5)

    try:
        btn_add_to_cart = driver.find_element(By.CSS_SELECTOR, 'button.product-addbtn')
    except Exception as e:
        pass
    
    if "add to bag" in btn_add_to_cart.text.lower():
        print("The script has been activated, this means the add to cart button is active")


        # Ensure the selectable is the correct product
        selectable_other_sizes = driver.find_element(By.ID, "options")
        selectable_other_sizes_wait = wait.until(EC.element_to_be_clickable(selectable_other_sizes))
        if selectable_other_sizes_wait.get_attribute("value") != matcha_type:
            selectable_other_sizes_dropdown = Select(selectable_other_sizes_wait)
            selectable_other_sizes_dropdown.select_by_value(matcha_type)
            print(f"Wrong option... selecting the correct option and moving on")
        

        # Ensure the qty is 1 and 1 only
        cart_qty = driver.find_element(By.ID, "mainQty")
        def get_cart_qty():
            return int(cart_qty.get_attribute("value"))
        cart_value = get_cart_qty()
        while cart_value > 1:
            btn_minus_qty = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="increase quantity"]')
            cart_value = get_cart_qty()
        

        # Click the add to cart button
        btn_add_to_cart.click()


        # Click the checkout button
        btn_checkout = driver.find_element(By.XPATH, '//div[@role="button" and contains(., "Checkout")]')
        btn_checkout_wait = wait.until(EC.element_to_be_clickable(btn_checkout))
        btn_checkout_wait.click()


        # End the script whenever the purchase has been made
        time.sleep(10)
        driver.quit()
        sys.exit(0)


    print(f"Button not active at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    time.sleep(poll_interval)



