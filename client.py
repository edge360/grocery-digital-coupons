# Install dependencies.
import subprocess
subprocess.call(['python3', 'setup.py'])

import sys
import os
import grocery_coupons
from configparser import RawConfigParser

def onStatus(status):
    print(status['message'])
    if 'error' in status:
        print(status['error'])

if __name__ == "__main__":
    parser = RawConfigParser()
    parser.read('config.ini')

    # Get email/password from config file
    email = os.getenv('email') or parser.get('shoprite', 'email')
    password = os.getenv('password') or parser.get('shoprite', 'password')
    delay = 10

    if len(sys.argv) > 1:
        if sys.argv[1] == 'shoprite':
            grocery_coupons.shoprite(email, password, delay, onStatus)
        elif sys.argv[1] == 'stop_and_shop':
            grocery_coupons.stop_and_shop(email, password, delay, onStatus)
        else:
            print('Unknown site [' + sys.argv[1] + ']')
    else:
        print('Usage: client.py [shoprite | stop_and_shop]')