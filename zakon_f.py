#загрузка библиотек
import csv #для создания файла
import requests # отправка запросов
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from bs4 import SoupStrainer
import socket
import socks


#запрос через браузер
headers ={'accept': '*/*',
          'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
base_url = 'https://www.zakon.kz/news'#адрес рабочей сраницы
date1=[]
def z_parser (base_url, headers):# функция для парсинга
    spisok=[]
    kom1=''
    session = requests.Session()# запрос к странице
    request=session.get (base_url, headers=headers)
    if request.status_code==200:#если соединение установлено
        soup=bs(request.content, 'lxml')
        #поиск даты
        date = soup.find_all('span', {"class": "tahoma font12 date n2"})
        date1.append(date)

        divs = soup.find_all('div', {"class": "cat_news_item"})
        for div in divs:
            #обработка исключений для метода text
            try:
                #поиск заголовков статей
                title=div.find('a', {"class": "tahoma font12"}).text
                # поиск колличества комметариев
                kom=div.find('span', {"class":"comm_num"})
                if div.find('span', {"class":"comm_num"})==None:#если комм-я нет, запсать 0
                    kom1='0'
                else:
                    kom1=kom.text #если есть записать кол-во комм-ев
                spisok.append({'title':title,  'kom':kom1})# добавляет в список заголовки и кол-во комм-ев
            except AttributeError:
                continue
        print(spisok)#ввод списка
    else:
        print('Error')#при отсутвии соединения со страницей печать Error
    return spisok
#функция для записи в файл
def file_write (spisok):
    with open('zakon.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(date1)
        a_pen.writerow(('Заголовок статьи', 'Количество комментариев'))
        for i in spisok:
            a_pen.writerow((i['title'], i['kom']))

spisok=z_parser(base_url , headers)
file_write(spisok)
