import requests
import fake_useragent
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup
from config import cookie
import sys
import time


async def findrm(username):
    link = f"https://wfts.su/game_history/{username}"
    user = fake_useragent.UserAgent().random

    header = {
        'user-agent': user,
        'cookie': cookie
    }
    results = []
    responce = requests.get(link, headers=header).text
    soup = BeautifulSoup(responce, 'lxml')
    for number in range(15):
        match = soup.find_all(class_="match")[number]
        rmmap = match.find(class_="mi-name").text
        rmmode = match.find(class_="mi-mode").text
        rmkd = match.find(class_="mi-kd").text

        findclass = match.find(class_="mi-icon-class")
        gameclass = findclass.get('style')

        if gameclass == 'background-image: url(/images/class0.png)':
            playclass = "⚔"
        elif gameclass == 'background-image: url(/images/class1.png)':
            playclass = "💉"
        elif gameclass == 'background-image: url(/images/class2.png)':
            playclass = "⚙"
        elif gameclass == 'background-image: url(/images/class3.png)':
            playclass = "🚬"
        else:
            playclass = "🗑"

        if not match.find(class_="mi-status status-lose"):
            result = f'\U00002747WIN  '
        elif rmmode == 'Мясорубка':
            result = f'\U00002b50MEAT'
        elif rmmode == 'Выживание':
            result == f'\U00002b50MEAT'
        else:
            result = f'\U0000274cLOSE'
        results.append(f"<b>{result}</b>  {playclass}  У/С: <b>{rmkd}</b> - <em>{rmmode}:{rmmap}</em> \n")
    results_str = ''
    for number in results:
        results_str += number
    lastgame = soup.find_all(class_="match")[0]
    rmdata = lastgame.find(class_="mi-date").text
    rmtime = lastgame.find(class_="mi-date-time").text
    rmstats = f"<b>Статистика последних 15 матчей: {username}</b>\n" \
              f"<em>Последняя игра {rmdata} в {rmtime} по МСК</em>\n" \
              f"⚔ - <b>Штурм</b>  💉 - <b>Мед</b>  ⚙ - <b>Инж</b>  🚬 - <b>Снап</b>  🗑 - <b>СЭД</b>\n\n" \
              f"{results_str}\n"
    return rmstats


async def statsfind(finduser):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}

    link = f"https://wfts.su/pvp/{finduser}"

    responce = requests.get(link, headers=header).text
    soup = BeautifulSoup(responce, 'lxml')

    checkfind = soup.find('div', class_="content")
    stats = []
    if checkfind.find_all('a')[0].text == "Поиск":
        block = soup.find('div', class_="statistics-block")

        shots = block.find_all('span')[3].text.replace(' ', '')
        shotshit = block.find_all('span')[5].text.replace(' ', '')

        stats.append(soup.find('td', class_='nickname').text)
        if int(shots) != 0:
            avgshots = (int(shotshit) / int(shots)) * 100
        else:
            avgshots = 0

        stats.append(f"<b>Никнейм:</b> {soup.find('td', class_='nickname').text}\n"
                     f"<b>{soup.find('td', class_='server').text}</b>\n"
                     f"<em>Статистика PVP матчей:</em>\n"
                     f"<b>Убийства/смерти:</b> {block.find_all('span')[17].text}\n"
                     f"<b>Процент попаданий:</b> {round(avgshots, 2)}%\n"
                     f"<b>Сыграно матчей:</b> {block.find_all('span')[25].text}\n"
                     f"<b>Процент побед:</b> {block.find_all('span')[33].text}\n"
                     f"<b>Время в игре:</b>{block.find_all('span')[39].text}\n"
                     f"<em>Здесь могла бы быть ваша реклама @tol9h4ik</em>\n"
                     f"<em>Так же рекомедую войти в чат @WFstats</em>\n"
                     f"<em>Учавствуй в ежедневной лотереи /ready</em>")
    else:
        stats.append("Игрок не найден или его статистика скрыта")

    return stats

def full_stats():
    link = f"https://wfts.su/match_page?id=3719daafb549dabc_16229cba"
    user = fake_useragent.UserAgent().random

    header = {
        'user-agent': user,
        'cookie': cookie
    }
    responce = requests.get(link, headers=header).text
    soup = BeautifulSoup(responce, 'lxml')
    result = soup.find(class_="hmatch-statistics")



    return result.contents

print(full_stats())

