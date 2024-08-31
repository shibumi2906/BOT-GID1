import telebot
from telebot import types
import config
from bd import init_db

# Создаём экземпляр бота
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# Инициализация базы данных
init_db()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = ("Привет! Я ваш бот-гид по местным событиям. Используйте текстовые команды для управления мной.\n"
                    "Доступные команды:\n"
                    "/events - Посмотреть предстоящие события\n"
                    "/help - Получить помощь\n")
    bot.send_message(message.chat.id, welcome_text)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = ("Список команд:\n"
                 "/start - начать работу с ботом\n"
                 "/events - посмотреть предстоящие события\n"
                 "/help - получить справку по командам\n")
    bot.send_message(message.chat.id, help_text)

# Обработчик команды /events
@bot.message_handler(commands=['events'])
def show_events(message):
    # Предполагается, что будет реализация вывода событий
    events_text = ("Список событий: (пример данных)\n"
                   "1. Музыкальный фестиваль - 12.05.2023\n"
                   "2. Выставка искусств - 15.05.2023\n")
    bot.send_message(message.chat.id, events_text)

# Обработчик для текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Извините, я не понял вашу команду. Используйте /help для получения списка команд.")

# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()

