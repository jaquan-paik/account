FROM ridibooks/python:bootstrap-django-2017.02.01

# Add source
ADD . /htdocs/www/

RUN mkdir -pv \
        /htdocs/www/logs \
        && chown -R www-data:www-data /htdocs/www/logs

# Install dependencies
RUN pip3.6 install -r /htdocs/www/docs/requirements/production.txt

ARG ENVIRONMENT
CMD /htdocs/www/docs/docker/$ENVIRONMENT/celery/startup.sh
