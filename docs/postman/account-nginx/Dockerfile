FROM nginx:stable

ADD ./docs/dev/nginx /etc/nginx/conf.d:ro
ADD ./docs/dev/cert /etc/nginx/cert/:ro

EXPOSE 80 80
EXPOSE 443 443