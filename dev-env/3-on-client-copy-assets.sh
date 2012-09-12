#!/bin/bash

FILEPATH=`readlink -f $0`
BASEDIR=`dirname $FILEPATH`
TMPDIR=$BASEDIR/tmp

# Copy db folder from tmp folder with (external owner) to a folder owned by the vagrant user
cp -r $TMPDIR/db /var/akvo/akvo/mediaroot/db
sudo chown -R vagrant:vagrant /var/akvo/akvo/mediaroot/db
sudo chmod -R 744 /var/akvo/akvo/mediaroot/db
