FROM node:slim

ADD . /src
WORKDIR /src
RUN npm install
CMD '/src/wait_for_response.sh','npm run pm-test -- $ENVIRONMENT $PM_API_KEY'
