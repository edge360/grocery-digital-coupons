FROM selenium/standalone-chrome
USER root

WORKDIR /opt/grocery-digital-coupons
ADD . /opt/grocery-digital-coupons

RUN apt-get update && apt-get install -y python3-distutils xvfb python3-pip
RUN pip install pipreqs && pipreqs --force . && pip install -r requirements.txt

USER 1200
ENTRYPOINT ["python3", "-u", "grocery_coupons.py"]
