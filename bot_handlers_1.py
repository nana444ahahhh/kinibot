from telebot.async_telebot import types
import asyncio

from bot import bot
import kinopoisk_api


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    # markup = types.ReplyKeyboardMarkup(row_width=2)
    # item_btn_1 = types.KeyboardButton('a')
    # item_btn_2 = types.KeyboardButton('v')
    # item_btn_3 = types.KeyboardButton('d')
    # markup.row(item_btn_1, item_btn_2, item_btn_3)
    markup = types.ForceReply(selective=False)
    await bot.send_message(message.chat.id, 'Привет, назови фильм о котором хочешь узнать.', reply_markup=markup)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['text'])
async def answer(message):
    name, description = kinopoisk_api.search(message.text)
    await bot.send_message(message.chat.id, f'*{name}*\n\n{description}', parse_mode='Markdown')


asyncio.run(bot.polling(none_stop=True))
