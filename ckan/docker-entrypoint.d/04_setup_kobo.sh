#!/bin/bash

if [[ $CKAN__PLUGINS == *"kobo"* ]]; then
      echo "Kobo db upgrade"
      ckan --config=$CKAN_INI db upgrade -p kobo
      # check if kobo in src or src_extensions
      if [ -d /srv/app/src/ckanext-kobo ]; then
         echo "Kobo in src"
         pip install -r /srv/app/src/ckanext-kobo/requirements.txt
      else
         echo "Kobo in src_extensions"
         pip install -r /srv/app/src_extensions/ckanext-kobo/requirements.txt
      fi
else
   echo "Not configuring kobo"
fi
