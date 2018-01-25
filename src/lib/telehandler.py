import telebot


tbot = telebot.TeleBot('516834738:AAFiBE5c-0TDGBQUBY2OvDvHDgh0UNBZrOU')

@tbot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # print(message.from_user.first_name)
    # bot.reply_to(message, u"Hello, welcome to this bot!")
    # bot.send_message(chat_id=message.from_user.id, text='cock')
    # markup = telebot.types.ReplyKeyboardRemove()
    markup = telebot.types.InlineKeyboardMarkup(row_width=6)
    gobtn1 = telebot.types.InlineKeyboardButton(text='Го', callback_data='say_ok')
    gobtn2 = telebot.types.InlineKeyboardButton(text='Го', callback_data='say_ok')
    gobtn3 = telebot.types.InlineKeyboardButton(text='Го', callback_data='say_ok')
    markup.row(gobtn1)
    markup.row(gobtn2, gobtn3)
    tbot.send_message(chat_id=message.from_user.id, text='Шо го? Камон коуч бой летс ду зис', reply_markup=markup)

@tbot.callback_query_handler(func=lambda call: call.data == 'say_ok')
def test_callback(call):
    tbot.send_message(call.from_user.id, text='найс найс')

# @bot.message_handler(regexp='Похналэ')
# def alo(message):
#     print('got it')


# print(bot.get_updates())