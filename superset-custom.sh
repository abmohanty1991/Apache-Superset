#! /bin/bash

# create Admin user. We can read this value from environment or from anywhere
echo "Creating Admin user ${ADMIN_USERNAME} email ${ADMIN_EMAIL}"
superset fab create-admin --username "$ADMIN_USERNAME" --firstname Superset --lastname Admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"

# Upgrading Superset metastore
echo "Upgrading DB"
superset superset db upgrade

# Init Superset, set up roles and permissions
superset superset init

# Starting server
/bin/sh -c /usr/bin/run-server.sh