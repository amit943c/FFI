#!/bin/bash

# cwd and set virtualenv
cd /var/app
. bin/activate

gunicorn -b 0.0.0.0:8080 main:main
