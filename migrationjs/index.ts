import express, { Express, Request, Response } from 'express';
import { json } from 'stream/consumers';
import { Telegraf, Telegram } from 'telegraf'
import { ExtraDice } from 'telegraf/typings/telegram-types';
import { DataSource } from 'typeorm';
import { AppDataSource } from './data-source';
import { User } from './Models/User';

const token = "5612645727:AAGJSnks-HY5Wn3Gb7PVSccPnwhlZf6L3eU"
if (token === undefined) {
    throw new Error('BOT_TOKEN must be provided!')
}

const bot = new Telegraf(token)
// Set the bot response
//bot.on('text', (ctx) => ctx.replyWithHTML('<b>Hello</b>'))
bot.on('dice', (ctx) => {
    if (ctx.message.dice.value == 6) {
        ctx.reply('ебать ты жеский')
    } else {
        ctx.replyWithDice({ "emoji": "🎰" }).then((mes) => console.log(mes))
    }
    console.log(ctx.message.dice.value)
})
// bot.on('text', (ctx) => {

//     console.log(ctx.message.text)

// })
bot.command('registration', async (ctx) => {
    console.log('here');
    const user = new User()
    user.name = ctx.message.from.username!
    await user.save()
})
bot.command('listplayers', async (ctx) => {
    const users = await User
        .createQueryBuilder("user")
    console.log(users)
    JSON.stringify()
    ctx.reply(users)
})
const secretPath = `/telegraf/${bot.secretPathComponent()}`

// Set telegram webhook
// npm install -g localtunnel && lt --port 3000
bot.telegram.setWebhook(`https://legal-hornets-agree-212-12-20-9.loca.lt${secretPath}`)
bot.launch
const app = express()
AppDataSource
    .initialize()
    .then(() => {
        console.log("Data source has been initialized!")
    })
    .catch((error) =>
        console.error(error))

//bot.telegram.setMyCommands([{command: "registration",description: "регистрация буруна"}])

app.get('/', (req: Request, res: Response) => res.send('Hello World!'))
// Set the bot API endpoint
app.use(bot.webhookCallback(secretPath))
app.listen(3000, () => {
    console.log('App running on port 3000!')
})