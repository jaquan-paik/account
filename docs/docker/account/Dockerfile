FROM ridibooks/python:bootstrap-django-2017.02.01

VOLUME ["/var/local/nginx/sockets"]

# Add source
ADD . /htdocs/www/
RUN chown -R www-data.www-data /htdocs/www/

# Install dependencies
ARG ENVIRONMENT
RUN pip3.6 install -r /htdocs/www/docs/requirements/$ENVIRONMENT.txt

# Configure
RUN mkdir -pv \
        /var/local/nginx \
        /var/local/nginx/sockets

RUN chown -R www-data:www-data /var/local/nginx/sockets

ARG SITE
ADD ./docs/docker/account/$ENVIRONMENT/$SITE/uwsgi.ini /etc/uwsgi/

RUN python3.6 /htdocs/www/src/manage.py $SITE collectstatic --noinput

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
