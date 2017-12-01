# Grocery Digital Coupon Automation

## Quick Start

1. Install the required software for [Python](https://www.python.org/downloads/) *(version 2.7)*.
2. Download the [pip](https://bootstrap.pypa.io/get-pip.py) script and install it with `python get-pip.py`
3. Run the setup script `python setup.py`
4. Run the web app with `python web.py`

*If on Linux, set the permissions of `chromedriver` to executable.*

## Usage

The script only supports [Shoprite](http://www.shoprite.com) and [Stop and Shop](http://www.stopandshop.com/) for now:

1. `python grocery_coupons.py shoprite`
2. `python grocery_coupons.py shop_and_shop`

## Dependencies
[Selenium](http://selenium-python.readthedocs.io/index.html)
[Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Hosting on Heroku

[gunicorn](http://gunicorn.org/) is the web server used for hosting on Heroku. Since a global variable is used to maintain status updates during processing, you'll need to set the number of [workers](http://docs.gunicorn.org/en/stable/settings.html#worker-processes) to `1`. Additionally, you should turn on [session affinity](https://devcenter.heroku.com/articles/session-affinity).

1. In Heroku, the set environment config variable `WEB_CONCURRENCY` to `1`. Alternatively, edit [Procfile](https://github.com/primaryobjects/grocery-digital-coupons/blob/web/Procfile) and set the line to `web: gunicorn web:app --log-file - -w 1`

2. Enable session affinity: `heroku features:enable http-session-affinity`
  
## More Info

### What are grocery digital coupons?
My local grocery stores - [ShopRite](http://www.shoprite.com) and [Stop and Shop](http://www.stopandshop.com/) - have a "digital coupon" feature, by which you can log onto their website and add "digital" coupons to your store loyalty card. If you buy a product and the corresponding digital coupon is added to your loyalty card, you'll save some money upon checkout.

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

### How do I launch the script?
Launch it with an argument for the store you want to access. Right now the two options are:

1. `python grocery_coupons.py shoprite`
2. `python grocery_coupons.py shop_and_shop`


## What's next?

The script only supports ShopRite and Stop and Shop for now, so the addition of other grocery stories would be great. It appears that [Giant's website](https://giantfoodstores.com/) looks similar to Stop and Shop since they're [owned by the same company](https://en.wikipedia.org/wiki/Stop_%26_Shop/Giant-Landover), so I assume this would be easy to integrate.

## Contact
You can contact the author, Sheil Naik, [on Twitter](http://www.twitter.com/sheilnaik).
