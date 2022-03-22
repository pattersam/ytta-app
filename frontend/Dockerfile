# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM tiangolo/node-frontend:10 as build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG FRONTEND_ENV=production
ENV VUE_APP_ENV=${FRONTEND_ENV}
ENV VUE_APP_NAME=ytta
ENV VUE_APP_DOMAIN_PROD=k8s-yttaapp-yttaappi-09ca915a8c-1517465418.eu-central-1.elb.amazonaws.com

RUN ["npm", "run", "build"]


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15

COPY --from=build-stage /app/dist/ /usr/share/nginx/html

COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
