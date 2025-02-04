FROM ckan/ckan-base:2.9.11


# Install any extensions needed by your CKAN instance
# See Dockerfile.dev for more details and examples

RUN apk add python3-dev py3-lxml geos-dev

RUN pip3 install -e 'git+https://github.com/ckan/ckanext-basiccharts.git@master#egg=ckanext-basiccharts'
RUN pip3 install -e 'git+https://github.com/keitaroinc/ckanext-visualize.git@master#egg=ckanext-visualize'
RUN pip3 install geojson shapely ckanext-pdfview
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-geoview.git@v0.2.0#egg=ckanext-geoview'
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-spatial.git@master#egg=ckanext-spatial'
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-hierarchy.git@master#egg=ckanext-hierarchy' && pip3 install -r ${APP_DIR}/src/ckanext-hierarchy/requirements.txt
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-harvest.git@v1.6.0#egg=ckanext-harvest' && pip3 install -r ${APP_DIR}/src/ckanext-harvest/requirements.txt
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-mapviews.git@master#egg=ckanext-mapviews'

# Copy custom initialization scripts
COPY docker-entrypoint.d/* /docker-entrypoint.d/

# Copy cron file
COPY cron.txt ${APP_DIR}/

# Import the crontab
RUN crontab ${APP_DIR}/cron.txt

# Apply any patches needed to CKAN core or any of the built extensions (not the
# runtime mounted ones)
COPY patches ${APP_DIR}/patches

RUN for d in $APP_DIR/patches/*; do \
        if [ -d $d ]; then \
            for f in `ls $d/*.patch | sort -g`; do \
                cd $SRC_DIR/`basename "$d"` && echo "$0: Applying patch $f to $SRC_DIR/`basename $d`"; patch -p1 < "$f" ; \
            done ; \
        fi ; \
    done

COPY setup/start_ckan.sh.override ${APP_DIR}/start_ckan.sh
