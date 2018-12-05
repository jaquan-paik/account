const newman = require('newman');
const { getCollection, getEnvironment } = require('./requests');

const noticeError = (error) => {
  console.log(error); // 우선은 로그만 찍어본다.
};

// 결과를 체크하여 에러가 있으면 어디서 어떤 에러가 났는지 알려준다.
const checkErrorAndSummary = (err, summary) => {
  let errorRaised = false;
  if (err !== null) {
    noticeError(err);
    return;
  }
  /* eslint-disable no-restricted-syntax */
  for (const exceution of summary.run.executions) {
    for (const assertion of exceution.assertions) {
      if (assertion.error) {
        errorRaised = true;
        noticeError({ error: assertion.error, request: exceution.request });
      }
    }
  }
  if (errorRaised) {
    throw new Error('api test fail');
  }
  console.log('no error');
};
const scenarioTest = async () => {
  const [collection, environment] = await Promise.all([getCollection(), getEnvironment()]);
  const options = {
    collection,
    environment,
    insecure: true,
    ignoreRedirects: true,
    // reporters: 'cli', error가 있으면 그것만 출력하고 전체 결과는 reporter는 사용하지 않는다.
  };
  newman.run(options, checkErrorAndSummary);
};

scenarioTest();
