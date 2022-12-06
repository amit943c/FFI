#!/bin/bash

# cwd and set virtualenv
cd /var/app
. bin/activate

python -u run_server.py
