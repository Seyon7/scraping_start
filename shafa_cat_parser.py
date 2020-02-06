import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
base_url = 'https://shafa.ua/zhenskie-sportivnye-progulochnye-kostyumy.xhtml'

def parse_prom(base_url: str, headers: dict) -> list:
    data = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        cards = soup.find_all('li', attrs={'class': 'b-catalog__item'})
        for card in cards:
            # Вытягиваем имя товара и превращаем в string
            name = card.find('span', attrs={'class': 'b-tile-item__title'}).text

            # Вытягиваем актуальную цену. Если есть старая цена, то ищем по другому классу. Получаем str
            curr_price = card.find('span', attrs={'class': 'b-tile-item__price'})
            if curr_price is None:
                curr_price = card.find('span', attrs={'class': 'x-gallery-tile__price x-gallery-tile__price_color_red', 'data-qaid': 'product_price'}).text
            else:
                curr_price = curr_price.text

            # Убираем пробелы и лишние символы в цене
            if curr_price.find('\u2009') != -1:
                curr_price = curr_price.replace('\u2009', '')
            elif curr_price.find('грн') != -1:
                curr_price = curr_price.replace('грн', '')

            if curr_price.find(' ') != -1:
                curr_price = curr_price.replace(' ', '')

            # Если есть старая цена - вытягиваем её как str, если нет - указываем None
            old_price = card.find('span', attrs={'class': 'b-tile-item__price-old'})
            if old_price is None:
                old_price = 'None'
            else:
                old_price = old_price.text

            # Убираем пробелы и лишние символы в цене
            if old_price.find('\u2009') != -1:
                old_price = old_price.replace('\u2009', '')
            elif old_price.find('грн') != -1:
                old_price = old_price.replace('грн', '')

            if old_price.find(' ') != -1:
                old_price = old_price.replace(' ', '')

            # Добавляем все в список и возвращаем его
            data.append((name.strip(), old_price.strip(), curr_price.strip()))
        return data
    else:
        print('ERROR')


dataset = parse_prom(base_url, headers)
for i in dataset:
    print(i[0] + ';' + i[1] + ';' + i[2])

# with open('shafa_cat_parse.txt', 'w') as file:
#     for el in dataset:
#         file.write(el[0] + ';' + el[1] + ';' + el[2] + '\n')
