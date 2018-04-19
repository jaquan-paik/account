FROM ridibooks/python:bootstrap-django-2017.02.01

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

ADD ./docs/docker/account/$ENVIRONMENT/uwsgi/admin.ini /etc/uwsgi/admin.ini
ADD ./docs/docker/account/$ENVIRONMENT/uwsgi/www.ini /etc/uwsgi/www.ini

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/www.ini"]
