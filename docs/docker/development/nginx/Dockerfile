FROM nginx:stable

COPY docs/docker/development/nginx/conf/nginx.conf /etc/nginx/nginx.conf

VOLUME ["/var/local/nginx/sockets"]

RUN touch /var/run/nginx.pid && \
  chown -R www-data:www-data /var/run/nginx.pid && \
  chown -R www-data:www-data /var/cache/nginx

ARG SITE
COPY docs/docker/development/nginx/conf/$SITE.conf /etc/nginx/conf.d
