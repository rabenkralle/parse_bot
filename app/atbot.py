from parse_web import logging_site, parse_site, make_addr_dict
import logging
import asyncio
import config

from sqlighter import SQLighter

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = config.API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')
db.create()



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    
    newline = "\n"
    """
    Это сообщение будет выходить при вызове команды /start или /help
    """
    await message.reply(f''' 
    Привет. Это *****!
    Подпишись на меня и тогда тебе будут приходить сообщения о поступлении товара.
    Также в любой момент ты можешь проверить наличие товара в магазине.
    Для этого тебе просто надо отправить сообщение с цифрой из списка:
    
    {newline.join(f"{key}: {value}" for key, value in name_dict.items())}
    
    Удачи!
                            ''')

# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на парсер!")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):

    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("*****")


# Вход на сайт
def login_site():
    global br
    br = logging_site()

# Функция создания словаря с адресами
def addr_dict():
    login_site()
    return make_addr_dict(config.addr_search, br)

# Функция создания списка товаров
def make_name_dict(addr):
    name_dict = {}
    for i in range(1,len(addr) + 1 ):
        name_check, __, __, __ = parse_site(addr[i], br)
        name_dict[i] = name_check
    return name_dict

# Проверяем наличие товара в магазине в данный момент
@dp.message_handler()
async def choose_parse(message: types.Message):

    input_parse = message.text
    # print(input_parse) # для проверки работы парсера
    if int(input_parse) in addr:
        try:
            login_site()
            name_check, in_stock_check, price_check, button_check = parse_site(addr[int(input_parse)], br)
        except:
            name_check, in_stock_check, price_check, button_check = parse_site(addr[int(input_parse)], br)

        print(name_check, in_stock_check, addr[int(input_parse)], price_check) # для проверки вывода информации
        await message.answer(f'{name_check} {in_stock_check} {addr[int(input_parse)]} {price_check}€')

    else:
        await message.answer('Вы ошиблись в выборе.')

# Постоянный парсинг сайта на изменение списка товаров 
async def addr_checker(wait_for):
    global addr
    await asyncio.sleep(wait_for)
    try:
        login_site()
        addr = make_addr_dict(config.addr_search, br)
    except:
        addr = make_addr_dict(config.addr_search, br)

# Постоянный парсинг сайта до момента появления товара в наличии
async def scheduled(wait_for, addr):
    while True:
        await asyncio.sleep(wait_for)
        try:
            login_site()
            name_check, in_stock_check, price_check, button_check = parse_site(addr, br)
        except:
            name_check, in_stock_check, price_check, button_check = parse_site(addr, br)

        if in_stock_check == 'In stock' and button_check:
            subscriptions = db.get_subscriptions()
            for s in subscriptions:
                await bot.send_message(s[1], f'‼️‼️{name_check} {in_stock_check} {addr} {price_check}€‼️‼️')
        else:
            print(f'none {addr}') # для проверки работы программы



if __name__ == '__main__':
    addr = addr_dict()
    name_dict = make_name_dict(addr)

    loop = asyncio.get_event_loop()
    loop.create_task(addr_checker(200))
    for i in range(2, len(addr)+1):
        loop.create_task(scheduled(50, addr[i]))
    
    executor.start_polling(dp, skip_updates=True)
