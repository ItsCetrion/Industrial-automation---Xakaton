import telebot
import os
import pandas as pd
from telebot import types

bot_token = '6746593435:AAGZzQbDaY6zcxs7klTVyFbkKej_BMiCIos'  # Замените YOUR_BOT_TOKEN на свой токен

bot = telebot.TeleBot(bot_token)

current_user_data = None
file_uploaded = False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Загрузить CSV файл")

    markup.add(item1)

    bot.reply_to(message, "Привет! Я бот для проверки данных в CSV файле. Выбери действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    global current_user_data
    global file_uploaded

    if message.text == "Загрузить CSV файл":
        bot.reply_to(message, "Пришли мне свой CSV файл.")
    else:
        bot.reply_to(message, "Я не понимаю твоего запроса. Выбери действие, используя кнопку 'Загрузить CSV файл'.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    global current_user_data
    global file_uploaded

    try:
        chat_id = message.chat.id
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Создаем директорию "downloads", если ее нет
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        file_name = os.path.join("downloads", file_path.split('/')[-1])
        downloaded_file = bot.download_file(file_path)

        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        current_user_data = pd.read_csv(file_name)

        result = check_data(current_user_data)

        bot.reply_to(message, result)

        # Опционально: удаление загруженного файла после обработки
        os.remove(file_name)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

def check_data(data):
    invalid_data = []

    for index, row in data.iterrows():
        if not (-20 <= row['Температура'] <= 20) or not (0 <= row['Давление'] <= 35):
            invalid_data.append(row['Номер_датчика'])

    if not invalid_data:
        return "Все данные в интервале. Всё хорошо."
    else:
        return f"Проблемы с датчиками: {', '.join(map(str, invalid_data))}"

bot.polling(none_stop=True)
