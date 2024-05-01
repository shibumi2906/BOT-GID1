import telebot
from telebot import types
import config
from db import get_events_by_category

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

def handle_start(message):
    """
    Обработчик команды /start, отправляет приветственное сообщение и основные команды.
    """
    welcome_text = "Привет! Я ваш бот-гид по местным событиям. Используйте текстовые команды для управления мной.\n"
    welcome_text += "Доступные команды:\n"
    welcome_text += "/events - Посмотреть предстоящие события\n"
    welcome_text += "/help - Получить помощь\n"
    bot.send_message(message.chat.id, welcome_text)

def handle_help(message):
    """
    Обработчик команды /help, отправляет список доступных команд.
    """
    help_text = "Список команд:\n"
    help_text += "/start - начать работу с ботом\n"
    help_text += "/events - посмотреть предстоящие события\n"
    help_text += "/help - получить справку по командам\n"
    bot.send_message(message.chat.id, help_text)

def handle_events(message):
    """
    Обработчик команды /events, отправляет список предстоящих событий.
    """
    # Предположим, что события фильтруются по категории с ID 1 для примера
    events = get_events_by_category(1)
    if events:
        events_text = "Список событий:\n" + "\n".join(
            f"{i + 1}. {event['title']} - {event['date_time'].strftime('%d.%m.%Y')}" for i, event in enumerate(events)
        )
    else:
        events_text = "На данный момент событий нет."
    bot.send_message(message.chat.id, events_text)

def handle_default(message):
    """
    Обработчик всех других сообщений, не являющихся командами.
    """
    bot.reply_to(message, "Извините, я не понял вашу команду. Используйте /help для получения списка команд.")

# Регистрация обработчиков
bot.register_message_handler(handle_start, commands=['start'])
bot.register_message_handler(handle_help, commands=['help'])
bot.register_message_handler(handle_events, commands=['events'])
bot.register_message_handler(handle_default, func=lambda message: True)

# Не добавляем запуск бота здесь, так как это должно быть в файле main.py
