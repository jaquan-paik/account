const request = require('request-promise-native');
const queryEncode = require('querystring').encode;

const {
  API_KEY,
  POSTMAN_BASE_URL,
  COLLECTION_NAME,
  ENVIRONMENT_NAME,
} = require('./constants');

const requestToPostman = async (url, method = 'GET', data = {}, makeQuery = false) => {
  const options = {
    method,
    uri: `${POSTMAN_BASE_URL}${url}${makeQuery ? `?${queryEncode(data)}` : ''}`,
    headers: {
      'X-Api-Key': API_KEY,
    },
    json: data,
  };
  const response = await request(options);
  return response;
};

const getCollection = async () => {
  let response = await requestToPostman('/collections');
  const collectionInfo = response.collections
    .filter(collection => collection.name === COLLECTION_NAME)[0];
  response = await requestToPostman(`/collections/${collectionInfo.uid}`);
  return response.collection;
};

const getEnvironment = async () => {
  let response = await requestToPostman('/environments');
  const environmentInfo = response.environments
    .filter(environment => environment.name === ENVIRONMENT_NAME)[0];
  response = await requestToPostman(`/environments/${environmentInfo.uid}`);
  return response.environment;
};

module.exports = { getCollection, getEnvironment };
