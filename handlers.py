from main import bot, dp, anti_flood
from aiogram.types import Message
from config import admin_id
from lottery import pincodes
from sqlite import SQLight, SQLrand
from rmfind import findrm, statsfind
from keyboards.keyboards import menu
import datetime
import random


async def sand_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="bot started")


db = SQLight('db/db.db')
dbrand = SQLrand('db/rand.db')


@dp.message_handler(commands=['start'])
async def start_message(message: Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)

    await message.reply("<b>Привет!</b>\n"
                        "Это бот для получения статистики игроков\n"
                        "<em>Все что тебе нужно сделать это написать никнейм.</em>\n"
                        "Ты подписался на рассылу, что бы отписаться /unsubscribe\n"
                        "Так же тут ежедневно проходят розыгрыши пинов, для участия /ready\n"
                        "Информация о боте /help", reply_markup=menu)


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)

    await message.answer("<em>Вы успешно подписались на рассылки</em>")


@dp.message_handler(commands=['help'])
async def help(message: Message):
    all_users = db.get_all_subscriptions()
    all_users_rand = dbrand.get_users()
    sum_user = 0
    sum_user_rand = 0
    for u in all_users:
        sum_user += 1

    for u in all_users_rand:
        sum_user_rand += 1

    await message.answer(f'<b>Информация о боте</b>\n'
                         f'<em>Количество пользователей:</em> <b>{sum_user}</b>\n\n'
                         f'/ready что бы принять участие в ежедневном розыгрыше пинкодов, '
                         f'<em>Сегодня приняли участие:</em> <b>{sum_user_rand}</b> <em>человек</em>\n\n'
                         f'@WFstats - чат где можно пообщаться\n\n'
                         f'<em>Что бы узнать статистику игрока просто напишите его никнейм</em>', reply_markup=menu)


@dp.message_handler(commands=['spam'])
async def spam(message: Message):
    if message.from_user.id == admin_id:
        subscribeers = db.get_subscriptions()
        spamtext = message.text.replace('/spam ', '')
        for s in subscribeers:
            try:
                await bot.send_message(s[1], text=spamtext)
            except Exception:
                file = open('logs/subslog.txt', 'a', encoding='utf-8')
                file.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")}      {s[0]} {s[1]} отписался\n')
                file.close()
    else:
        await message.answer("<b>Это команда только для админа, соре...</b>")


@dp.message_handler(commands=['spam_all'])
async def spam_all(message: Message):
    if message.from_user.id == admin_id:
        subscribeers = db.get_all_subscriptions()
        spamtext = message.text.replace('/spam_all ', '')
        for s in subscribeers:
            try:
                await bot.send_message(s[1], text=spamtext)
            except Exception:
                file = open('logs/allsubslog.txt', 'a', encoding='utf-8')
                file.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")}      {s[0]} {s[1]} отписался\n')
                file.close()
    else:
        await message.answer("<b>Это команда только для админа, соре...</b>")


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        await message.answer("<em>Вы и так отписаны</em>")
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("<em>Вы отписались от рассылок</em>")


@dp.message_handler(commands=['ready'])
async def ready(message: Message):
    timenow = datetime.datetime.now()
    delta = timenow + datetime.timedelta(hours=5)
    hourready = 23 - delta.hour
    minuteredy = 59 - timenow.minute
    if not dbrand.user_exists(message.from_user.id):
        dbrand.add_user(message.from_user.id, True)

    await message.answer(f'<b>Вы приняли участие в ежедневном розыгрыше пинов</b>\n'
                         f'<em>До начала розыгрыша: {hourready} часов {minuteredy} минут</em>\n'
                         f'Делать больше ничего не нужно, если вы победите бот отправит вам пин-код', reply_markup=menu)


@dp.message_handler(commands=['run'])
async def run(message: Message):
    if message.from_user.id == admin_id:
        users = dbrand.get_users()
        arr_users = []
        wins = []
        for u in users:
            arr_users.append(u[1])

        for number in range(10):
            wins.append(random.choice(arr_users))

        for number in range(10):
            go = number - 1
            try:
                await bot.send_message(wins[go],
                                       text=f'Поздравляю ты победил в ежедневном розыгрыше вот твой пинкод:'
                                            f' {pincodes[go]}')
                await bot.send_message(admin_id, text=f'Юзер {wins[go]} получил свой пинкод: {pincodes[go]}')
            except Exception:
                await bot.send_message(admin_id, text=f'Юзер {wins[go]} не получил свой пинкод: {pincodes[go]}')
        dbrand.deliteusers()
    else:
        await message.answer("<b>Это команда только для админа, соре...</b>")


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=5)
async def echo(message: Message):
    if message.text == 'Помощь':
        await help(message)
    elif message.text == 'Розыгрыш':
        await ready(message)
    else:
        await message.answer("<em>Выполняется поиск, подождите...</em>", reply_markup=menu)
        finduser = message.text
        try:
            stats = await statsfind(finduser)
            if len(stats) < 2:
                await bot.send_message(message.from_user.id, text="Игрок не найден или его статистика скрыта")
                return 0
        except Exception:
            await bot.send_message(message.from_user.id, text="Игрок не найден или его статистика скрыта")
            return 0
        username = stats[0]
        await message.answer(text=stats[1])
        rmstats = await findrm(username)
        await message.answer(text=rmstats)
        file = open('logs/log.txt', 'a', encoding='utf-8')
        file.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")} {message}\n')
        file.close()