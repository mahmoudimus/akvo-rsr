#!/bin/bash

#FILEPATH=`readlink -f $0`
#BASEDIR=`dirname $FILEPATH`
#TMPDIR=$BASEDIR/tmp
TMPDIR="$(dirname "$0")/tmp"

# Grab db folder from test
rm -rf $TMPDIR/db
scp -P 2270 -r `whoami`@test.akvo.org:/var/www/akvo/db $TMPDIR/
