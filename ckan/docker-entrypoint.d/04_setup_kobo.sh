#!/bin/bash

if [[ $CKAN__PLUGINS == *"kobo"* ]]; then
      echo "Kobo db upgrade"
      ckan --config=$CKAN_INI db upgrade -p kobo
else
   echo "Not configuring kobo"
fi
