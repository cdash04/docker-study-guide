FROM node:24.0.0-alpine

RUN apk add curl

WORKDIR /app

COPY package.json .

RUN yarn --frozen-lockfile

COPY . .

RUN yarn build

EXPOSE 3000

CMD [ "yarn", "start" ]
