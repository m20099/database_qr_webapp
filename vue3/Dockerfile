FROM node:18-alpine

RUN apk add --no-cache git && yarn global add @vue/cli

WORKDIR /app

COPY my-project/package.json my-project/yarn.lock ./

# RUN yarn install

COPY my-project .

CMD ["yarn", "serve"]
