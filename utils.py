import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CurConverter:
    @staticmethod
    def convert(quote: str, base: str, amount:str):

        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать в такую же валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество валюты {amount}')

        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={quote_ticker}_{base_ticker}&compact=ultra&apiKey=f7aad03331b59365fb7b')
        total_base = json.loads(r.content)[f'{quote_ticker}_{base_ticker}']
        return total_base
