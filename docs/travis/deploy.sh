#!/bin/bash
set -e

# Set environment
if [ "$1" = development ]
then

export ENVIRONMENT=development
export ACCOUNT_ECR=$DEV_ACCOUNT_ECR
export AWS_ACCESS_KEY_ID=$DEV_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$DEV_AWS_SECRET_ACCESS_KEY
export IMAGE_TAG=${TRAVIS_COMMIT::8}

else

export ENVIRONMENT=production
export ACCOUNT_ECR=$PROD_ACCOUNT_ECR
export AWS_ACCESS_KEY_ID=$PROD_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$PROD_AWS_SECRET_ACCESS_KEY
export IMAGE_TAG=$TRAVIS_TAG

fi

# Prepare build
make ci-settings ns=$ENVIRONMENT

$(aws ecr get-login --no-include-email --region=$AWS_DEFAULT_REGION)

docker pull ridibooks/python:bootstrap-django-2017.02.01 & \
docker pull nginx:stable & \
wait


# Build image
make ci-build-account env=$ENVIRONMENT & \
make nginx-build-image env=$ENVIRONMENT & \
wait

# Tag image
make ci-tag-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest & \
make ci-tag-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$IMAGE_TAG & \
make nginx-tag-image env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest & \
make nginx-tag-image env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$IMAGE_TAG & \
wait

# Push image
make ci-push-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest & \
make ci-push-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$IMAGE_TAG & \
make nginx-push-image env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest & \
make nginx-push-image env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$IMAGE_TAG & \
wait


# Deploy
ecs deploy --timeout=1200 --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY account-cluster account-www & \
ecs deploy --timeout=1200 --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY account-cluster account-cron & \
wait

curl -X POST --data-urlencode "payload={\"text\": \"[$ENVIRONMENT - $IMAGE_TAG] 계정서버 배포가 완료되었습니다.\nRepo: https://github.com/ridi/account\"}" $SLACK_DEPLOY_HOOK
