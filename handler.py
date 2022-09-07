import chat
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Handler:
  def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Создать игру", callback_data="create_game"),
               InlineKeyboardButton(
                   "Вывести общую статистику", callback_data="allstat"),
               InlineKeyboardButton(
                   "Вывести мою статистику", callback_data="mystat"),
               InlineKeyboardButton("Шутка дня", callback_data="top_joke"),
               InlineKeyboardButton("Анекдот дня", callback_data="top_anekdot"))
    return markup


  def game_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Начать игру", callback_data="game_start"),
               InlineKeyboardButton(
                   "Отменить игру", callback_data="game_stop"),
               InlineKeyboardButton("Записаться на игру",
                                    callback_data="write_to_a_game"),
               InlineKeyboardButton("Моя команда победила",
                                    callback_data="win_game"),
               InlineKeyboardButton("Моя команда проиграла", callback_data="false_game"))
    return markup


  def getJokeFunction(message, now_chat):
    bot.send_message(message.message.chat.id, now_chat.getHohma(1))
    #bot.send_message(message.message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())


  def getAnektod(message, now_chat):
    anekdot = now_chat.getHohma(2)
    if (anekdot[0] == True):
        bot.send_message(message.message.chat.id,
                         "Эта шутка уже была раньше, попробуй снова")
    else:
        bot.send_message(message.message.chat.id, anekdot)


  def createGameFunction(now_chat, message, from_who):
    isGame = now_chat.createGame(from_who)
    if (isGame is False):
        bot.answer_callback_query(
            message.id, 'Игру уже кто-то начал.\nЗаверши предыдущую, прежде чем начать новую.')
        return

    bot.send_message(message.message.chat.id, 'Так, так, так.. Кто это тут у нас хочет начать игру?\nДавайте поможем %s собрать участников.\nСейчас в 1/4 игроков в игре.' %
                     from_who, reply_markup=game_markup())


  def writeOnAGame(now_chat, message, from_who):
    isMe = now_chat.writeUserToGame(from_who)
    if (isMe == 1):
        bot.answer_callback_query(
            message.id, '%s, в данный момент идёт игра, жди.' % from_who)
    elif (isMe == 2):
        bot.answer_callback_query(
            message.id, '%s, игроков уже достаточно.' % from_who)
    elif (isMe == 3):
        bot.answer_callback_query(
            message.id, '%s, ты уже в игре, дай другим записаться.' % from_who)
    elif (isMe == 4):
        bot.answer_callback_query(
            message.id, '%s, и куда ты регаться пытаешься?' % from_who)
    else:
        bot.send_message(message.message.chat.id,
                         '%s, ты записался.\nСейчас %s/4 игроков в игре.' % (from_who, len(isMe)))


  def startGame(now_chat, message, from_who):
    isGameStart = now_chat.gameStart(from_who)
    if (isGameStart == 0):
        bot.answer_callback_query(
            message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif (isGameStart == 1):
        bot.answer_callback_query(message.id, 'Слишком мало игроков для игры.')
        return
    elif (isGameStart == 2):
        bot.answer_callback_query(message.id, 'Идёт игра, жди очереди.')
        return
    elif (isGameStart == 3):
        bot.answer_callback_query(
            message.id, 'Ты не создатель игры, иди лесом.')
        return

    players = isGameStart

    teams = "Наши команды:\n"
    team = list(players.items())

    if (len(team) == 2):
        teams += team[0][0] + " vs " + team[1][0]
    elif (len(team) == 4):
        team = list(players.items())
        teams += team[0][0] + " и " + team[1][0] + \
            "\nvs\n" + team[2][0] + " и " + team[3][0]

    bot.send_message(message.message.chat.id, teams + "\nИгра началась!")


  def stopGame(now_chat, message, from_who):
    isGameStop = now_chat.gameStop(from_who)
    if (isGameStop == 0):
        bot.answer_callback_query(
            message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif (isGameStop == 1):
        bot.answer_callback_query(
            message.id, 'Игра даже не началась, отменять нечего.')
        return
    elif (isGameStop == 2):
        bot.answer_callback_query(message.id, 'Отменять нечего.')
    elif (isGameStop == 3):
        bot.send_message(message.message.chat.id,
                         '%s отменил игру.' % from_who)


  def winGame(now_chat, message, from_who):
    isResult = now_chat.writeResult(True, from_who)
    if (isResult == 0):
        bot.answer_callback_query(
            message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif (isResult == 1):
        bot.answer_callback_query(message.id, 'Игра даже не началась.')
        return
    else:
        bot.send_message(message.message.chat.id,
                         '%s объявил победу своей команды.' % from_who)


  def loseGame(now_chat, message, from_who):
    isResult = now_chat.writeResult(False, from_who)
    if (isResult == 0):
        bot.answer_callback_query(
            message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif (isResult == 1):
        bot.answer_callback_query(message.id, 'Игра даже не началась.')
        return
    else:
        bot.send_message(message.message.chat.id,
                         '%s объявил поражение своей команды.' % from_who)
