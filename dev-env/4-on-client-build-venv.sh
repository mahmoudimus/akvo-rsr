#!/bin/bash

FILEPATH=`readlink -f $0`
BASEDIR=`dirname $FILEPATH`

VENVDIR=$BASEDIR/../venv
REQDIR=$BASEDIR/../scripts/deployment/pip/requirements

# Create virtualenv
if [ ! -d "$VENVDIR" ]; then
  echo "Builing new virtualenv"
  virtualenv -q $VENVDIR -p `which python2.7`
else
  echo "Clear and rebuild existing virtualenv"
  virtualenv -q $VENVDIR --clear
fi

pip install -E $VENVDIR -r $REQDIR/0_system.txt
pip install -E $VENVDIR -r $REQDIR/1_deployment.txt
pip install -E $VENVDIR -r $REQDIR/2_rsr.txt
pip install -E $VENVDIR -r $REQDIR/3_testing.txt
pip install -E $VENVDIR -r $REQDIR/4_ci.txt