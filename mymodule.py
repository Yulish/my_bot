import telebot
from telebot import types
import requests
import json

# Ваш токен
API_TOKEN = "7979213873:AAEZ9s7xYlYbkfQLtHR-PYw-d9j3sQrDDSA"
bot = telebot.TeleBot(API_TOKEN)

keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
    'фунт': 'GBP',
}



@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    parts = message.text.lower().strip().split()
    purchase_currency = parts[0]
    target_currency = parts[1]
    amount = float(parts[2])
    from_currency = keys.get(purchase_currency)
    to_currency = keys.get(target_currency)
    r = requests.get(f'https://v6.exchangerate-api.com/v6/ff9b8add538cb109125252b7/pair/{from_currency}/{to_currency}')
    data = r.json()
    data['result'] = 'success'
    conversion_rate = data['conversion_rate']
    summ = conversion_rate * amount
    text = f'Стоимость {amount} {purchase_currency} составляет {summ:.2f} {target_currency}.'
    bot.send_message(message.chat.id, text)
    text = f'Стоимость {amount} USD составляет {summ:.2f} {purchase}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
