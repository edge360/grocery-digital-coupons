FROM python:3.8

WORKDIR /app

#install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable

#install Chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /app

#install xvfb for headless
RUN apt-get install -y xvfb

#install python dependencies
RUN pip install requests selenium flask flask_sslify PyJWT pyvirtualdisplay

ADD . /app

ENTRYPOINT ["python", "-u", "/app/client.py"]
