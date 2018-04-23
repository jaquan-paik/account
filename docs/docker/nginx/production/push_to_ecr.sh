#!/bin/sh
env=production
ecr_path=588135293606.dkr.ecr.ap-northeast-2.amazonaws.com

make nginx-build-image env=$env
make nginx-tag-image env=$env ecr_path=$ecr_path tag=latest
make nginx-push-image env=$env ecr_path=$ecr_path tag=latest
