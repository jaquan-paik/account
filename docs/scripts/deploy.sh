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


# Set environment
if [ "$1" = development ]; then

export ENVIRONMENT=development
export ECR_REPO_URL=$DEV_ACCOUNT_ECR
export AWS_ACCESS_KEY_ID=$DEV_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$DEV_AWS_SECRET_ACCESS_KEY
export TAG=${TRAVIS_COMMIT::8}

elif [ "$1" = staging ]; then

export ENVIRONMENT=staging
export ECR_REPO_URL=$STAGING_ACCOUNT_ECR
export AWS_ACCESS_KEY_ID=$STAGING_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$STAGING_AWS_SECRET_ACCESS_KEY
export TAG=${TRAVIS_COMMIT::8}

else

export ENVIRONMENT=production
export ECR_REPO_URL=$PROD_ACCOUNT_ECR
export AWS_ACCESS_KEY_ID=$PROD_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$PROD_AWS_SECRET_ACCESS_KEY
export TAG=$TRAVIS_TAG

fi


# Prepare build
make ci-settings ns=$ENVIRONMENT

$(aws ecr get-login --no-include-email --region=$AWS_DEFAULT_REGION)

docker pull ridibooks/python:bootstrap-django-2017.02.01 & \
docker pull nginx:stable & \
wait


# Build image
docker-compose -f ./docs/docker/compose/build.yml build


# Push image
run_and_check_exit_code "ecs-cli push $ENVIRONMENT/account/uwsgi:$TAG"
run_and_check_exit_code "ecs-cli push $ENVIRONMENT/account/nginx:$TAG"

if [ $? -ne 0 ]; then
    echo "push fails"
    exit 1
fi


# Deploy
run_and_check_exit_code "ecs-cli compose --cluster account-cluster --project-name account-www -f docs/docker/compose/account.yml service up --timeout 1200" \
                        "ecs-cli compose --cluster account-cluster --project-name account-cron -f docs/docker/compose/cron.yml service up --timeout 1200"

if [ $? -ne 0 ]; then
    echo "deploy fails"
    exit 1
fi


curl -X POST --data-urlencode "payload={\"text\": \"[$ENVIRONMENT - $TAG] 계정서버 배포가 완료되었습니다.\nRepo: https://github.com/ridi/account\"}" $SLACK_DEPLOY_HOOK
