EXPORT_SETTINGS_UID=esVgBLmJHSYCD8Sw9ucdpbb
ASSET_UID=acYmnomBXuW7Son6yEnRGd
KOBO_TOKEN=d3eb4da9f511ab5865f4b6573aadfdd28ab924de
KF_URL=eu.kobotoolbox.org
curl -L "https://${KF_URL}/api/v2/assets/${ASSET_UID}/export-settings/${EXPORT_SETTINGS_UID}/data.csv" \
  -H "Authorization: Token ${KOBO_TOKEN}" \
  -o data.csv
