FROM mcr.microsoft.com/playwright:v1.45.0-jammy
WORKDIR /bot
COPY package.json package-lock.json* /bot/
RUN npm install
COPY src /bot/src
CMD ["node", "src/bot.js"]
