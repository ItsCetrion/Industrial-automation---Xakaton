import telebot
from telebot import types


bot = telebot.TeleBot("6746593435:AAGZzQbDaY6zcxs7klTVyFbkKej_BMiCIos")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    bnt2 = types.KeyboardButton('Удалить фото')
    bnt3 = types.KeyboardButton('Изменить текст')
    markup.row(btn1)
    markup.row(bnt2, bnt3)
    bot.send_message(message.chat.id, "Привет", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, "Website is open")
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, "delete")

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    bnt2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    bnt3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn1)
    markup.row(bnt2, bnt3)
    bot.reply_to(message, 'Какое красивое фото', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


bot.polling(none_stop=True)