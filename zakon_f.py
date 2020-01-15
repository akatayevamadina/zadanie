import csv
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from bs4 import SoupStrainer

headers ={'accept': '*/*',
          'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
base_url = 'https://www.zakon.kz/news'
def z_parser (base_url, headers):
    spisok=[]
    kom1=''
    session = requests.Session()
    request=session.get (base_url, headers=headers)
    if request.status_code==200:
        soup=bs(request.content, 'lxml')
        divs = soup.find_all('div', {"class": "cat_news_item"})
        for div in divs:
            try:
                title=div.find('a', {"class": "tahoma font12"}).text
                kom=div.find('span', {"class":"comm_num"})
                if div.find('span', {"class":"comm_num"})==None:
                    kom1='0'
                else:
                    kom1=kom.text

                spisok.append({'title':title,  'kom':kom1})
            except AttributeError:
                continue
        print(spisok)
    else:
        print('Error')
    return spisok
def file_write (spisok):
    with open('zakon.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Заголовок статьи', 'Количество комментариев'))
        for i in spisok:
            a_pen.writerow((i['title'], i['kom']))

spisok=z_parser(base_url , headers)
file_write(spisok)

