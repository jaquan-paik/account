#!/bin/bash

function gracefulShutdown {
    /usr/local/bin/celery multi stopwait worker
}
trap gracefulShutdown SIGTERM

if [ "$ENABLE_BEAT" == "1" ]
then
    /usr/local/bin/celery beat \
        -A $CELERY_APP_NAME \
        -b $CELERY_BROKER_URL \
        --workdir=/htdocs/www/src \
        --loglevel=INFO
else
    /usr/local/bin/celery worker \
        -A $CELERY_APP_NAME \
        $BEAT_OPT \
        -Q $CELERY_QUEUE \
        -b $CELERY_BROKER_URL \
        -c $CELERY_WORKER_COUNT \
        --workdir=/htdocs/www/src \
        --loglevel=INFO
fi
