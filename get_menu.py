import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime

dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

with open('menu.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["#Last Update"+str(dt_now)])
    writer.writerow(['#menu_name', 'category', 'price', 'kcal'])

    base = "https://www.sukiya.jp/"
    urls = []

    res = requests.get('https://www.sukiya.jp/menu/in/gyudon/')
    soup = BeautifulSoup(res.text, 'html.parser')
    # 牛丼
    for product in soup.find_all("div", class_="product_menu"):
        for i in product.find_all("li", class_="menu_item"):
            try:
                # print(i.find("a")['href'])
                urls.append(base + i.find("a")['href'])
            except TypeError as e:
                print(e)

    menu_urls = ['https://www.sukiya.jp/menu/in/tondon/',
                 'https://www.sukiya.jp/menu/in/sukimix/',
                 'https://www.sukiya.jp/menu/in/unagi/',
                 'https://www.sukiya.jp/menu/in/karubi/',
                 'https://www.sukiya.jp/menu/in/curry/',
                 'https://www.sukiya.jp/menu/in/don/',
                 'https://www.sukiya.jp/menu/in/special/',
                 'https://www.sukiya.jp/menu/in/kids/',
                 'https://www.sukiya.jp/menu/in/side/',
                 'https://www.sukiya.jp/menu/in/drink/']

    for url in menu_urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        product = soup.find("div", class_="sec_product_table")

        # それ以外
        for i in product.find_all("td", class_="cell_product"):
            try:
                print(i.find("a")['href'])
                urls.append(base + i.find("a")['href'])
            except TypeError as e:
                print(e)

    for u in urls:
        res = requests.get(u)
        soup = BeautifulSoup(res.text, 'html.parser')
        base_menu_name = soup.find(
            'div', class_='heading hd_first').find('h1').text
        sec = soup.find('div', id='sec_dish_nums')

        category = urlparse(u).path.split('/')[4]
        # print(category)

        for n in sec.find_all('li', class_='clr'):
            menu_name = base_menu_name + n.find('dt').get_text(strip=True)
            price = n.find('dd', class_='price').find(
                'em').get_text(strip=True)
            kcal = int(n.find('dd', class_='calorie').get_text(
                strip=True).strip('( kcal)').replace(',', ''))
            writer.writerow([menu_name, category, price, kcal])
