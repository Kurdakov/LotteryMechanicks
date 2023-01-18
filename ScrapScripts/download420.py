from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from datetime import datetime
import locale
import csv
import time
import socket
import urllib.error


def parse_page(page_number):
    error = 0
    url = 'https://www.stoloto.ru/4x20/archive/{}'.format(page_number)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urlopen(request).read()
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout, ConnectionResetError) as error:
        return 1 , "", ""

    root = BeautifulSoup(html ,"html.parser")
    # Название, пример: "Результаты тиража № 1, 31 декабря 2016 в 15:10"
    title = root.select_one('#content > h1').text.strip()

    # Вытаскиваем дату, пример: "31 декабря 2016 в 15:10"
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    date_time_str = title.split(',  ')[1]
    date_time_str = date_time_str.replace(" в ", ' ')
    datetime_object = datetime.strptime(date_time_str, '%d %B %Y %H:%M')
    date_time_str = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

    # Вытаскиваем номера, пример: ['20', '2', '10', '4', '2', '16', '9', '17']
    numbers = [x.text.strip() for x in root.select('.winning_numbers > ul > li')]

    return error, date_time_str, numbers


max_page_number = 262252
min_page_number = 1
result = ''
socket.setdefaulttimeout(5)
# Перебор страниц от 1 до <max_page_number> включительно
error = 0
for page_number in range(min_page_number, max_page_number + 1):
    error, date_time_str, numbers = parse_page(page_number)
    while error:
        error, date_time_str, numbers = parse_page(page_number)

    # Список чисел преобразуем в строку:
    # ['20', '2', '10', '4', '2', '16', '9', '17'] -> '20 2 10 4 2 16 9 17'
    numbers = ','.join(numbers)
    str = "%d, %s, %s\n" % (page_number, numbers, date_time_str)

    with open('lotto4x20.csv', 'a', encoding='utf-8', newline='\n') as f:
        f.write(str)
    time.sleep(1)



