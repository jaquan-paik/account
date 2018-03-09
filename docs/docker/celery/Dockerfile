FROM ridibooks/python:bootstrap-django-2017.02.01

# Add source
ADD . /htdocs/www/

# Install dependencies
RUN pip3.6 install -r /htdocs/www/docs/requirements/production.txt

CMD ["/htdocs/www/docs/docker/celery/startup.sh"]
