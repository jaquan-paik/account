#!/bin/bash

function gracefulShutdown {
    /usr/local/bin/celery multi stopwait worker --pidfile="/var/run/celery"
}
trap gracefulShutdown SIGTERM

if [ "$ENABLE_BEAT" == "1" ]
then
    BEAT_OPT="-B "
else
    BEAT_OPT=""
fi

/usr/local/bin/celery worker \
    -A $CELERY_APP_NAME \
    $BEAT_OPT \
    -Q $CELERY_QUEUE \
    -b $CELERY_BROKER_URL \
    -c $CELERY_WORKER_COUNT \
    --workdir=/htdocs/www/src \
    --logfile=/htdocs/www/logs/celery.log \
    --pidfile=/var/run/celery \
    --loglevel=INFO
