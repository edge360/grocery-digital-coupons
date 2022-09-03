import os
import time
import argparse
from configparser import RawConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay.display import Display



driver = None
display = None

def shoprite(email, password):

    #initialize browser and virt display
    initialize()

    try:
        print("Loading Page...")
        driver.get('https://www.shoprite.com/digital-coupon')

        print("Navigating to Login Page...")
        wait = WebDriverWait(driver, 60)
        wait.until(EC.element_to_be_clickable((By.ID, "AccountHeaderButton"))).click()


        print("Logging In...")
        wait.until(EC.element_to_be_clickable((By.ID, "Email"))).send_keys(email)
        driver.find_element(By.ID,'Password').send_keys(password)
        driver.find_element(By.ID,'Password').send_keys(Keys.RETURN)
        print("Logged In...")
        time.sleep(1)

        print("Redirecting back to Coupon page...")
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "sr-digital-coupons")))

        print("Loading All Coupons to page...")
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-default.btn-sm.ng-tns-c98-0.ng-star-inserted"))).click()

        print("Finding  Coupons...")
        coupon_count = 0
        coupons = driver.find_elements(By.CLASS_NAME, 'coupon-item-container')
        for coupon in coupons:
            coupon_name = coupon.find_element(By.CLASS_NAME, 'coupon-brand-name').text
            coupon_desc = coupon.find_element(By.CLASS_NAME, 'coupon-desc').text
            try:
                coupon.find_element(By.CLASS_NAME, 'available-to-clip.ng-star-inserted').click()
                print("Clipped: " + str(coupon_name) + " --- " + str(coupon_desc))
                count += 1
            except:
                #print("FAIL - Already Clipped")
                pass

        if coupon_count:
            print("Clipped " + coupon_count + "coupons :)")
        else:
            print("No Coupons Available")

        #close/quit chrome and stop display
        driver.close()
        driver.quit()
        display.stop()


    except Exception as e:
        #close/quit chrome and stop display on exception
        print(e)
        driver.close()
        driver.quit()
        display.stop()

def initialize():
    global driver
    global display

    #ran with virtual display to avoid captchas when using headless
    display = Display(visible=0, size=(1200, 1000))
    display.start()

    options = Options()
    options.add_argument("--enable-javascript")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1200x1000')
    options.add_argument('start-maximized')

    driver = webdriver.Chrome(options=options)

    print('Browser initialized')


def stop_and_shop(email, password):
    pass

def acme(email,password):
    pass



if __name__ == '__main__':

    arparser = argparse.ArgumentParser(description='Grocery Digital Coupons.')
    arparser.add_argument('--config', type=str, default='shoprite', help='Config section to read login from.')
    arparser.add_argument('--store', type=str, default='shoprite', nargs='?', help='Store to clip coupons [shoprite, acme, stop_and_shop].')
    arparser.add_argument('--user', type=str, nargs='?', help='Login username or read from config.ini.')
    arparser.add_argument('--password', type=str, nargs='?', help='Login password or read from config.ini.')
    args = arparser.parse_args()

    parser = RawConfigParser()
    parser.read('config.ini')

    # Get email/password from config file
    email = os.getenv('email') or args.user or parser.get(args.config, 'email')
    password = os.getenv('password') or args.password or parser.get(args.config, 'password')

    if args.store == 'shoprite':
        shoprite(email, password)
    elif args.store == 'stop_and_shop':
        stop_and_shop(email, password)
    elif args.store == 'acme':
        acme(email, password)
    elif args.store == 'help':
        print('Usage: coupons.py [shoprite | acme | stop_and_shop]')
    else:
        print('Unknown store: ' + args.store)
