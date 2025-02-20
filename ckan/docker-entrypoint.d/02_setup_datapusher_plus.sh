#!/bin/sh

case "$CKAN__PLUGINS" in
  *"datapusher_plus"*)
    echo "datapusher_plus db upgrade"
    ckan --config="$CKAN_INI" db upgrade -p datapusher_plus
    ;;
  *)
    echo "Not configuring datapusher_plus"
    ;;
esac