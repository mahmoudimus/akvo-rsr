#!/bin/bash

FILEPATH=`readlink -f $0`
BASEDIR=`dirname $FILEPATH`
APPDIR=$BASEDIR/akvo

python $APPDIR/manage.py runserver 1337