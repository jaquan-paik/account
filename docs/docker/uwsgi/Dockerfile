FROM ridibooks/python:bootstrap-django-2018.06.06

RUN apt-get update
RUN apt-get install -y ca-certificates
RUN apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip3.6 install -U pip pipenv

# Add source
ADD . /htdocs/www/
RUN chown -R www-data.www-data /htdocs/www/

# Install dependencies
ARG ENVIRONMENT
RUN make global-python-package-install-$ENVIRONMENT
ADD ./docs/docker/uwsgi/$ENVIRONMENT/account.ini /etc/uwsgi/account.ini

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/account.ini"]
