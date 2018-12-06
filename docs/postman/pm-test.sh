#!/bin/bash

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
counter=0
until $(curl --output /dev/null --silent --head --insecure --fail $STATUS_CHECK_URL); do
    echo "Waiting."
    ((counter++))
    sleep 5
    if  ((counter >= 60)); then
        echo "no response from ${STATUS_CHECK_URL} for 5 min"
        exit 1
    fi
done

run_and_check_exit_code "node scenario-test.js $COLLECTION_NAMES $ENVIRONMENT $PM_API_KEY"
