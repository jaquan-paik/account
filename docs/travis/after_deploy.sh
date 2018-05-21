#!/bin/bash
set -e

curl -X POST --data-urlencode "payload={\"text\": \"[$ENVIRONMENT - $IMAGE_TAG] 계정서버 배포가 완료되었습니다.\nRepo: https://github.com/ridi/account\"}" $SLACK_DEPLOY_HOOK
