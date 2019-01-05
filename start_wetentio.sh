#!/bin/bash

. myvenv/bin/activate
sudo python manage.py runserver ec2-18-218-159-5.us-east-2.compute.amazonaws.com:80 > /dev/null 2>&1 &

