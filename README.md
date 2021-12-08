# Grocery Digital Coupon Automation

Automatically clip digital coupons on food store web sites!

*Also available as a [web app](https://github.com/primaryobjects/grocery-digital-coupons/tree/web).*

## Quick Start

`git clone https://github.com/edge360/grocery-digital-coupons.git`

`docker build -t grocery-digital-coupons /opt/grocery-digital-coupons`

Edit `config.ini` to include your login information.

`docker run --rm grocery-digital-coupons:latest <arguments>`

Entrypoint: client.py

## Usage

The script supports [Shoprite](http://www.shoprite.com), [ACME](https://www.acmemarkets.com), and [Stop and Shop](http://www.stopandshop.com/).

1. `python3 client.py`
2. `python3 client.py --store shoprite --user username --password password`

The full command-line arguments are shown below.

```text
usage: client.py [-h] [--config CONFIG] [--store [STORE]] [--user [USER]]
                 [--password [PASSWORD]]

Grocery Digital Coupons.

optional arguments:
  --help                  Show this help message and exit
  --config CONFIG         Config section to read login from.
  --store [STORE]         Store to clip coupons [shoprite, acme, stop_and_shop].
  --user [USER]           Login username or read from config.ini.
  --password [PASSWORD]   Login password or read from config.ini.
  --notify [000-000-0000] Phone number to send a text message summary of results.
```

## Dependencies
[Selenium](http://selenium-python.readthedocs.io/index.html)
[Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

**Helpful Commands**

```bash
C:\Users\YOUR_USER_NAME\AppData\Local\Programs\Python\Python38-32\python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
C:\Users\YOUR_USER_NAME\AppData\Local\Programs\Python\Python38-32\python client.py
alias coupons="cd ~/Documents/grocery-digital-coupons && python3 client.py --store shoprite --config shoprite1 && python3 client.py --store shoprite --config shoprite2"
```

## More Info

### What are grocery digital coupons?
My local grocery stores - [ShopRite](http://www.shoprite.com), [ACME](https://www.acmemarkets.com), and [Stop and Shop](http://www.stopandshop.com/) - have a "digital coupon" feature, by which you can log onto their website and add "digital" coupons to your store loyalty card. If you buy a product and the corresponding digital coupon is added to your loyalty card, you'll save some money upon checkout.

### So what's the problem?
The problem is that the digital coupons have to be added manually. If you buy something and the coupon isn't present on your loyalty card at the time of checkout, you won't get the discount.

### Wow, that's dumb.
Yep.

### What's the solution?
The script adds *all* digital coupons to your card each week. Then, you'll automatically get the discount when you buy a product without having to do any legwork.

### So how does the script work?
The script uses [Selenium](http://selenium-python.readthedocs.io/index.html) to launch the grocery store's website, login with your loyalty card information, and automatically add each available coupon to your card.

### Where is my login information saved?
The file `config_example.ini` contains an example of how to set up the config file. This file will need to be renamed `config.ini` in order for the script to work.

## What's next?

The script supports ShopRite, Acme, and Stop and Shop for now, so the addition of other grocery stories would be great. It appears that [Giant's website](https://giantfoodstores.com/) looks similar to Stop and Shop since they're [owned by the same company](https://en.wikipedia.org/wiki/Stop_%26_Shop/Giant-Landover), so I assume this would be easy to integrate.

## Contact

You can contact the author, Sheil Naik, [on Twitter](http://www.twitter.com/sheilnaik).
