#!/bin/bash

if [[ $CKAN__PLUGINS == *"contact"* ]]; then
   echo "Contact in src"
   ckan config-tool "$CKAN_INI" "ckanext.contact.mail_to=$CKANEXT__CONTACT__MAIL_TO"
else
   echo "Not configuring contact"
fi
