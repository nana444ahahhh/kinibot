import asyncio

from bot import bot
import maps

ind = False
city = ''


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.send_message(message.chat.id, """\
Привет! Это игра "Угадай город"! Здесь ты по фото будешь отгадывать город!\n
Напиши "Новый город", чтобы получить фотографию города, затем попробуй его отгадать!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['text'])
async def answer(message):
    global ind, city
    if ind:
        if message.text.lower() == city.lower():
            await bot.send_message(message.chat.id, 'Молодец! Правильно!')
            ind = False
        else:
            await bot.send_message(message.chat.id, 'Неправильно! Подумай ещё.')

    elif 'новый город' in message.text.lower():
        city = maps.get_random_city()
        coordinates = maps.get_city_coordinates(city)
        maps.load_city_photo(*coordinates)

        await bot.send_photo(message.chat.id, photo=open(r'city.png', 'rb'), caption="Угадайте город")
        ind = True

    else:
        await bot.send_message(message.chat.id, 'Я вас не понимаю')


asyncio.run(bot.polling(none_stop=True))
