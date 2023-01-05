import telebot
from config import keys, TOKEN
from utils import ConvertionException, CurConverter

bot = telebot.TeleBot(TOKEN)
  
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате: \n<имя валюты, цену которой вы хотите узнать> \
<в какую валюту перевести> <количество переводимой валюты>\n \
Просмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Должно быть три параметра')

        quote, base, amount = values

        total_base = CurConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(amount) * float(total_base)}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
