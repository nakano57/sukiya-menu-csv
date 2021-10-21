import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime

dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

base = "https://www.sukiya.jp/"

url = "https://www.sukiya.jp/menu/in/gyudon/"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
lnav = soup.find(id='lnav_menu_in')

menu_urls = []
for item in lnav.find_all('dd', class_='hd'):
    menu_urls.append(base+item.find('a').get('href'))


urls = []
for url in menu_urls:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    if soup.find_all("div", class_="product_menu") is not None:

        for product in soup.find_all("div", class_="product_menu"):
            for i in product.find_all("li", class_="menu_item"):
                try:
                    # print(i.find("a")['href'])
                    urls.append(base + i.find("a")['href'])
                except TypeError as e:
                    print(e)
    else:
        product = soup.find("div", class_="sec_product_table")

        for i in product.find_all("td", class_="cell_product"):
            try:
                print(i.find("a")['href'])
                urls.append(base + i.find("a")['href'])
            except TypeError as e:
                print(e)


with open('menu.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['#Last Update:'+str(dt_now)])
    writer.writerow(['#menu_name', 'category', 'price', 'kcal'])

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
