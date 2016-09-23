#!/bin/sh
     pid=`ps aux | grep nexus-{{ nexus_iq_old_version }} | grep -v grep | awk '{print $2}'`
     kill $pid