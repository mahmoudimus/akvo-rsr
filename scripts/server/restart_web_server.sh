#!/bin/bash

sudo service nginx stop
sudo service uwsgi stop
sleep 4s
sudo service uwsgi start
sudo service nginx start
