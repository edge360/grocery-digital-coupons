FROM selenium/standalone-chrome
USER root

WORKDIR /opt/grocery_coupons
ADD . /opt/grocery_coupons

RUN apt-get update && apt-get install -y python3-distutils xvfb python3-pip
RUN pip install pipreqs && pipreqs --force . && pip install -r requirements.txt

ENTRYPOINT ["python3", "-u", "grocery_coupons.py"]
