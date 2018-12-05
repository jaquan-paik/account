FROM mariadb:10.1

ADD ./docs/dev/settings/dump.sql /docker-entrypoint-initdb.d/dump.sql
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=account
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=test