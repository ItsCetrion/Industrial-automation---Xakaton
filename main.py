import telebot
import webbrowser
bot = telebot.TeleBot('6746593435:AAGZzQbDaY6zcxs7klTVyFbkKej_BMiCIos')


@bot.message_handler(commands=["sisite", "website"])
def site(message):
    webbrowser.open('https://www.xvideos.com/?k=ded+old')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name}")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "<b>help</b> <em><u>information!</u></em>", parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == "информация":
        bot.send_message(message.chat.id, f"Вот тебе информация {message.from_user.first_name}")
    elif message.text.lower() == "id":
        bot.send_message(message.chat.id, f"Вот твой id\n{message.from_user.id}")


bot.polling(none_stop=True)