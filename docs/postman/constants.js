const POSTMAN_BASE_URL = 'https://api.getpostman.com';
const COLLECTION_NAME = 'Account';

const ENVIRONMENT_NAME = process.argv[2];
const API_KEY = process.argv[3];

module.exports = {
  API_KEY, POSTMAN_BASE_URL, COLLECTION_NAME, ENVIRONMENT_NAME,
};
