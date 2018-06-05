#!/bin/sh

ecs-cli configure --region ap-northeast-2 --cluster account-cluster

ecs-cli compose --project-name account-www --file docker-compose-www.yml service up \
--deployment-min-healthy-percent 100 \
--deployment-max-percent 200 \
--target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:588135293606:targetgroup/account-www/5cc15ab261b2021f \
--container-name account-nginx \
--container-port 80 \
--role ecsServiceRole

ecs-cli compose --project-name account-cron --file docker-compose-cron.yml service up \
--deployment-min-healthy-percent 0 \
--deployment-max-percent 100
