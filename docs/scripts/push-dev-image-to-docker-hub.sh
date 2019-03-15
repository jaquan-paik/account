#!/bin/bash
set -e

run_and_check_exit_code() {
    pids=""
    for command in "$@"; do
        eval $command &
        pids="$pids $!"
    done

    for p in $pids; do
        if wait $p; then
            echo "success"
        else
            echo "failure"
            exit 1
        fi
    done
}

run_and_check_exit_code "docker login -u $DOCKER_DEV_ID -p $DOCKER_DEV_PASSWORD"
run_and_check_exit_code "docker tag development/account/uwsgi:$TAG ridibooks/account-dev"
run_and_check_exit_code "docker push ridibooks/account-dev"
if [ $? -ne 0 ]; then
    echo "push fails"
    exit 1
fi
