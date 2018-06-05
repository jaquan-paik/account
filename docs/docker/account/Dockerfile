FROM ridibooks/python:bootstrap-django-2018.06.06

# Add source
ADD . /htdocs/www/
RUN chown -R www-data.www-data /htdocs/www/

# Install dependencies
ARG ENVIRONMENT
RUN pip3.6 install -r /htdocs/www/docs/requirements/$ENVIRONMENT.txt

ADD ./docs/docker/account/$ENVIRONMENT/uwsgi/www.ini /etc/uwsgi/www.ini

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/www.ini"]
