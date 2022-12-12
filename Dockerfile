FROM python:3.8.16-slim-bullseye

##############################################################################
# OS Updates and Python packages
##############################################################################
RUN apt-get update && \
    apt-get install -y apt-transport-https

##############################################################################
# Configure application
##############################################################################


WORKDIR /var/app

RUN pip3 install virtualenv
RUN virtualenv /var/app
RUN /var/app/bin/pip install setuptools --upgrade

##############################################################################
# Copy app and install requirements
##############################################################################
COPY requirements.txt /var/app/requirements.txt
RUN  /var/app/bin/pip install -r /var/app/requirements.txt
RUN pip3 install --upgrade googleapis-common-protos
ADD . /var/app

##############################################################################
# Run start.sh script when the container starts.
# Note: If you run migrations etc outside CMD, envs won't be available!
##############################################################################
RUN chmod +x /var/app/run-server.sh
ENTRYPOINT ["/var/app/run-server.sh"]

EXPOSE 8080