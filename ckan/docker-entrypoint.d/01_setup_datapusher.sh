#!/bin/sh

case "$CKAN__PLUGINS" in
    *datapusher*)
        # Datapusher settings have been configured in the .env file
        # Set API token if necessary
        if [ -z "$CKAN__DATAPUSHER__API_TOKEN" ]; then
            echo "Set up ckan.datapusher.api_token in the CKAN config file"

            # Generate a token and set it in the CKAN configuration file
            TOKEN=$(ckan -c "$CKAN_INI" user token add ckan_admin datapusher | tail -n 1 | tr -d '\t')
            ckan config-tool "$CKAN_INI" "ckan.datapusher.api_token=$TOKEN"
        else
            echo "CKAN__DATAPUSHER__API_TOKEN is already set: $CKAN__DATAPUSHER__API_TOKEN"
        fi
        ;;
    *)
        echo "Not configuring DataPusher"
        ;;
esac