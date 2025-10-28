import requests
from config import EXCHANGE_API_KEY

keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
    'фунт': 'GBP',
}


class CurrencyConverter:
    API_KEY = EXCHANGE_API_KEY

    @staticmethod
    def get_price(base, quote, amount):
        from_currency = keys.get(base.lower())
        to_currency = keys.get(quote.lower())

        if not from_currency or not to_currency:
            return "Ошибка: валюта не найдена"

        url = f'https://v6.exchangerate-api.com/v6/{CurrencyConverter.API_KEY}/pair/{from_currency}/{to_currency}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('result') == 'success':
                conversion_rate = data['conversion_rate']
                total = conversion_rate * amount
                return total
        return "Ошибка API"

