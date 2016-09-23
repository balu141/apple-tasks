#!/bin/bash

nexus_keystore_password=$1
java_location=$2
nexus_lib_location=$3
util_list=$4

$java_location/java -cp  $nexus_lib_location/$util_list org.eclipse.jetty.util.security.Password $nexus_keystore_password 2>&1 | grep OBF | tr -d '\n'
