FROM node:lts-alpine

# setting env mode
ENV NODE_ENV=development

WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "./"]

# RUN npm install --production --silent && mv node_modules ../

# installing dependencies
RUN apk update
RUN npm install
RUN npm install json5

COPY . .

EXPOSE 3000
EXPOSE 5000

# setting user and permission to access the /app folder
# RUN chown & USER node can be removed if container takes too long to build, but may cause problems
RUN chown -R node /usr/src/app
USER node

CMD ["npm", "start"]
