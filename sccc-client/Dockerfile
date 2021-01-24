FROM node:alpine AS dependency-stage
WORKDIR /app
COPY package.json ./
RUN yarn install
COPY . .

FROM dependency-stage as build-stage
RUN yarn run build

FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]