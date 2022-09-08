# Grocery Digital Coupon Automation

Automatically clip digital coupons on food store web sites!

The script supports [ShopRite](http://www.shoprite.com), [PriceRite](https://www.priceritemarketplace.com/), [Fairway](https://www.fairwaymarket.com/). [Dearborn Markets](https://www.dearbornmarket.com/), [Gourmet Garage](https://www.gourmetgarage.com/), and [The Fresh Grocer](https://www.thefreshgrocer.com/).


## Quick Start

`git clone https://github.com/edge360/grocery-digital-coupons.git`

`docker build -t grocery-digital-coupons /opt/grocery-digital-coupons`

docker-compose.yml
 ```
 grocery-digital-coupons:
    image: pointccclx/grocery-digital-coupons:latest
    container_name: grocery-digital-coupons
    environment:
      - EMAIL=email@gmail.com
      - PASSWORD=password123
      - STORE=shoprite
```

## Usage

Pass arguments via CLI or ENV

docker
`docker run --rm grocery-digital-coupons:latest --user 'email@gmail.com' --password 'password123' --store 'shoprite'`

`docker run --rm grocery-digital-coupons:latest  --env EMAIL='email@gmail.com' --env PASSWORD='password123' --env STORE='shoprite'`

docker-compose

`docker-compose.yml up grocery-digital-coupons` 

The full command-line arguments are shown below.

```text
usage: grocery_coupons.py [-h] [--store [STORE]] [--user [USER]]
                 [--password [PASSWORD]]

optional arguments:
  --help                  Show this help message and exit
  --store [STORE]         Store to clip coupons [shoprite | pricerite | fairway | dearborn | gourmet | fresh].
  --user [USER]           Login username or read from ENV.
  --password [PASSWORD]   Login password or read from ENV.
```

## More Info

### What are grocery digital coupons?
My local grocery stores have a "digital coupon" feature, by which you can log onto their website and add "digital" coupons to your store loyalty card. If you buy a product and the corresponding digital coupon is added to your loyalty card, you'll save some money upon checkout.

### So what's the problem?
The problem is that the digital coupons have to be added manually. If you buy something and the coupon isn't present on your loyalty card at the time of checkout, you won't get the discount.

### Wow, that's dumb.
Yep.

### What's the solution?
The script adds *all* digital coupons to your card each week. Then, you'll automatically get the discount when you buy a product without having to do any legwork.

### So how does the script work?
The script uses [Selenium](http://selenium-python.readthedocs.io/index.html) to launch the grocery store's website, login with your loyalty card information, and automatically add each available coupon to your card.

### Where is my login information saved?
Your login information is passed via command line when you call the script or thru environmental variables set when you run the docker image.

## What's next?

The script was re-written for Docker support and to target Wakefern brands which include ShopRite, PriceRite, Fairway. Dearborn Markets, Gourmet Garage, and The Fresh Grocer for now. All of these brands appear to utilize the same login/auth and coupon DB in some respect, some coupons may only be available via clipping with certain stores. I would like to expand these at some point to other local stores including ACME/Albertsons, etc... 
