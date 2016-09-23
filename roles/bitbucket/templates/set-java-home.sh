#!/usr/bin/env bash

if [ -z "$JAVA_HOME" ]; then
    export JAVA_HOME=
fi

if [ -n "$JAVA_HOME" ] && [ -x "$JAVA_HOME/bin/java" ];  then
    # found java executable in JAVA_HOME
    JAVA_BINARY="$JAVA_HOME/bin/java"
else
    if [ -n "$JAVA_HOME" ]; then
        # invalid JAVA_HOME set
        echo "-------------------------------------------------------------------------------"
        echo "  JAVA_HOME \"$JAVA_HOME\" does not point to a valid Java home directory."
        echo "-------------------------------------------------------------------------------"
    else
        # JAVA_HOME not set
        java_type=$(type -p java)
        if [ -n java_type ]; then
            # java is in PATH
            JAVA_BINARY=java
        fi
    fi
fi

if [ "$JAVA_BINARY" ]; then
    JAVA_VERSION=$("$JAVA_BINARY" -version 2>&1 | awk -F '"' '/version/ {print $2}')
    if [ "$JAVA_VERSION" \< "1.8" ]; then
        echo "-------------------------------------------------------------------------------"
        echo "  Atlassian Bitbucket does not support Java $JAVA_VERSION."
        echo "  Please start the product with Java 8 or greater."
        echo "-------------------------------------------------------------------------------"
        exit 1
    fi
fi