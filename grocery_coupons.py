import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

browser = None

def initialize():
    global browser

    path = os.getenv('GOOGLE_CHROME_SHIM') or None

    options = webdriver.ChromeOptions()
    options.binary_location = path
    if path:
        options.add_argument('headless')

    browser = webdriver.Chrome(executable_path='chromedriver', chrome_options = options)

    print 'Using ' + (path or './chromedriver')

def test(email, password, delay = 10, callback = None):
    result = { 'email': email, 'existingCount': 0, 'count': 0, 'message': None, 'screenshot': None }

    if callback:
        callback(result)

    return result

def shoprite(email, password, delay = 10, callback = None):
    result = { 'email': email, 'existingCount': 0, 'count': 0, 'message': None, 'screenshot': None }

    initialize()

    if callback:
        result['message'] = 'Navigating to home page.'
        callback(result)

    try:
        browser.get('https://www.shoprite.com')

        if callback:
            result['message'] = 'Locating sign-in page.'
            callback(result)

        # Wait for signin link.
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.ID, 'signinbutton'))
        )

        try:
        	browser.find_element_by_id('signinbutton').click()
        except Exception as e:
            print 'Already signed-in. ' + repr(e)

        if callback:
            result['message'] = 'Entering login details.'
            callback(result)

        # Login
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.ID, "Email"))
        )

        # Send login info.
        browser.find_element_by_id('Email').send_keys(email)
        browser.find_element_by_id('Password').send_keys(password)
        browser.find_element_by_id('Password').send_keys(Keys.RETURN)

        if callback:
            result['message'] = 'Signing in.'
            callback(result)

        # Wait until the site loads, find the welcome page or error message.
        WebDriverWait(browser, delay).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.main-menu-myaccount, .field-validation-error, .validation-summary-errors'))
        )

        if callback:
            result['message'] = 'Checking if login succeeded.'
            callback(result)

        # Check if the login succeeded.
        fields = browser.find_elements_by_xpath("//*[contains(text(), 'incorrect') or contains(text(), 'try again')]")
        if len(fields) > 0:
            # Invalid login?
            result['message'] = 'Error'
            result['error'] = 'Invalid login.'
            result['screenshot'] = browser.get_screenshot_as_base64()
            callback(result)
            count = -1
        else:
            if callback:
                result['message'] = 'Navigating to coupons.'
                callback(result)

            browser.get('http://coupons.shoprite.com')

            # Click the sign-in button again, if it's there.
            try:
                WebDriverWait(browser, delay).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.menuItem__button'))
                )

                signInButtons = browser.find_elements_by_css_selector("button.menuItem__button")
                if len(signInButtons) > 0:
                    print 'Clicking additional sign-in.'
                    signInButtons[0].click()
            except Exception as e:
                print 'Ignoring additional sign-in. ' + repr(e)

            WebDriverWait(browser, delay).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#coupon-center-title'))
            )

            if callback:
                result['message'] = 'Loading coupons.'
                callback(result)

            WebDriverWait(browser, delay).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "coupon-item"))
            )

            # Click the link to show all coupons
            #btnShowAll = browser.find_elements_by_xpath("//button[contains(text(), 'Show All')]")
            #btnShowAll[1].click()

            # Read all coupons on the current page, then process all subsequent pages by clicking Next, until no more pages.
            if callback:
                result['message'] = 'Reading coupons.'
                callback(result)

            btnNextDisabled = ''
            page = 1

            while len(btnNextDisabled) == 0:
                try:
                    # Click all the buttons to add the coupons to your card
                    list_of_coupon_buttons = browser.find_elements_by_css_selector("a.available-to-clip:not(.ng-hide)")

                    for count, coupon_button in enumerate(list_of_coupon_buttons, start=1):
                        coupon_button.click()

                        if callback:
                            result['count'] += 1
                            result['message'] = 'Added ' + str(result['count']) + '. Already clipped ' + str(result['existingCount']) + '. Page ' + str(page)
                            callback(result)

                        time.sleep(.250)

                    if callback:
                        result['existingCount'] += len(browser.find_elements_by_class_name('clipped-coupon-circle'))
                        result['message'] = 'Added ' + str(result['count']) + '. Already clipped ' + str(result['existingCount']) + '. Page ' + str(page)
                        result['screenshot'] = browser.get_screenshot_as_base64()
                        callback(result)

                    # Get the next page.
                    btnNextDisabled = browser.find_elements_by_xpath("//button[contains(@class, 'disabled') and contains(text(), 'Next')]")
                    if len(btnNextDisabled) == 0:
                        btnNext = browser.find_elements_by_xpath("//button[contains(text(), 'Next')]")
                        btnNext[1].click()

                        page += 1

                        if callback:
                            result['message'] = 'Added ' + str(result['count']) + '. Already clipped ' + str(result['existingCount']) + '. Page ' + str(page)
                            callback(result)

                        time.sleep(0.5)
                except UnexpectedAlertPresentException as e:
                    print "Dismissing alert " + repr(e)
                    alert = browser.switch_to_alert()
                    alert.accept()
                    continue
                except Exception as e:
                    print repr(e)
                    continue

            if callback:
                result['message'] = 'Complete!'
                callback(result)
    except UnexpectedAlertPresentException as e:
        alert = browser.switch_to_alert()
        alert.accept()
    except Exception as e:
        if callback:
            result['message'] = 'Error'
            result['error'] = repr(e)
            result['screenshot'] = browser.get_screenshot_as_base64()
            callback(result)

    browser.close()

    return result

def stop_and_shop(email, password, delay = 10, callback = None, complete = None):
    initialize()

    # Get email/password from config file
    email = parser.get('stop and shop', 'email')
    password = parser.get('stop and shop', 'password')

    # Visit the Login page
    browser.get('https://stopandshop.com/login/')

    # Login
    help_element = browser.find_element_by_link_text('help')
    help_element.send_keys(Keys.TAB)
    username_element = browser.switch_to.active_element
    username_element.send_keys(email)
    username_element.send_keys(Keys.TAB)
    password_element = browser.switch_to.active_element
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)

    # Wait until link to go to coupons page is ready
    WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'coupons'))
    )

    # Go to coupons page
    browser.get('https://stopandshop.com/dashboard/coupons-deals/')

    # Wait until coupons are ready
    WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'load-to-card'))
    )

    # Click all the buttons to add the coupons to your card
    list_of_coupon_buttons = browser.find_elements_by_class_name('load-to-card')

    for count, coupon_button in enumerate(list_of_coupon_buttons, start=1):
        try:
            coupon_button.click()
            if callback:
                result['message'] = 'Added ' + str(count) + ' coupons!'
                result['count'] = count
                callback(result)
            time.sleep(1)
        except:
            continue

    result['screenshot'] = browser.get_screenshot_as_base64()

    if callback:
        result['message'] = 'Complete!'
        callback(result)

    browser.close()

    return result
