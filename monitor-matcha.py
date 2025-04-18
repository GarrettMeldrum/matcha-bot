import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


webpageURL = 'https://j-j-market.com/products/matcha-wako-from-marukyu-koyamaen-100g'
webpageURL = 'https://j-j-market.com/products/matcha-powder-yame-no-mukashi-from-jj-market-30g' # test matcha product page


input_email = 'garrettmeldrum14@gmail.com'
input_country = 'United States'
input_first_name = 'Malorie'
input_last_name = 'Stick'
input_address_1 = '8200 ARISTA PL'
input_address_2 = 'UNIT 306'
input_city = 'BROOMFIELD'
input_state = 'Colorado'
input_zip_code = '80021'
input_phone_number = '5809209875'


input_card_number = '5239925934326174'
input_expiration_date_month = '09'
input_expiration_date_year = '25'
input_security_code = '909'
input_name_on_card = 'Malorie Stick'


driver = webdriver.Chrome()
driver.get(webpageURL)
time.sleep(5)


# iterating
timeout = 60
poll_interval = 0.5
start_time = time.time()
wait = WebDriverWait(driver, 20)


# Configure the log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


while True:
    buttonAddToCart = driver.find_element(By.ID, "ProductSubmitButton-template--22602600186182__main")

    # Check if the 'disabled' attribute is absent, meaning the button is enabled
    if buttonAddToCart.get_attribute('disabled') is None:
        print("The 'Add to Cart' button is enabled! Oh boy, it's Mitzi time!")
        

        # Click add to cart
        # This step does not require any implicit waiting or sleep
        buttonAddToCart.click()
        
        
        # Click on the cart icon
        # Implicit wait and sleep to give the website enough time to interact with the element
        #driver.implicitly_wait(10)
        time.sleep(1)
        #cart_icon = driver.find_element(By.ID, "cart-icon-bubble")
        cart_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'cart-icon-bubble')))
        cart_icon.click()


        # Click the checkbox for worried free delivery
        # Implicit wait and sleep to give the website enough time to interact with the element
        #driver.implicitly_wait(10)
        time.sleep(1)
        checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and @name='checkbox']")
        #checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='checkbox']")))
        # quick test to make sure that the checkbox is checked or not. If not then ensure it is clicked.
        if not checkbox.is_selected():
            checkbox.click()


        # Worry-Free Delivery button to add quantity
        # Implicit wait and sleep to give the website enough time to interact with the element
        #driver.implicitly_wait(10)
        time.sleep(1)
        #worry_free_delivery = driver.find_element(By.XPATH, "//a[@class='cart-item__name h4 break' and text()='Worry-Free Delivery']")
        worry_free_delivery = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='cart-item__name h4 break' and text()='Worry-Free Delivery']")))
        #quantity_box = driver.find_element(By.XPATH, "//button[@class='quantity__button' and @name='plus']")
        quantity_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='quantity__button' and @name='plus']")))
        quantity_box.click()


        # Click the checkout button
        # Do not want to wait or sleep here
        #checkout_button = driver.find_element(By.ID, "checkout")
        checkout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'checkout')))
        checkout_button.click()


        '''
        CHECKING OUT SECTION
        '''


        # input email
        #email_container = driver.find_element(By.ID, "email")
        email_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email')))
        email_container.send_keys(input_email)


        # select country from dropdown
        #country_container = driver.find_element(By.NAME, 'countryCode')
        country_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'countryCode')))
        select_country = Select(country_container).select_by_value("US")
        #select_country.select_by_value("US")
        

        # input first name
        #first_name_container = driver.find_element(By.NAME, "firstName")
        first_name_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'firstName')))
        first_name_container.send_keys(input_first_name)
        

        # input last name
        #last_name_container = driver.find_element(By.NAME, "lastName")
        last_name_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'lastName')))
        last_name_container.send_keys(input_last_name)


        # input address 1
        #address_container = driver.find_element(By.NAME, "address1")
        address_container_1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'address1')))
        address_container_1.send_keys(input_address_1)


        # input address 2
        #address_container = driver.find_element(By.NAME, "address2")
        address_container_2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'address2')))
        address_container_2.send_keys(input_address_2)


        # input city name
        #city_container = driver.find_element(By.NAME, "city").send_keys(input_city)
        city_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'city')))
        city_container.send_keys(input_city)


        # select state via dropdown
        #state_container = driver.find_element(By.NAME, 'zone')
        state_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'zone')))
        select_state = Select(state_container).select_by_visible_text("Colorado")
        #select_state.select_by_visible_text("Colorado")


        # input zip code
        #zip_code_container = driver.find_element(By.NAME, 'postalCode').send_keys(input_zip_code)
        zip_code_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'postalCode')))
        zip_code_container.send_keys(input_zip_code)


        # input phone number
        #phone_number_container = driver.find_element(By.NAME, 'phone').send_keys(input_phone_number)
        phone_number_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'phone')))
        phone_number_container.send_keys(input_phone_number)


        # input card number
        expiration_date_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-number-')]")))
        card_number_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'number')))
        card_number_container.send_keys(input_card_number)
        driver.switch_to.default_content()


        # input expiration date
        expiration_date_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-expiry-')]")))
        expiration_date_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'expiry')))
        expiration_date_container.send_keys(input_expiration_date_month)
        expiration_date_container.send_keys(input_expiration_date_year)
        driver.switch_to.default_content()


        # input security code
        security_code_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-verification_value-')]")))
        security_code_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'verification_value')))
        security_code_container.send_keys(input_security_code)
        driver.switch_to.default_content()


        # input card name
        card_name_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'card-fields-iframe') and starts-with(@id, 'card-fields-name-')]")))
        card_name_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'name')))
        card_name = card_name_container.get_attribute("value")
        # ensure that the card name is correct
        if card_name != input_name_on_card:
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


        # ensure the "Use shipping address as billing address" is selected
        shipping_is_billing_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billingAddress")))
        if not shipping_is_billing_checkbox.is_selected():
            shipping_is_billing_checkbox.click()


        remember_me_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "RememberMe-RememberMeCheckbox")))
        if remember_me_checkbox.is_selected():
            remember_me_checkbox.click()



        # click "Pay now" and the order has been placed
        pay_now_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout-pay-button")))
        pay_now_container.click()

        print("Purchase completed!")
        time.sleep(60)
        



    print(f"Attribute still disabled at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    time.sleep(poll_interval)




    