import time, sys, os, logging, platform
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException, WebDriverException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# website to perform the looping for purchase
website = 'https://ippodotea.com/collections/matcha/products/sayaka-100g'
# For testing
#website = 'https://ippodotea.com/collections/matcha/products/uji-shimizu'
# Other defined variables for the script
poll_interval = 0.5
refresh_interval = 60 * 60
log_interval = 60
matcha_type = "sayaka-100g"
# For testing
#matcha_type = "uji-shimizu"


# Initialize the driver and load the .env variables that will be utilized
def startup_process():

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

        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        logging.info("ChromeDriver started successfully.")
        return driver
    except Exception as e:
        logging.error(f"Failed to start ChromeDriver: {e}")
        sys.exit(1)


# search for the .env file in the project dir
load_dotenv()
driver = startup_process()
driver.get(website)
wait = WebDriverWait(driver, 15, poll_frequency=poll_interval)
start_time = time.time()
last_refresh = time.time()
last_log_time = time.time()

print(f"Script started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
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
        btn_add_to_cart = driver.find_element(By.CSS_SELECTOR, '.product-addbtn')
    except Exception as e:
        logging.warning("Coudn't find add-to-cart button, will retry")
        time.sleep(1)
        continue
    

    if btn_add_to_cart.text.lower() != 'sold out':


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
        print(f"The cart value is {cart_value}")
        

        # Click the add to cart button
        btn_add_to_cart.click()


        # Click the checkout button
        btn_checkout = driver.find_element(By.XPATH, '//div[@role="button" and contains(., "Checkout")]')
        btn_checkout_wait = wait.until(EC.element_to_be_clickable(btn_checkout))
        btn_checkout_wait.click()

        
        # STEP 01 --> input the email address
        input_email = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        input_email.clear()
        input_email.send_keys(os.getenv("EMAIL"))
        print(f"STEP 03 --> Inputted email address at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 02 --> ensure the marketing checkbox is not selected
        checkbox_marketing = wait.until(EC.element_to_be_clickable((By.NAME, "marketing_opt_in")))
        if checkbox_marketing.is_selected:
            checkbox_marketing.click()
        print(f"STEP 04 --> Unclicked the marketing checkbox at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 03 --> select the country
        selectable_country = wait.until(EC.element_to_be_clickable((By.NAME, "countryCode")))
        selectable_country_dropdown = Select(selectable_country)
        selectable_country_dropdown.select_by_value(os.getenv("COUNTRY"))
        print(f"STEP 05 --> Selected the country at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 04 --> input first name
        input_firstname = driver.find_element(By.NAME, "firstName")
        input_firstname_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_firstname))
        input_firstname_wait.send_keys(os.getenv("FIRST_NAME"))
        print(f"STEP 06 --> Inputted the first name at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 05 --> input last name
        input_lastname = driver.find_element(By.NAME, "lastName")
        input_lastname_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_lastname))
        input_lastname_wait.send_keys(os.getenv("LAST_NAME"))
        print(f"STEP 07 --> Inputted the last name at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 06 --> input address
        input_address = driver.find_element(By.NAME, "address1")
        input_address_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_address))
        input_address_wait.send_keys(os.getenv("ADDRESS"))
        print(f"STEP 08 --> Inputted the address at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 07 --> input address 02
        input_address_02 = driver.find_element(By.NAME, "address2")
        input_address_02_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_address_02))
        input_address_02_wait.send_keys(os.getenv("ADDRESS_02"))
        print(f"STEP 09 --> Inputted address 2 at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 08 --> city
        input_city = driver.find_element(By.NAME, "city")
        input_city_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_city))
        input_city_wait.send_keys(os.getenv("CITY"))
        print(f"STEP 10 --> Inputted city at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 09 --> state
        selectable_state = driver.find_element(By.NAME, "zone")
        selectable_state_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(selectable_state))
        selectable_state_dropdown = Select(selectable_state)
        selectable_state_dropdown.select_by_value(os.getenv("STATE"))
        print(f"STEP 11 --> Selected state at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 10 --> postal code
        input_zip = driver.find_element(By.NAME, "postalCode")
        input_zip_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_zip))
        input_zip_wait.send_keys(os.getenv("ZIP_CODE"))
        print(f"STEP 12 --> Inputted zip code at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 11 --> phone
        input_phone = driver.find_element(By.NAME, "phone")
        input_phone_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_phone))
        input_phone_wait.send_keys(os.getenv("PHONE"))
        print(f"STEP 13 --> Inputted phone number at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        ''' INPUT CARD CREDENTIALS '''


        # STEP 01 --> input card number
        expiration_date_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-number-')]")))
        card_number_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'number')))
        card_number_container.send_keys(os.getenv("CARD_NUMBER"))
        driver.switch_to.default_content()
        print(f"STEP 14 --> Inputted the card number at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 02 --> input expiration date
        expiration_date_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-expiry-')]")))
        expiration_date_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'expiry')))
        expiration_date_container.send_keys(os.getenv("EXPIRATION_MONTH"))
        expiration_date_container.send_keys(os.getenv("EXPIRATION_YEAR"))
        driver.switch_to.default_content()
        print(f"STEP 15 --> Inputted expiration date at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 03 --> input security code
        security_code_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-verification_value-')]")))
        security_code_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'verification_value')))
        security_code_container.send_keys(os.getenv("SECURITY_CODE"))
        driver.switch_to.default_content()
        print(f"STEP 16 --> Inputted security code at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 04 --> input card name
        card_name_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-name-')]")))
        card_name_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'name')))
        card_name = card_name_container.get_attribute("Value")
        correct_card_name = os.getenv("NAME_ON_CARD")
        # STEP 05 --> ensure that the card name is correct
        if card_name != correct_card_name:
            # first try to clear the name before we input the correct name
            try:
                card_name_container.clear()
            except Exception as e:
                print("An error was raised: ", e)
            card_name_container.send_keys(correct_card_name)   
        driver.switch_to.default_content()
        print(f"STEP 17 --> Ensured/Inputted card name at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 06 --> ensure the shipping is the same as billing
        checkbox_billing = driver.find_element(By.NAME, "billingAddress")
        checkbox_billing_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(checkbox_billing))
        if not checkbox_billing_wait.is_selected:
            checkbox_billing_wait.click()
        print(f"STEP 18 --> Ensured/Checked the billing same as shipping box at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 07 --> ensure that our information is not saved by SHOP
        checkbox_remember_me = driver.find_element(By.NAME, "RememberMe")
        checkbox_remember_me_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(checkbox_remember_me))
        if checkbox_remember_me_wait.is_selected:
            checkbox_remember_me_wait.click()
        print(f"STEP 19 --> Unclicked the remember me button at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")

        
        # STEP 20 --> click pay now
        btn_pay_now = driver.find_element(By.ID, "checkout-pay-button")
        btn_pay_now_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(btn_pay_now))
        btn_pay_now_wait.click()
        print(f"STEP 20 --> Clicked pay now button at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")
        


        # End the script whenever the purchase has been made
        time.sleep(60)
        driver.quit()
        sys.exit(0)


    if now - last_log_time >= log_interval:
        print(f"Attribute still disabled at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        last_log_time = now
    time.sleep(poll_interval)

