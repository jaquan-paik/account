FROM nginx:stable

COPY ./docs/dev/nginx /etc/nginx/conf.d
COPY ./docs/dev/cert /etc/nginx/cert/

RUN touch /var/run/nginx.pid && \
  chown -R www-data:www-data /var/run/nginx.pid && \
  chown -R www-data:www-data /var/cache/nginx

EXPOSE 80 80
EXPOSE 443 443