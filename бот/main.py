import telebot
import wikipedia
import re
import logging
from telebot import types

# Включаем логирование
logging.basicConfig(filename='bot.log', level=logging.ERROR)

# Создаем экземпляр бота
bot = telebot.TeleBot('token from @papaBot')

# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")

# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        # Проверяем, что длина возвращаемого текста достаточна
        if len(wikitext) < 100:
            return "Информация о данном термине слишком короткая. Попробуйте ввести другой запрос."
        # Получаем первую тысячу символов
        wikitext = ny.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        logging.error("Error in getwiki: %s", str(e))
        return 'В энциклопедии нет информации об этом'

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton("/start")
    item_help = types.KeyboardButton("/help")
    item_list = types.KeyboardButton("/list")  # Добавляем кнопку "Список"
    markup.add(item_start, item_help, item_list)  # Добавляем кнопку в разметку
    bot.send_message(message.chat.id, "Привет! Отправьте мне любое слово, и я найду его значение на Wikipedia.", reply_markup=markup)


# Обработчик команды /help
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "Этот бот предоставляет информацию из Wikipedia. Отправьте мне любое слово, и я найду его значение на Wikipedia.")

# Обработчик кнопки "Список"
@bot.message_handler(func=lambda message: message.text == "/list")
def list_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_country = types.KeyboardButton("Страна")
    item_russia = types.KeyboardButton("Россия")
    item_flag = types.KeyboardButton("Флаг")
    markup.add(item_country, item_russia, item_flag)
    bot.send_message(message.chat.id, "Выберите слово из списка:", reply_markup=markup)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if not message.text:
        bot.send_message(message.chat.id, "Вы отправили пустое сообщение. Введите слово для поиска.")
    else:
        try:
            if message.text.lower() == 'страна':
                bot.send_message(message.chat.id, getwiki('Страна'))
            elif message.text.lower() == 'россия':
                bot.send_message(message.chat.id, getwiki('Россия'))
            elif message.text.lower() == 'флаг':
                bot.send_message(message.chat.id, getwiki('Флаг'))
            else:
                bot.send_message(message.chat.id, "Не могу обработать ваш запрос. Попробуйте выбрать слово из списка.")
        except Exception as e:
            logging.error("Error in handle_text: %s", str(e))
            bot.send_message(message.chat.id, "Возникла ошибка при обработке запроса.")

# Обработчик кнопки "Начать"
@bot.message_handler(func=lambda message: message.text == "Начать")
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_suggest = types.KeyboardButton("Предложить картинку")
    item_help = types.KeyboardButton("/help")
    markup.add(item_suggest, item_help)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

# Запускаем бота
bot.polling(none_stop=True, interval=0)
