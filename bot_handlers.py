from telebot.async_telebot import types
import asyncio
import os
from bot import bot
from kinopoisk_api import KinopoiskAPI


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.send_message(message.chat.id, 'Привет, назови фильм о котором хочешь узнать.')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['text'])
async def answer(message):
    api = KinopoiskAPI()
    is_good_request = False
    film_names = api.search(message.text)
    if not film_names:
        await bot.send_message(message.chat.id, "Извините, по вашему запросу результатов не найдено")
    else:
        for name in film_names:
            if name.lower() == message.text.lower():
                is_good_request = True
                description = api.get_film_short_description(name)
                api.download_poster(name)
                markup = types.InlineKeyboardMarkup()
                item_rating = types.InlineKeyboardButton(text='Рейтинг', callback_data='rating')
                item_year = types.InlineKeyboardButton(text='Год производства', callback_data='year')
                item_countries = types.InlineKeyboardButton(text='Страны', callback_data='countries')
                markup.add(item_rating, item_year, item_countries)
                if os.path.exists('img.jpg'):
                    await bot.send_photo(message.chat.id,
                                         photo=open('img.jpg', 'rb'),
                                         caption=f'*{name}*\n\n{description}',
                                         parse_mode='Markdown',
                                         reply_markup=markup)
                else:
                    await bot.send_message(message.chat.id,
                                           f'*{name}*\n\n{description}',
                                           parse_mode='Markdown',
                                           reply_markup=markup)
                return
        if not is_good_request:
            res = ""
            markup = types.ReplyKeyboardMarkup(row_width=2)
            for el in film_names:
                btn = types.KeyboardButton(el)
                markup.add(btn)
            for i in range(len(film_names)):
                res += f"{i + 1}) {film_names[i]}\n"
            await bot.send_message(message.chat.id,
                                   f'Вот результаты по вашему запросу:\n{res}\n Выберите интересующий вас вариант',
                                   reply_markup=markup)


# markup = types.InlineKeyboardMarkup()
# item_rating = types.InlineKeyboardButton(text='Рейтинг', callback_data='rating')
# item_year = types.InlineKeyboardButton(text='Год', callback_data='year')
# item_countries = types.InlineKeyboardButton(text='Страны', callback_data='countries')
# markup.add(item_rating, item_year, item_countries)
#
# await bot.send_photo(message.chat.id,
#                      photo=open('img.jpg', 'rb'),
#                      caption=f'*{name}*\n\n{description}',
#                      parse_mode='Markdown',
#                      reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
async def answer(call):
    film = call.message.caption
    api = KinopoiskAPI()
    if call.data == 'rating':
        await bot.send_message(call.message.chat.id, f'Рейтинг Кинопоиска: {api.get_film_rating(film)}')

    elif call.data == 'year':
        await bot.send_message(call.message.chat.id, f'Год производства: {api.get_film_year(film)}')

    elif call.data == 'countries':
        await bot.send_message(call.message.chat.id, f'Страны: {api.get_film_countries(film)}')


asyncio.run(bot.polling(none_stop=True))
