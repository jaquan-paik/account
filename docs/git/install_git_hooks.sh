#!/bin/sh

cp ./pre_commit.sh ../../.git/hooks/pre-commit
cp ./commit_msg.sh ../../.git/hooks/commit-msg
cp ./prepare_commit_msg.sh ../../.git/hooks/prepare-commit-msg

if ! command -v git-secrets &> /dev/null; then brew install git-secrets; fi

git secrets --add "(\"|')?(AWS|aws|Aws)?_?(SECRET|secret|Secret)?_?(ACCESS|access|Access)?_?(KEY|key|Key)(\"|')?\\s*(:|=>|=)\\s*(\"|')?[A-Za-z0-9/\\+=]{40}(\"|')?"
git secrets --add "(\"|')?(AWS|aws|Aws)?_?(ACCOUNT|account|Account)_?(ID|id|Id)?(\"|')?\\s*(:|=>|=)\\s*(\"|')?[0-9]{4}\\-?[0-9]{4}\\-?[0-9]{4}(\"|')?"

# aws secret key
git secrets --add "(\"|\')[a-zA-Z0-9]{14}\/[a-zA-Z0-9]{25}(\"|\')|\=\ ?[a-zA-Z0-9]{14}\/[a-zA-Z0-9]{25}"

# sentry
git secrets --add "(\"|\')https:\/\/.*\@sentry\.io(\"|\')|\=\ ?https:\/\/.*\@sentry\.io"

# general pattern
git secrets --add "(\_|\-)(key|KEY|Key)(\"|\')?\ ?(\:|\=)?\ ?(\"|\')([a-zA-Z0-9\-\_]{12})"
git secrets --add "(\_|\-)(secret|SECRET|Secret)(\"|\')?\ ?(\:|\=)?\ ?(\"|\')([a-zA-Z0-9\-\_]{12})"
git secrets --add "(\_|\-)(id|ID|Id)(\"|\')?\ ?(\:|\=)?\ ?(\"|\')([a-zA-Z0-9\-\_]{12})"
git secrets --add "(\_|\-)(token|TOKEN|Token)(\"|\')?\ ?(\:|\=)?\ ?(\"|\')([a-zA-Z0-9\-\_]{12})"

# git secrets --add 를 중복으로 하게 되면 에러 출력하기 때문에 마지막에 echo 를 넣어준다.
echo ""
