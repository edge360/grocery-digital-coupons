import os
import time
import argparse
import traceback
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay.display import Display



driver = None
display = None

def wakefern_coupons(email, password, store):

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
        driver.find_element(By.ID,'password').send_keys(password)
        driver.find_element(By.ID,'password').send_keys(Keys.RETURN)
        #check for successful login before proceeding
        time.sleep(1)

        try:
            print("Success...")
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, coupon_app)))
            #iframe = wait(driver).until(EC.presence_of_element_located((
            #    By.ID, coupon_app)))
            #driver.switch_to.frame(iframe)
            print("Switching to iframe...")
        except:
            print("Incorrect email or password")
            return

        print("Loading All Coupons to page...")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class^='btn btn-default btn-sm ng']"))).click()

        print("Clipping  Coupons...")
        clipped_count = 0
        coupons = driver.find_elements(By.CLASS_NAME, 'coupon-item-container')
        total_count = len(coupons)
        #####account for modal diaglogue for super coupon
        for coupon in coupons:
            coupon_name = coupon.find_element(By.CLASS_NAME, 'coupon-brand-name').text
            coupon_desc = coupon.find_element(By.CLASS_NAME, 'coupon-desc').text
            try:
                coupon.find_element(By.CLASS_NAME, 'available-to-clip.ng-star-inserted').click()
                print("Clipped: " + str(coupon_name) + " --- " + str(coupon_desc))
                clipped_count += 1
                try:
                    #print("Encountered super coupon dialog... clicking OKAY")
                    super_coupon_diag = driver.find_element(By.CLASS_NAME, 'btn.btn-outline-dark').click()
                    print("Clicked OKAY.. next coupon")
                except:
                    pass
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


    except:
        exit_with_failure("store error")

    """
    except Exception as e:
        #close/quit chrome and stop display on exception
        print(e)
        driver.close()
        driver.quit()
        display.stop()
    """



def albertsons_coupons(email, password, store):

    #initialize browser and virt display
    initialize()


    try:

        print("Loading Page...")
        driver.get('https://www.acmemarkets.com/foru/coupons-deals.html')
        wait = WebDriverWait(driver, 60)


        print(driver.title)
        print("Navigating to Login...")

        time.sleep(1)

        print("Logging In...")
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'form-control.sigin-email.body-m'))).send_keys(email)
        driver.find_element(By.CLASS_NAME,'form-control.sign-in-passwordfield.body-m').send_keys(password)
        driver.find_element(By.CLASS_NAME, 'form-control.sigin-email.body-m').send_keys(Keys.RETURN)

        time.sleep(5)
        print(driver.title)

        #accept cookies dialogue, then wait for fade out
        wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
        time.sleep(1)
        
        #wait for load button, continute to click until unavailable
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn.load-more')))
        print("Loading Coupons...")
        try:
            while ( load := driver.find_element(By.CLASS_NAME, 'btn.load-more') ):
                load.click()
                print("...")
                time.sleep(3)
        except:
            pass
            print("Loaded coupons")

        clipped_count = 0
        coupons = driver.find_elements(By.CLASS_NAME, 'col-12.col-sm-12.col-md-6.col-lg-4.coupon-grid-offer')
        total_count = len(coupons)
        for coupon in coupons:
            coupon_name = coupon.find_element(By.CLASS_NAME, 'grid-coupon-description-text-title').text
            coupon_desc = coupon.find_element(By.CLASS_NAME, 'grid-coupon-heading-offer-price').text
            try:
                coupon.find_element(By.CLASS_NAME, 'btn.grid-coupon-btn.btn-default').click()
                print("Clipped: " + str(coupon_name) + " --- " + str(coupon_desc))
                clipped_count += 1
            except:
                #Already Clipped
                pass

        if not clipped_count:
            print("No New Coupons Clipped --- 0/" + str(total_count))
        else:
            print("Clipped " + str(clipped_count) + " new coupon(s) --- " + str(clipped_count) + "/" + str(total_count))


        driver.close()
        driver.quit()
        display.stop()


    except Exception as e:
        #close/quit chrome and stop display on exception
        exit_with_failure("store error")
        print(e)
        driver.close()
        driver.quit()
        display.stop()

def exit_with_failure(message):
    traceback.print_exc()
    print_with_timestamp(message)
    sys.exit(1)

def print_with_timestamp(text):
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {text}')

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
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    print_with_timestamp('Browser initialized')


if __name__ == '__main__':

    arparser = argparse.ArgumentParser(description='Grocery Digital Coupons.')
    arparser.add_argument('--store', type=str, default='shoprite', nargs='?', help='Store to clip coupons [shoprite | pricerite | fairway | dearborn | gourmet | fresh]. Add arg or read from STORE env ')
    arparser.add_argument('--user', type=str, nargs='?', help='Login username. Add arg  or read from EMAIL env.')
    arparser.add_argument('--password', type=str, nargs='?', help='Login password. Add arg or read from PASSWORD env.')
    args = arparser.parse_args()

    #all wake fern brands use same login/auth and same coupon db (applicable coupons may differ)
    #shoprite, pricerite, fairway, dearborn market, gourmet garage, fresh grocer

    # Get email/password from ENV or cli
    email = os.getenv('EMAIL') or args.user
    password = os.getenv('PASSWORD') or args.password
    store = os.getenv('STORE') or args.store

    if store == 'shoprite':
        try:
            wakefern_coupons(email, password, 'shoprite')
        except:
            exit_with_failure("fail")
    elif store == 'pricerite':
        wakefern_coupons(email, password, 'pricerite')
    elif store == 'fairway':
        wakefern_coupons(email, password, 'fairway')
    elif store == 'dearborn':
        wakefern_coupons(email, password, 'dearborn')
    elif store == 'gourmet':
        wakefern_coupons(email, password, 'gourment')
    elif store == 'fresh':
        wakefern_coupons(email, password, 'fresh')
    elif store == 'help':
        print('Usage: grocery_coupons.py [shoprite | pricerite | fairway | dearborn | gourmet | fresh]')

    elif store == 'acme':
        try:
            albertsons_coupons(email, password, 'acme')
        except:
            exit_with_failure("fail")
    else:
        print('Unknown store: ' + args.store)


