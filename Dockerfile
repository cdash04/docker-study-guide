FROM node:24

WORKDIR /app

COPY package.json .

RUN yarn --frozen-lockfile

COPY . .

RUN yarn build

EXPOSE 3000

CMD [ "yarn", "start" ]
