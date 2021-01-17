import requests
from bs4 import BeautifulSoup

URL = "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G06"

res = requests.get(URL)
if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')
    cards = soup.select('.best-list')[1].select('ul > li')

    for index, card in enumerate(cards):
        title = card.select_one('.itemname')
        price = card.select_one('.s-price > strong')

        res_info = requests.get(title['href'])
        if res_info.status_code == 200:
            soup_info = BeautifulSoup(res_info.content, 'html.parser')
            provider_info = soup_info.select_one('.text__seller > a')

            print(index + 1, title.get_text(),
                  price.get_text(), provider_info.get_text())
