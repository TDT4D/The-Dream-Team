FROM node:23-alpine AS build

WORKDIR /app

COPY client/package*.json ./
RUN npm install
COPY client .
RUN npm run build

FROM node:23-alpine

WORKDIR /express-app

RUN mkdir client
COPY --from=build /app/build client/build/

COPY server/package*.json .
RUN npm install
COPY server .

RUN echo BUILD_PATH=./client/build > .env 
CMD ["npm", "start"]

EXPOSE 3000