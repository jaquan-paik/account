const newman = require('newman');
const { getCollections, getEnvironment } = require('./requests');

const noticeError = (error) => {
  console.log(error); // 우선은 로그만 찍어본다.
};

const getParsedRequest = (request) => ({
    method: request.method,
    url: `${request.url.protocol}/${request.url.host.join('.')}`,
    query: JSON.stringify(request.url.query.reference),
    header: JSON.stringify(request.headers.reference),
    body: JSON.stringify(request.body)
});

const checkErrorAndSummary = (err, summary) => {
  const collectionName = summary.collection.name;
  let errorRaised = false;
  if (err !== null) {
      noticeError(err);
      throw new Error(` collections: "${collectionName}" test fail`); 
  }
  for (const exceution of summary.run.executions) {
      if (exceution.requestError) {
          noticeError({collectionName,error: exceution.requestError, request: getParsedRequest(exceution.request)});
          errorRaised = true;
          continue;
      }
      for (const assertion of exceution.assertions) {
          if (assertion.error) {
              errorRaised = true;
              noticeError({collectionName, error: assertion.error, request: getParsedRequest(exceution.request)});
          }
      }
  }

  if (errorRaised) {
      throw new Error(` collections: "${collectionName}" test fail`);
  }
  console.log(`collection: "${collectionName}" passed`);
};

const scenarioTest = (collection, environment)=>{
  const options = {
    collection,
    environment,
    insecure: true,
    ignoreRedirects: true,
    // reporters: 'cli',// error가 있으면 그것만 출력하고 전체 결과는 reporter는 사용하지 않는다.
  };
  newman.run(options, checkErrorAndSummary);
}

const main = async () => {
  const [collections, environment] = await Promise.all([getCollections(), getEnvironment()]);
  collections.forEach(collection=>scenarioTest(collection,environment))
};

main();

