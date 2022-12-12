#!/bin/bash

# cwd and set virtualenv
cd /var/app
. bin/activate

gunicorn main:main
