import express, { Express, Request, Response } from 'express';
import {Telegraf } from 'telegraf'

const token = "5612645727:AAGJSnks-HY5Wn3Gb7PVSccPnwhlZf6L3eU"
if (token === undefined) {
  throw new Error('BOT_TOKEN must be provided!')
}

const bot = new Telegraf(token)
// Set the bot response
bot.on('text', (ctx) => ctx.replyWithHTML('<b>Hello</b>'))
bot.on('dice', (ctx) => ctx.reply('норм роляешь'))

const secretPath = `/telegraf/${bot.secretPathComponent()}`

// Set telegram webhook
// npm install -g localtunnel && lt --port 3000
bot.telegram.setWebhook(`https://little-geckos-attend-212-12-20-9.loca.lt${secretPath}`)

const app = express()
app.get('/', (req: Request, res: Response) => res.send('Hello World!'))
// Set the bot API endpoint
app.use(bot.webhookCallback(secretPath))
app.listen(3000, () => {
  console.log('Example app listening on port 3000!')
})