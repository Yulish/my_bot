import telebot
from config import API_TOKEN
from extensions import CurrencyConverter, keys

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: not message.text.startswith('/') and message.text.lower() in keys)
def greet(message: telebot.types.Message):
    username = message.from_user.username if message.from_user.username else 'друг'
    bot.send_message(message.chat.id, f'Доброго времени суток, {username}! Отправьте /start, чтобы начать работу.')

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Введите запрос боту в следующем формате:\n <имя валюты, цену на которую надо узнать> <имя валюты, цену в которой надо узнать> <количество переводимой валюты>\nЧтобы увидеть список всех доступных валют, нажмите: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        parts = message.text.lower().strip().split()
        if len(parts) != 3:
            raise ValueError("Неверный формат запроса. Используйте: <валюта_покупки> <целевая_валюта> <сумма>")

        purchase_currency = parts[0]
        target_currency = parts[1]
        amount = float(parts[2])

        from_currency = keys.get(purchase_currency)
        to_currency = keys.get(target_currency)

        total = CurrencyConverter.get_price(purchase_currency, target_currency, amount)


        if isinstance(total, float):

            text = f'Стоимость {amount} {from_currency} составляет {total:.2f} {to_currency}.'
            bot.send_message(message.chat.id, text)
        else:
            raise ValueError(total)

    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка: " + str(e))

bot.polling(none_stop=True)
