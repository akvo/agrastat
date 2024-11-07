#!/bin/sh

# Remove 'https://' from CKAN_SITE_URL if present
CKAN_SITE_URL=${CKAN_SITE_URL#https://}

cat << EOF > /traefik-config/dynamic.yml
http:
  routers:
    ckan-service-router-80:
      rule: "Host(\`${CKAN_SITE_URL}\`)"
      service: ckan-service
      entrypoints: web
      middlewares:
        - redirect-to-https

    ckan-service-router-443:
      entrypoints:
        - websecure
      rule: "Host(\`${CKAN_SITE_URL}\`)"
      service: ckan-service
      tls:
        certResolver: myresolver

  middlewares:
    redirect-to-https:
      redirectScheme:
        scheme: "https"
        permanent: true

  services:
    ckan-service:
      loadBalancer:
        servers:
          - url: "http://ckan:5000"

EOF