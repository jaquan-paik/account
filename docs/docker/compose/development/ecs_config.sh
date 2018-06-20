#!/bin/sh

ecs-cli configure --region ap-northeast-2 --cluster account-cluster

ecs-cli compose --project-name account-www --file docker-compose-www.yml service up \
--deployment-min-healthy-percent 100 \
--deployment-max-percent 200 \
--target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:689221834431:targetgroup/ecs-account-scalable/34676c9b585f80ad \
--container-name account-nginx \
--container-port 80 \
--role ecsServiceRole

ecs-cli compose --project-name account-www-local --file docker-compose-www-local.yml service up \
--deployment-min-healthy-percent 100 \
--deployment-max-percent 200 \
--target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:689221834431:targetgroup/ecs-account-local-scalable/e7ea350ec4ff06ff \
--container-name account-nginx \
--container-port 80 \
--role ecsServiceRole

ecs-cli compose --project-name account-cron --file docker-compose-cron.yml service up \
--deployment-min-healthy-percent 0 \
--deployment-max-percent 100
