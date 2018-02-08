FROM ridibooks/python:bootstrap-django-2017.02.01

# Add source
ADD . /htdocs/www/
RUN chown -R www-data.www-data /htdocs/www/

# Install dependencies
RUN pip3.6 install -r /htdocs/www/docs/requirements/production.txt

# Configure
ARG SITE
ADD ./docs/docker/library/$SITE/uwsgi.ini /etc/uwsgi/

EXPOSE 8000 8001 8002

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
