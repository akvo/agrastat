#!/bin/sh

case "$CKAN__PLUGINS" in
  *"harvest"*)
    echo "Harvest db upgrade"
    ckan --config="$CKAN_INI" db upgrade -p harvest
    ;;
  *)
    echo "Not configuring harvest"
    ;;
esac