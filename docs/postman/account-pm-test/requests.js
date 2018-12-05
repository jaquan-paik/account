const request = require('request-promise-native');
const queryEncode = require('querystring').encode;

const {
    API_KEY,
    POSTMAN_BASE_URL,
    COLLECTION_NAMES,
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

const getCollections = async () => {
    const response = await requestToPostman('/collections');
    const collectionInfos = response.collections
        .filter(collection => COLLECTION_NAMES.includes(collection.name));
    const responses = await Promise.all(collectionInfos.map(collectionInfo => requestToPostman(`/collections/${collectionInfo.uid}`)));
    return responses.map(response=>response.collection);
};

const getEnvironment = async () => {
    let response = await requestToPostman('/environments');
    const environmentInfo = response.environments
        .filter(environment => environment.name === ENVIRONMENT_NAME)[0];
    response = await requestToPostman(`/environments/${environmentInfo.uid}`);
    return response.environment;
};

module.exports = {getCollections, getEnvironment};
