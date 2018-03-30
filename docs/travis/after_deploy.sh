#!/bin/bash

COMMIT_SHA=${TRAVIS_COMMIT::8}

curl -X POST --data-urlencode "payload={\"text\": \"$ENVIRONMENT - $COMMIT_SHA - 배포가 완료되었습니다.\"}" $SLACK_DEPLOY_HOOK
