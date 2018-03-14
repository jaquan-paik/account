FROM nginx:stable

ARG ENVIRONMENT
COPY docs/docker/$ENVIRONMENT/nginx/conf/nginx.conf /etc/nginx/nginx.conf

VOLUME ["/var/local/nginx/sockets"]

RUN touch /var/run/nginx.pid && \
  chown -R www-data:www-data /var/run/nginx.pid && \
  chown -R www-data:www-data /var/cache/nginx

ARG SITE
COPY docs/docker/$ENVIRONMENT/nginx/conf/$SITE.conf /etc/nginx/conf.d
