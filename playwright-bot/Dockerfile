FROM mcr.microsoft.com/playwright:v1.45.0-jammy
WORKDIR /bot
COPY package.json package-lock.json* /bot/
RUN npm install --omit=dev
COPY src /bot/src
EXPOSE 4000
CMD ["node", "src/server.js"]
