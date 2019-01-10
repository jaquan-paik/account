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

curl -X POST --data-urlencode "payload={\"text\": \"[Account][$ENVIRONMENT - $TAG] 배포가 시작됩니다.\nRepo: https://github.com/ridi/account\"}" $SLACK_DEPLOY_HOOK
# Deploy
if [ "$ENVIRONMENT" = staging ]; then
run_and_check_exit_code "ecs-cli compose --cluster account-staging-cluster --project-name account-staging-www -f docs/docker/compose/account.yml service up --timeout 1200"
else
run_and_check_exit_code "ecs-cli compose --cluster account-cluster --project-name account-www -f docs/docker/compose/account.yml service up --timeout 1200" \
                        "ecs-cli compose --cluster account-cluster --project-name account-cron -f docs/docker/compose/cron.yml service up --timeout 1200"
fi

if [ $? -ne 0 ]; then
    echo "deploy fails"
    exit 1
fi


curl -X POST --data-urlencode "payload={\"text\": \"[Account][$ENVIRONMENT - $TAG] 배포가 완료되었습니다.\nRepo: https://github.com/ridi/account\"}" $SLACK_DEPLOY_HOOK

