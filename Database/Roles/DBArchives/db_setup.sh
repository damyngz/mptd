#!/usr/bin/env bash

# retuires environment var root_pw

#
# setup db root and admin user
#
./setup_db_root_user.sh $root_pw mptduser 127.0.0.1 mptdpassword
#
# setup database
#
mysql -u mptduser -pmptdpassword 2>/dev/null -e "create database mptd_finance;"