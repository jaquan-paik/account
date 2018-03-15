FROM ridibooks/python:bootstrap-django-2017.02.01

VOLUME ["/var/local/nginx/sockets"]

# Add source
ADD . /htdocs/www/
RUN chown -R www-data.www-data /htdocs/www/

# Install dependencies
RUN pip3.6 install -r /htdocs/www/docs/requirements/development.txt

# Configure
RUN mkdir -pv \
        /htdocs/www/logs \
        /htdocs/www/logs/uwsgi \
        /var/local/nginx \
        /var/local/nginx/sockets

RUN chown -R www-data:www-data /var/local/nginx/sockets \
        && chown -R www-data:www-data /htdocs/www/logs

ARG SITE
ADD ./docs/docker/development/account/$SITE/uwsgi.ini /etc/uwsgi/

RUN python3.6 /htdocs/www/src/manage.py $SITE collectstatic --noinput

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
