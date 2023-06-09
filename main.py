import telebot
from extensions import APIException, Convertor
from config import *


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def start(message: telebot.types.Message):
    text = """"Приветствую! Я Конвертирую валюты. Хочешь узнать какие \
валюты  могу обрабатывать? Введи команду /values. \n Для конвертации вводить в формате: \
<имя валюты, цену которую вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, 'Неверное количество параметров! Воспользуйтесь командой /help')
    try:
        new_price = Convertor.get_price(base, quote, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {quote} : {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка команды! Воспользуйтесь командой /help':\n {e}")

bot.polling()
