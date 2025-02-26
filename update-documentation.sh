#!/usr/bin/sh
set -eu

docker run -i --rm -v "$(pwd)/docs:/docs" \
    akvo/akvo-sphinx:20220525.082728.594558b make html

cp -r ./docs/build/html/* ./src/ckanext-agra-theme/ckanext/agra_theme/public/documentation