#!/bin/bash
command="$1"
until $(curl --output /dev/null --silent --head --insecure --fail https://account.dev.ridi.io/ridi/complete); do
    echo "Waiting."
    sleep 5
done
exec $command
