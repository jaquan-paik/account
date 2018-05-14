#!/bin/bash
set -e

COMMIT_SHA=${TRAVIS_COMMIT::8}

curl -X POST --data-urlencode "payload={\"text\": \"[$ENVIRONMENT - $COMMIT_SHA] 계정서버 배포가 완료되었습니다.\nRepo: https://github.com/ridi/account\"}" $SLACK_DEPLOY_HOOK
