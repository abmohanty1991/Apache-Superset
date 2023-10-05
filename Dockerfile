
FROM apache/superset:latest-dev

USER root

#RUN pip install psycopg2

ENV ADMIN_EMAIL admin@org.com
ENV ADMIN_USERNAME admin
ENV ADMIN_PASSWORD admin
ENV FLASK_APP superset

COPY config.py /app/superset/config.py
COPY superset_config.py /app/superset/superset-config.py
COPY middleware.py /app/superset/middleware.py
COPY . /app/

# ENV SUPERSET_CONFIG_PATH /app/superset/config.py

# COPY superset-init.sh /app/superset-custom.sh
COPY superset-custom.sh /app/superset-custom.sh

RUN chmod +x /app/superset-custom.sh
RUN chmod +x /app/config.py
RUN chmod +x /app/superset/superset-config.py
RUN chmod +x /app/superset/middleware.py



USER superset

# echo "Creating Admin user ${ADMIN_USERNAME} email ${ADMIN_EMAIL}"
# superset fab create-admin --username "$ADMIN_USERNAME" --firstname Superset --lastname Admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"
# RUN superset superset fab create-admin --username admin --firstname admin --lastname admin --email admin --password admin

# Upgrading Superset metastore
# echo "Upgrading DB"
# RUN superset db upgrade

# Init Superset, set up roles and permissions
# RUN superset init
# CMD ["superset superset fab create-admin --username admin --firstname admin --lastname admin --email admin --password admin"]
ENTRYPOINT [ "/app/superset-custom.sh" ]
