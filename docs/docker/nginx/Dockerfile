FROM nginx:stable

ARG ENVIRONMENT
COPY docs/docker/nginx/$ENVIRONMENT/conf/nginx.conf /etc/nginx/nginx.conf

RUN touch /var/run/nginx.pid && \
  chown -R www-data:www-data /var/run/nginx.pid && \
  chown -R www-data:www-data /var/cache/nginx

COPY docs/docker/nginx/$ENVIRONMENT/conf/account.conf /etc/nginx/conf.d
