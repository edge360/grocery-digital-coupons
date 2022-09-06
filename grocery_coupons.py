#!/bin/python3
import os
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay.display import Display



driver = None
display = None

def coupons(email, password, store):

    #initialize browser and virt display
    initialize()

    if store == "shoprite":
        coupon_site = "https://www.shoprite.com/digital-coupon"
        coupon_app = "sr-digital-coupons"
    elif store == "pricerite":
        coupon_site = "https://www.priceritemarketplace.com/digital-coupon"
        coupon_app = "pricerite-digital-coupons"
    elif store ==  "fairway":
        coupon_sitee = "https://www.fairwaymarket.com/digital-coupon"
        coupon_app = "fairway-digital-coupons"
    elif store ==  "dearborn":
        coupon_site = "https://www.dearbornmarket.com/digital-coupon"
        coupon_app = "dearborn-digital-coupons"
    elif store == "gourmet":
        coupon_site = "https://www.gourmetgarage.com/digital-coupon"
        coupon_app = "gourmet-digital-coupons"
    elif store == "tfg":
        coupon_site = "https://www.thefreshgrocer.com/digital-coupon"
        coupon_app = "tfg-digital-coupons"
    else:
        print("Invalid Store...")
        return

    try:
        print("Loading Page...")
        driver.get(coupon_site)
        wait = WebDriverWait(driver, 60)

        #find modal dialog and remove
        try:
            modal = driver.find_element(By.ID, "outside-modal")
            driver.execute_script("arguments[0].remove();", modal)
        except:
            pass

        wait.until(EC.element_to_be_clickable((By.ID, "AccountHeaderButton"))).click()


        print("Logging In...")
        wait.until(EC.element_to_be_clickable((By.ID, "Email"))).send_keys(email)
        driver.find_element(By.ID,'Password').send_keys(password)
        driver.find_element(By.ID,'Password').send_keys(Keys.RETURN)
        #check for successful login before proceeding
        time.sleep(1)

        try:
            print("Success...")
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, coupon_app)))
        except:
            print("Incorrect email or password")
            return

        #print("Loading All Coupons to page...")
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-default.btn-sm.ng-tns-c98-0.ng-star-inserted"))).click()
        #print("Clipping  Coupons...")
        clipped_count = 0
        coupons = driver.find_elements(By.CLASS_NAME, 'coupon-item-container')
        total_count = len(coupons)
        for coupon in coupons:
            coupon_name = coupon.find_element(By.CLASS_NAME, 'coupon-brand-name').text
            coupon_desc = coupon.find_element(By.CLASS_NAME, 'coupon-desc').text
            try:
                coupon.find_element(By.CLASS_NAME, 'available-to-clip.ng-star-inserted').click()
                print("Clipped: " + str(coupon_name) + " --- " + str(coupon_desc))
                clipped_count += 1
            except:
                #Already Clipped
                pass

        if not clipped_count:
            print("No New Coupons Clipped --- 0/" + str(total_count))
        else:
            print("Clipped " + str(clipped_count) + " new coupon(s) --- " + str(clipped_count) + "/" + str(total_count))


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



#def okay():
if __name__ == '__main__':
    arparser = argparse.ArgumentParser(description='Grocery Digital Coupons.')
    arparser.add_argument('--config', type=str, default='shoprite', help='Config section to read login from.')
    arparser.add_argument('--store', type=str, default='shoprite', nargs='?', help='Store to clip coupons [shoprite, acme, stop_and_shop].')
    arparser.add_argument('--user', type=str, nargs='?', help='Login username or read from config.ini.')
    arparser.add_argument('--password', type=str, nargs='?', help='Login password or read from config.ini.')
    args = arparser.parse_args()

    #all wake fern brands use same login/auth and same coupon db (applicable coupons may differ
    #shoprite, pricerite, fairway, dearborn market, gourmet garage, fresh grocer

    # Get email/password from ENV or cli
    email = os.getenv('EMAIL') or args.user
    password = os.getenv('PASSWORD') or args.password

    if args.store == 'shoprite':
        coupons(email, password, 'shoprite')
    elif args.store == 'pricerite':
        coupons(email, password, 'pricerite')
    elif args.store == 'fairway':
        coupons(email, password, 'fairway')
    elif args.store == 'dearborn':
        coupons(email, password, 'dearborn')
    elif args.store == 'gourmet':
        coupons(email, password, 'gourment')
    elif args.store == 'fresh':
        coupons(email, password, 'fresh')
    elif args.store == 'help':
        print('Usage: grocery_coupons.py [shoprite | pricerite | fairway | dearborn | gourmet | fresh]')
    else:
        print('Unknown store: ' + args.store)
