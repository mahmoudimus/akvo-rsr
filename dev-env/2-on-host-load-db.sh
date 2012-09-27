#!/bin/bash

SSH_USER=daniel
DB_USER=rsruser
DB_PASSWORD=u5r6vKSBwUxE4EMB

# E.g.
# SSH_USER=daniel
# DB_USER=daniel
# DB_PASSWORD=karlsson

BASEDIR="$(dirname "$0")"
TMPDIR=$BASEDIR/tmp
ssh $SSH_USER@test.akvo.org -p 2270 "mysqldump -u $DB_USER -p$DB_PASSWORD rsrdb_rc | gzip" > $TMPDIR/rsr_mysql_db.sql.gz
ssh -i $BASEDIR/ssh_keys/vagrant vagrant@33.33.33.15 -p 22 'gunzip | mysql -u rsr-user -plake rsr' < $TMPDIR/rsr_mysql_db.sql.gz