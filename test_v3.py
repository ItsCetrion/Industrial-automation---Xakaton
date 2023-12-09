import telebot
import os
import pandas as pd
from telebot import types

bot_token = '6746593435:AAGZzQbDaY6zcxs7klTVyFbkKej_BMiCIos'  # Замените YOUR_BOT_TOKEN на свой токен
bot = telebot.TeleBot(bot_token)

current_user_data = None
file_uploaded = False
configuring_temperature = False
configuring_pressure = False

min_pressure = 0
max_pressure = 0
min_temperature = 0
max_temperature = 0


# Обработчики команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global min_pressure
    min_pressure = -25
    global max_pressure
    max_pressure = 20
    global min_temperature
    min_temperature = -20
    global max_temperature
    max_temperature = 25
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Загрузить CSV файл")
    item2 = types.KeyboardButton("Изменение конфигурации")

    markup.add(item1, item2)

    bot.reply_to(message, "Привет! Я бот для проверки данных в CSV файле. Выбери действие:", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    global current_user_data
    global file_uploaded
    global configuring_temperature
    global configuring_pressure
    if message.text == "Загрузить CSV файл":
        bot.reply_to(message, "Пришли мне свой CSV файл.")
    elif message.text == "Изменение конфигурации":
        show_configuration_menu(message.chat.id)
    elif configuring_temperature:
        handle_temperature_input(message)
    elif configuring_pressure:
        handle_pressure_input(message)
    else:
        bot.reply_to(message, "Я не понимаю твоего запроса. Выбери действие, используя кнопку 'Загрузить CSV файл'.")

# Обработчик Inline-команд
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == "change_temperature":
        change_temperature_configuration(call.message.chat.id)
    elif call.data == "change_pressure":
        change_pressure_configuration(call.message.chat.id)

# Функция для вывода меню изменения конфигурации
def show_configuration_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Изменение температуры", callback_data="change_temperature")
    item2 = types.InlineKeyboardButton("Изменение давления", callback_data="change_pressure")

    markup.add(item1, item2)

    bot.send_message(chat_id, "Выберите параметр для изменения конфигурации:", reply_markup=markup)

# Функция для изменения температуры
def change_temperature_configuration(chat_id):
    global configuring_temperature
    configuring_temperature = True
    bot.send_message(chat_id, "Введите новые минимальное и максимальное значения температуры (через пробел):")

# Функция для изменения давления
def change_pressure_configuration(chat_id):
    global configuring_pressure
    configuring_pressure = True
    bot.send_message(chat_id, "Введите новые минимальное и максимальное значения давления (через пробел):")

# Функция для обработки ввода значений температуры
def handle_temperature_input(message):
    global configuring_temperature

    try:
        values = message.text.split()
        global min_temperature
        global max_temperature
        min_temperature = int(values[0])
        max_temperature = int(values[1])

        # Здесь можно обновить конфигурацию с учетом новых значений температуры
        bot.send_message(message.chat.id, f"Конфигурация температуры изменена. Мин: {min_temperature}, Макс: {max_temperature}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка ввода. Попробуйте еще раз. Ошибка: {str(e)}")

    configuring_temperature = False

# Функция для обработки ввода значений давления
def handle_pressure_input(message):
    global configuring_pressure
    global min_pressure
    global max_pressure
    try:
        values = message.text.split()
        min_pressure = float(values[0])
        max_pressure = float(values[1])

        # Здесь можно обновить конфигурацию с учетом новых значений давления
        bot.send_message(message.chat.id, f"Конфигурация давления изменена. Мин: {min_pressure}, Макс: {max_pressure}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка ввода. Попробуйте еще раз. Ошибка: {str(e)}")

    configuring_pressure = False


def check_data(data, min_temperature=-20, max_temperature=20, min_pressure=0, max_pressure=35):
    invalid_data = []

    for index, row in data.iterrows():
        if not (min_temperature <= row['Температура'] <= max_temperature) or not\
                (min_pressure <= row['Давление'] <= max_pressure):
            invalid_data.append(row['Номер_датчика'])

    if not invalid_data:
        return "Все данные в интервале. Всё хорошо."
    else:
        return f"Проблемы с датчиками: {', '.join(map(str, invalid_data))}"


# Обработчик документов (загрузка CSV файла)
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
        file_uploaded = True

        print(min_temperature, max_temperature)
        result = check_data(current_user_data, min_temperature=min_temperature, max_temperature=max_temperature, min_pressure=min_pressure, max_pressure=max_pressure)

        bot.reply_to(message, result)

        # Опционально: удаление загруженного файла после обработки
        os.remove(file_name)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


# Запуск бота
bot.polling(none_stop=True)
