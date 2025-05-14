import time, sys, os, logging
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


webpageURL = 'https://j-j-market.com/products/matcha-wako-from-marukyu-koyamaen-100g'
#webpageURL = 'https://j-j-market.com/products/matcha-powder-yame-no-mukashi-from-jj-market-30g' # test matcha product page

# search for the .env file in the project dir
load_dotenv()


# Configure and start the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    driver_path = ChromeDriverManager().install()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.info("ChromeDriver started successfully.")
except SessionNotCreatedException as e:
    logger.error(f"Session failed: Chrome/driver version mismatch? {e}")
    sys.exit(1)
except WebDriverException as e:
    logger.error(f"WebDriver error starting Chrome: {e}")
    sys.exit(1)

driver.get(webpageURL)
wait = WebDriverWait(driver, 15, poll_frequency=0.5)
time.sleep(5)


refresh_interval = 60 * 60
last_refresh = time.time()
poll_interval = 0.5
start_time = time.time()
log_interval = 60
last_log_time = time.time()


print(f"JJ-Market Bot --> Script started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
while True:
    now = time.time()
    if now - last_refresh >= refresh_interval:
        logging.info("Refreshing page after 1 hour")
        driver.refresh()
        last_refresh = now
        time.sleep(5)
        
        
    try:
        buttonAddToCart = driver.find_element(By.ID, "ProductSubmitButton-template--22602600186182__main")
    except Exception as e:
        logging.warning("Coudn't find add-to-cart button, will retry")
        time.sleep(1)
        continue
    

    # Check if the button is enabled
    if buttonAddToCart.get_attribute('disabled') is None:
        print("The 'Add to Cart' button is enabled! Oh boy, it's Mitzi time!")
        

        # STEP 01
        buttonAddToCart.click()
        time.sleep(1)
        print(f"STEP 01 --> Clicked add to cart at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")
        

        # STEP 02 --> Go to the cart
        cart_icon = (By.ID, 'cart-icon-bubble')
        cart_icon_wait = wait.until(EC.element_to_be_clickable(cart_icon))
        cart_icon_wait.click()
        print(f"STEP 02 --> Clicked the cart icon at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")
        

        # STEP 03 --> Wait for the worry-free delivery checkbox to appear
        checkbox_footer = driver.find_element(By.ID, "main-cart-footer")
        checkbox_wait = wait.until( lambda drv: checkbox_footer.find_element(By.NAME, "checkbox"))
        if not checkbox_wait.is_selected():
            checkbox_wait.click()
            print(f"STEP 03 --> Checked the worry-free delivery box at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")
        print(f"STEP 03 --> Ensured the worry-free delivery box was checked at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 04 --> Check if we can find the worry-free delivery and if not, reclick the checkbox to make the element appear
        try:
            cart_item_row = (By.XPATH,"//tr[contains(@class,'cart-item') and "".//a[contains(@class,'cart-item__name') and normalize-space(text())='Worry-Free Delivery']]")
            cart_item_row_wait = wait.until(EC.presence_of_element_located(cart_item_row))
        except:
            checkbox_wait.click()
            time.sleep(1)
            checkbox_wait.click()
            cart_item_row_wait
        print(f"STEP 04 --> Ensured that worry-free delivery has been added to cart")


        # STEP 05 --> Click the plus button to get us over the free shipping limit
        plus_btn_wait = wait.until( lambda drv: cart_item_row_wait.find_element(By.NAME, "plus"))
        plus_btn_wait.click()
        print(f"STEP 05 --> Clicked the plus button at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 06 --> Click the checkout button
        checkout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'checkout')))
        checkout_button.click()
        print(f"STEP 06 --> Clicked checkout button at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")
      

        ''' CHECKING OUT SECTION '''


        # STEP 07 --> Input the email address
        input_email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
        input_email.clear()
        input_email.send_keys(os.getenv('EMAIL'))
        print(f"STEP 07 --> Inputted email address at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 08 --> Select country from dropdown
        select_country = wait.until(EC.element_to_be_clickable((By.NAME, "countryCode")))
        Select(select_country).select_by_value(os.getenv("COUNTRY"))
        print(f"STEP 08 --> Selected country from dropdown at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")
        

        # STEP 09 --> Input first name
        input_firstname = wait.until(EC.element_to_be_clickable((By.NAME, "firstName")))
        input_firstname.send_keys(os.getenv("FIRST_NAME"))
        print(f"STEP 09 --> Inputted first name at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 10 --> Input last name
        input_lastname = wait.until(EC.element_to_be_clickable((By.NAME, "lastName")))
        input_lastname.send_keys(os.getenv("LAST_NAME"))
        print(f"STEP 10 --> Inputted last name at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 11 --> Input address 1
        input_address = wait.until(EC.element_to_be_clickable((By.NAME, "address1")))
        input_address.send_keys(os.getenv("ADDRESS"))
        print(f"STEP 11 --> Inputted address line 1 at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 12 --> Input address 2
        input_address_02 = wait.until(EC.element_to_be_clickable((By.NAME, "address2")))
        input_address_02.send_keys(os.getenv("ADDRESS_02"))
        print(f"STEP 12 --> Inputted address line 2 at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 13 --> Input city name
        input_city = wait.until(EC.element_to_be_clickable((By.NAME, "city")))
        input_city.send_keys(os.getenv("CITY"))
        print(f"STEP 13 --> Inputted city at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 14 --> Select state via dropdown
        select_state = wait.until(EC.element_to_be_clickable((By.NAME, "zone")))
        Select(select_state).select_by_value(os.getenv("STATE"))
        print(f"STEP 14 --> Selected state at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 15 --> Input zip code
        input_zip_code = wait.until(EC.element_to_be_clickable((By.NAME, "postalCode")))
        input_zip_code.send_keys(os.getenv("ZIP_CODE"))
        print("STEP 15 --> Inputted zip code at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 16 --> Input phone number
        input_phone = wait.until(EC.element_to_be_clickable((By.NAME, "phone")))
        input_phone.send_keys(os.getenv("PHONE"))
        print(f"STEP 16 --> Inputted phone number at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 17 --> Input card number
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-number-')]")))
        card_number_container = wait.until(EC.element_to_be_clickable((By.ID, "number")))
        card_number_container.send_keys(os.getenv("CARD_NUMBER"))
        driver.switch_to.default_content()
        print(f"STEP 17 --> Inputted the card number at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 18 --> Input expiration date
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-expiry-')]")))
        expiration_date_container = wait.until(EC.element_to_be_clickable((By.ID, "expiry")))
        expiration_date_container.send_keys(os.getenv("EXPIRATION_MONTH"))
        expiration_date_container.send_keys(os.getenv("EXPIRATION_YEAR"))
        driver.switch_to.default_content()
        print(f"STEP 18 --> Inputted the expiration date at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 19 --> Input security code
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-verification_value-')]")))
        security_code_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "verification_value")))
        security_code_container.send_keys(os.getenv("SECURITY_CODE"))
        driver.switch_to.default_content()
        print(f"STEP 19 --> Inputted the security code at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 20 --> Input card name
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-name-')]")))
        card_name_container = wait.until(EC.element_to_be_clickable((By.ID, "name")))
        card_name = card_name_container.get_attribute("value")
        correct_card_name = os.getenv("NAME_ON_CARD")
        if card_name != correct_card_name:
            # first try to clear the name before we input the correct name
            try:
                card_name_container.clear()
            except Exception as e:
                print("An error was raised: ", e)
            card_name_container.send_keys(correct_card_name)   
        driver.switch_to.default_content()
        print(f"STEP 17 --> Ensured/Inputted card name at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 21 --> Check/Ensure the checkbox for billing same as shipping is selected
        checkbox_billing_is_shipping = wait.until(EC.element_to_be_clickable((By.ID, "billingAddress")))
        if checkbox_billing_is_shipping.is_selected() == False:
            checkbox_billing_is_shipping.click()
        print(f"STEP 21 --> Checked/Ensured the checkbox for billing same as shipping is clicked at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")


        # STEP 22 --> Check/Ensure the checkbox is unchecked for remember me
        remember_me_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "RememberMe-RememberMeCheckbox")))
        if remember_me_checkbox.is_selected():
            remember_me_checkbox.click()
        print(f"STEP 22 --> Checked/Ensured the checkbox is not selected for remember me at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")



        # STEP 23 --> Click "Pay now" and the order has been placed
        pay_now_container = wait.until(EC.element_to_be_clickable((By.ID, "checkout-pay-button")))
        pay_now_container.click()
        print(f"STEP 23 --> Clicked pay now and the order has been placed at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}...")
        print("Purchase completed! Script will terminate in 10 seconds...")
        time.sleep(10)
        driver.quit()
        sys.exit(0)
        

    if now - last_log_time >= log_interval:
        print(f"JJ-Market Bot --> Attribute still disabled at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        last_log_time = now
    time.sleep(poll_interval)
