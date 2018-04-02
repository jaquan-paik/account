#!/bin/bash

COMMIT_SHA=${TRAVIS_COMMIT::8}

curl -X POST --data-urlencode "payload={\"text\": \"계정서버 배포가 완료되었습니다.[$ENVIRONMENT - $COMMIT_SHA]\nRepo: https://github.com/ridi/account\"}" $SLACK_DEPLOY_HOOK
