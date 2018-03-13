FROM nginx:stable

COPY docs/docker/nginx/conf/nginx.conf /etc/nginx/nginx.conf

VOLUME ["/var/local/nginx/sockets"]

RUN touch /var/run/nginx.pid && \
  chown -R www-data:www-data /var/run/nginx.pid && \
  chown -R www-data:www-data /var/cache/nginx

ARG ENVIRONMENT
COPY docs/docker/nginx/$ENVIRONMENT/www.conf /etc/nginx/conf.d
#COPY docs/docker/nginx/$ENVIRONMENT/admin.conf /etc/nginx/conf.d
