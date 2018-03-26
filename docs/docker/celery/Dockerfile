FROM ridibooks/python:bootstrap-django-2017.02.01

# Add source
ADD . /htdocs/www/

# Install dependencies
ARG ENVIRONMENT
RUN pip3.6 install -r /htdocs/www/docs/requirements/$ENVIRONMENT.txt

CMD /htdocs/www/docs/docker/celery/startup.sh
