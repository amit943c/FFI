# pull official base image
# FROM python:3.8-slim-buster

RUN apt-get -y update
# RUN apt-get install -y git
# install google chrome
RUN apt-get install wget gnupg2 -y
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable

ARG CHROME_VERSION="92.0.4515.107-1"
RUN wget --no-verbose -O /tmp/chrome.deb http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

#extra dependencies for chromedriver
# install chromedriver
ARG CHROME_DRIVER_VERSION="92.0.4515.107"
RUN apt-get install -yqq unzip
RUN apt-get install curl -y
RUN apt-get install -y build-essential libssl-dev libffi-dev
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
RUN unzip -o /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver
#RUN curl https://chromedriver.storage.googleapis.com/75.0.3770.140/chromedriver_linux64.zip -o /usr/local/bin/chromedriver.zip
#RUN unzip /usr/local/bin/chromedriver.zip -d /usr/local/bin/


#RUN export PATH=$PATH:/usr/local/bin
#RUN ln -s /usr/local/bin/chromedriver /usr/bin


# ENV display port to avoid crash
ENV DISPLAY=:99

#tessract installation
RUN apt-get install tesseract-ocr -y

RUN apt-get update && apt-get install -y git


# ENV work directory
WORKDIR /var/epfo

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/var/epfo"

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# ENV FLASK_APP=app/aadhaar_lite_crawlers/uidai_gov_in_provider/run_server.py
# ENV FLASK_ENV=development

# EXPOSE 5432
# CMD flask db init && flask db migrate  && flask db upgrade && python app/rmq/aadhar_lite_publisher.py
# CMD python app/rmq/aadhaar_lite_consumer.py
# CMD  flask run
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

RUN chmod +x /var/epfo/run-server.sh

ENTRYPOINT ["/var/epfo/run-server.sh"]
EXPOSE 8080
