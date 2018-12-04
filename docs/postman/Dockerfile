FROM node:slim

ADD . /src
WORKDIR /src
RUN npm install
ARG PM_API_KEY
ENV PM_API_KEY=$PM_API_KEY
CMD bash wait_for_response.sh "npm run pm-test -- development $PM_API_KEY"