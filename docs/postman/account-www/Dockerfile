FROM ridibooks/python:bootstrap-django-2018.11.12.2

ADD . /htdocs/www
WORKDIR /htdocs/www
CMD bash ./docs/docker/wait_for_it.sh 'mysqladmin ping -h account-mariadb -u root -proot' & make docker-all