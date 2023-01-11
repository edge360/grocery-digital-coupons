FROM python:3.9.4-buster

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update

RUN apt-get install -yqq unzip
RUN apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN apt-get install -y python3-distutils xvfb python3-pip
RUN pip install pipreqs
COPY . /app

WORKDIR /app
RUN pipreqs --force .

RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]

ENTRYPOINT ["python3", "-u", "grocery_coupons.py"]
