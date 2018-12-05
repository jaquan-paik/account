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
until $(curl --output /dev/null --silent --head --insecure --fail https://account.dev.ridi.io/ridi/complete); do
    echo "Waiting."
    sleep 5
done

run_and_check_exit_code "node scenario-test.js $COLLECTION_NAMES $PM_API_KEY"
