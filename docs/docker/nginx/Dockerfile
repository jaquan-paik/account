FROM nginx:stable

COPY docs/prod/nginx/conf/nginx.conf /etc/nginx/nginx.conf

RUN touch /var/run/nginx.pid && \
  chown -R www-data:www-data /var/run/nginx.pid && \
  chown -R www-data:www-data /var/cache/nginx

ARG SITE
COPY docs/prod/nginx/conf/$SITE.conf /etc/nginx/conf.d
