FROM selenium/standalone-chrome

WORKDIR /opt/grocery_coupons

RUN apt-get update && apt-get install -y python3-distutils xvfb python3-pip
RUN pip install pipreqs && pipreqs --force . && pip install 

ADD . /opt/grocery_coupons

ENTRYPOINT ["python3", "-u", "grocery_coupons.py"]
