#!/bin/bash

if [[ $CKAN__PLUGINS == *"harvest"* ]]; then
      echo "Harvest db upgrade"
      ckan --config=$CKAN_INI db upgrade -p harvest
else
   echo "Not configuring harvest"
fi