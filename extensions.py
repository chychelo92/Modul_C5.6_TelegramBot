import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена! Воспользуйтесь командой /help")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена! Воспользуйтесь командой /help")

        if base_key == quote_key:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}! Воспользуйтесь командой /help")
        
        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}! Воспользуйтесь командой /help")
        
        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={quote_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][quote_key] * float(amount)
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote} : {new_price}"
        return message

