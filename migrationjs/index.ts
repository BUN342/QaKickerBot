import express, { Request, Response } from 'express';
import { Telegraf } from 'telegraf'
import { AppDataSource } from './data-source';
import { Chat } from './Models/Chat';
import { User } from './Models/User';

const token = "5612645727:AAGJSnks-HY5Wn3Gb7PVSccPnwhlZf6L3eU"
if (token === undefined) {
    throw new Error('BOT_TOKEN must be provided!')
}

const bot = new Telegraf(token)
// Set the bot response
//bot.on('text', (ctx) => ctx.replyWithHTML('<b>Hello</b>'))

bot.on('dice', (ctx) => {
    if (ctx.message.dice.emoji == "🎲" && ctx.message.dice.value == 6) {
        ctx.reply('да это жеско')
    } else {
        ctx.replyWithDice({ "emoji": ctx.message.dice.emoji })
            .then((mes) => {
                if (mes.dice.value in [1, 22, 43]) {
                    ctx.reply("В сола не почувствовал")
                }
                if (mes.dice.value == 64) {
                    ctx.reply("Разъебочка тремя топорами")
                }
            }
            )

    }
})

bot.command(('/regchat'), async (ctx) => {


    const chat = Chat
        .findOneByOrFail(
            {
                telegramId: ctx.chat.id
            }
        )
        .then(() => ctx.reply("Этот чат уже зареган"))
        .catch(async () => {
            const chat = new Chat()
            chat.telegramId = ctx.chat.id
            await chat.save()
            ctx.reply('Чат был успешно зареган')
        })
    

})

bot.command(('/gofootball'), async (ctx) => {

})

bot.command('registration', async (ctx) => {
    ctx.replyWithSticker("CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE")
    const user = await User.findOneByOrFail({ telegram_id: ctx.message.from.id })
        .then(() => {
            ctx.reply(`${ctx.message.from.first_name}, ты уже зареган`)
        })
        .catch(async () => {
            let user = new User()
            user.name = ctx.message.from.first_name
            user.telegram_id = ctx.message.from.id
            await user.save()
            ctx.reply(`${user.name}, ты успешно зарегался`)
        })
})
bot.command('listplayers', async (ctx) => {
    let users = await User.find()
    //users = JSON.stringify(users);
    let usersToSend = ''
    users.forEach((elem, index) => {
        usersToSend += `${index + 1}. ${elem.name} -- ${elem.score} \r\n`
    })
    ctx.replyWithSticker("CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE")
    console.log(usersToSend)
    //users = JSON.sringify(users)
    usersToSend ? ctx.reply(usersToSend) : ctx.reply("Никто еще не зарегистрировался :с")
})
bot.command('mystat', async (ctx) => {
    ctx.replyWithSticker("CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE")
    let user = await User.findOneByOrFail({ name: ctx.message.from.first_name })
        .then((user) => {
            ctx.reply(`${user.name}, у тебя ${user.score} очков`)
        })
        .catch(() => {
            ctx.reply("Слыш зарегайся сначала")
        })
})
bot.command('foodpoll', (ctx) => {
    ctx.replyWithSticker("CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE")
    ctx.replyWithPoll("Что на обед?", [
        "Мак",
        "Мама мия",
        "Тандыр",
        "Доставка",
        "У кого др11"
    ], {
        is_anonymous: false,
        open_period: 600
    })
})

bot.on('message', (ctx) => {
    if ('text' in ctx.message) {
        if (ctx.message.text.toLowerCase().includes("логи")
            || ctx.message.text.toLowerCase().includes("краш")) {
            ctx.replyWithSticker("CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE")
        }

    }
})
const secretPath = `/telegraf/${bot.secretPathComponent()}`

// Set telegram webhook
// npm install -g localtunnel && lt --port 3000
bot.telegram.setWebhook(`https://rare-hornets-poke-212-12-20-9.loca.lt${secretPath}`)
const app = express()
AppDataSource
    .initialize()
    .then(() => {
        console.log("Data source has been initialized!")
    })
    .catch((error) =>
        console.error(error))

bot.telegram.setMyCommands([
    {
        command: "registration",
        description: "регистрация буруна"
    },
    {
        command: "mystat",
        description: "мой бурун"

    },
    {
        command: "listplayers",
        description: "список бурунов"
    },
    {
        command: "foodpoll",
        description: "кто сегодня с обедом?"
    }
])

app.get('/', (req: Request, res: Response) => res.send('Hello World!'))
// Set the bot API endpoint
app.use(bot.webhookCallback(secretPath))
app.listen(3000, () => {
    console.log('App running on port 3000!')
})