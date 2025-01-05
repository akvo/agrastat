#!/bin/bash

if [ "$CKAN__TRACKING_ENABLED" ] ; then
   echo "Set up ckan.tracking_enabled in the CKAN config file"
   ckan config-tool $CKAN_INI "ckan.tracking_enabled = $CKAN__TRACKING_ENABLED"
else
   echo "Not configuring Site Tracking"
fi
