const POSTMAN_BASE_URL = 'https://api.getpostman.com';
const COLLECTION_NAMES = process.argv[2];

const ENVIRONMENT_NAME = 'development'; // 테스트용은 항상 development 환경 변수만 가지고 와야 한다.
const API_KEY = process.argv[3];

module.exports = {
    API_KEY, POSTMAN_BASE_URL, COLLECTION_NAMES, ENVIRONMENT_NAME,
};
