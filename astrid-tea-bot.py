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


# real site
website = 'https://astridtea.com/products/okita-matcha?variant=45366670033119'
# this is live cart test
website = 'https://astridtea.com/products/takayama-chasen-matcha-whisk'
# search for the .env file in the project dir
load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    logger.info("ChromeDriver started successfully.")
except SessionNotCreatedException as e:
    logger.error(f"Session failed: Chrome/driver version mismatch? {e}")
    sys.exit(1)
except WebDriverException as e:
    logger.error(f"WebDriver error starting Chrome: {e}")
    sys.exit(1)


driver.get(website)
wait = WebDriverWait(driver, 15, poll_frequency=0.5)
time.sleep(5)


actions = ActionChains(driver)
actions.move_to_element_with_offset(driver.find_element(By.TAG_NAME, "body"), x_offset=200, y_offset=150)
actions.click()
actions.perform()


while True:


    # The add to cart button
    btn_add_to_cart = driver.find_element(By.CSS_SELECTOR,"button.product__form-submit.btn.btn--primary.btn--outline[type='submit'][name='add']")


    # if add to cart button is enabled
    if btn_add_to_cart.get_attribute('disabled') is None:
        print("it is enabled!")


        # The quantity amount
        qty_attr = driver.find_element(By.XPATH,"//input""[@type='number'"" and @name='quantity'"" and contains(@class,'qty__adjust-input')"" and @data-quantity-field]")
        def get_qty():
            return int(qty_attr.get_attribute("value"))


        # ensures that after the add to cart element is enabled, that we still have to selected before adding to cart
        qty_value = get_qty()
        while qty_value > 2:
            minus_btn =     driver.find_element(By.CSS_SELECTOR,"button.qty__adjust-btn.qty__adjust-btn--minus""[type='button'][aria-label='Decrease'][data-quantity-minus][data-quantity-button]").click()
            time.sleep(0)
            qty_value = get_qty()
        while qty_value < 2:
            plus_btn = driver.find_element(By.CSS_SELECTOR,"button.qty__adjust-btn.qty__adjust-btn--plus""[type='button'][aria-label='Increase'][data-quantity-plus][data-quantity-button]").click()
            time.sleep(0)
            qty_value = get_qty()


        # add the item to the cart
        btn_add_to_cart.click()


        # find and wait for the checkout button to be clickable
        btn_checkout = (By.XPATH,"//button""[@type='submit' and @name='button-route-2']""[contains(@class,'cart__checkout') and contains(@class,'btn--primary')]")
        btn_checkout_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(btn_checkout))
        btn_checkout_wait.click()


        ''' BEGINNING OF THE CHECKOUT PROCESS '''


        # STEP 01 --> input the email address
        input_email = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        input_email.clear()
        input_email.send_keys(os.getenv("EMAIL"))


        # STEP 02 --> ensure the marketing checkbox is not selected
        checkbox_marketing = wait.until(EC.element_to_be_clickable((By.NAME, "marketing_opt_in")))
        if checkbox_marketing.is_selected:
            checkbox_marketing.click()


        # STEP 03 --> select the country
        selectable_country = wait.until(EC.element_to_be_clickable((By.NAME, "countryCode")))
        selectable_country_dropdown = Select(selectable_country)
        selectable_country_dropdown.select_by_value(os.getenv("COUNTRY"))


        # STEP 04 --> input first name
        input_firstname = driver.find_element(By.NAME, "firstName")
        input_firstname_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_firstname))
        input_firstname_wait.send_keys(os.getenv("FIRST_NAME"))


        # STEP 05 --> input last name
        input_firstname = driver.find_element(By.NAME, "lastName")
        input_firstname_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_firstname))
        input_firstname_wait.send_keys(os.getenv("LAST_NAME"))


        # STEP 06 --> input address
        input_address = driver.find_element(By.NAME, "address1")
        input_address_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_address))
        input_address_wait.send_keys(os.getenv("ADDRESS"))


        # STEP 07 --> input address 02
        input_address_02 = driver.find_element(By.NAME, "address2")
        input_address_02_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_address_02))
        input_address_02_wait.send_keys(os.getenv("ADDRESS_02"))


        # STEP 08 --> city
        input_city = driver.find_element(By.NAME, "city")
        input_city_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_city))
        input_city_wait.send_keys(os.getenv("CITY"))


        # STEP 09 --> state
        selectable_state = driver.find_element(By.NAME, "zone")
        selectable_state_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(selectable_state))
        selectable_state_dropdown = Select(selectable_state)
        selectable_state_dropdown.select_by_value(os.getenv("STATE"))


        # STEP 10 --> postal code
        input_zip = driver.find_element(By.NAME, "postalCode")
        input_zip_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_zip))
        input_zip_wait.send_keys(os.getenv("ZIP_CODE"))


        # STEP 11 --> phone
        input_phone = driver.find_element(By.NAME, "phone")
        input_phone_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(input_phone))
        input_phone_wait.send_keys(os.getenv("PHONE"))


        ''' INPUT CARD CREDENTIALS '''

        # STEP 01 --> input card number
        expiration_date_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-number-')]")))
        card_number_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'number')))
        card_number_container.send_keys(os.getenv("CARD_NUMBER"))
        driver.switch_to.default_content()


        # STEP 02 --> input expiration date
        expiration_date_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-expiry-')]")))
        expiration_date_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'expiry')))
        expiration_date_container.send_keys(os.getenv("EXPIRATION_MONTH"))
        expiration_date_container.send_keys(os.getenv("EXPIRATION_YEAR"))
        driver.switch_to.default_content()


        # STEP 03 --> input security code
        security_code_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-verification_value-')]")))
        security_code_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'verification_value')))
        security_code_container.send_keys(os.getenv("SECURITY_CODE"))
        driver.switch_to.default_content()


        # STEP 04 --> input card name
        card_name_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-name-')]")))
        card_name_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'name')))
        card_name = card_name_container.get_attribute(os.getenv("NAME_ON_CARD"))
        # STEP 05 --> ensure that the card name is correct
        if card_name != card_name:
            # first try to clear the name before we input the correct name
            try:
                clear_button = driver.find_element(By.XPATH, "//button[@aria-label='Clear']").click()
            except Exception as e:
                print("An error was raised: ", e)
            # double check the name value has been removed
            try:
                driver.execute_script("arguments[0].removeAttribute('value');", card_name_container)
            except Exception as e:
                print("An error was raised: ", e)
            card_name_container.send_keys()
        driver.switch_to.default_content()


        # STEP 06 --> ensure the shipping is the same as billing
        checkbox_billing = driver.find_element(By.NAME, "billingAddress")
        checkbox_billing_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(checkbox_billing))
        if not checkbox_billing_wait.is_selected:
            checkbox_billing_wait.click()


        # STEP 07 --> ensure that our information is not saved by SHOP
        checkbox_remember_me = driver.find_element(By.NAME, "RememberMe")
        checkbox_remember_me_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(checkbox_remember_me))
        if checkbox_remember_me_wait.is_selected:
            checkbox_remember_me_wait.click()


        # STEP 08 --> click pay now
        btn_pay_now = driver.find_element(By.ID, "checkout-pay-button")
        btn_pay_now_wait = WebDriverWait(driver, 10, poll_frequency=0.5).until(EC.element_to_be_clickable(btn_pay_now))
        btn_pay_now_wait.click()


        print("Purchase made, I am going to sleep!!!")
        time.sleep(60)
        sys.exit(0)


    print("it is disabled!")
    time.sleep(0.5)