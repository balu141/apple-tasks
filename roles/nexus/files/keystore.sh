#!/bin/bash


location=$1
password=`echo $2 | tr -d '[[:space:]]'`
java_location=$3

$java_location/keytool -genkey -noprompt \
-alias nexus-alias \
-keystore $location \
-keyalg RSA \
-keypass $password \
-storepass $password \
-dname "CN=artl.apple.com, OU=ID, O=artl, L=Bala, S=SWamy, C=GB"
