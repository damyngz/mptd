#!/usr/bin/env bash

#-------------------------------------------------------------
rootpw=$1
sqluser=$2
sqlhost=$3
sqlpw=$4


#install mysql------------------------------------------------
sudo apt install mysql-server -y 1>/dev/null
sudo apt install expect -y 1>/dev/null

#setup root user----------------------------------------------

SECURE_MYSQL=$(expect -c "
  set timeout 30
  spawn mysql_secure_installation
  expect \"Would you like to setup VALIDATE PASSWORD plugin?\"
  send \"\r\"
  expect \"Enter current password for root (enter for none):\"
  send \"\r\"
  expect \"New password: \"
  send \"$rootpw\r\"
  expect \"Re-enter new password: \"
  send \"$rootpw\r\"
  expect \"Change the root password?\"
  send \"n\r\"
  expect \"Remove anonymous users?\"
  send \"y\r\"
  expect \"Disallow root login remotely?\"
  send \"y\r\"
  expect \"Remove test database and access to it?\"
  send \"y\r\"
  expect \"Reload privilege tables now?\"
  send \"y\r\"
  expect eof
")

echo "$SECURE_MYSQL"
#sudo apt purge expect -y 1>/dev/null

#secure root user---------------------------------------------
# TODO decide switching root user plugin from auth_socket to mysql_native_password

#setup master user--------------------------------------------
sudo mysql -u root -e "create user $sqluser@$sqlhost identified by '$sqlpw'; grant all privileges on *.* to $sqluser;"

#-------------------------------------------------------------
echo "All Done"