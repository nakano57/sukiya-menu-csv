import traceback
import requests
import csv
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime
import traceback

dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

base = "https://www.sukiya.jp/"

url = "https://www.sukiya.jp/menu/in/gyudon/"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
lnav = soup.find(id='local_nav').find('dl')

menu_urls = []
for item in lnav.find_all('dd', class_='hd'):
    menu_urls.append(base+item.find('a').get('href'))

menu_urls = [x for x in menu_urls if not ('out' in x)]


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
    # writer.writerow(['#Last Update:'+str(dt_now)])
    writer.writerow(['#menu_name', 'category', 'price',
                     'kcal', 'protein', 'fat', 'carbohydrate', 'sodium'])

    for u in urls:
        res = requests.get(u.replace('index.html', 'nutrient.html'))
        soup = BeautifulSoup(res.text, 'html.parser')

        base_menu_name = soup.find(
            'div', class_='heading hd_first').find('h1').text
        sec = soup.find('div', id='sec_dish_nums')

        category = urlparse(u).path.split('/')[4]
        # print(category)

        for clr, tr in zip(sec.find_all('li', class_='clr'), soup.find('table').find_all('tr')[1:]):
            menu_name = base_menu_name + clr.find('dt').get_text(strip=True)
            price = clr.find('dd', class_='price').find(
                'em').get_text(strip=True)

            ###########名前CHECK############
            if base_menu_name == tr.find('th').text.replace('（店内メニュー）', ''):
                table_menu_name = base_menu_name
            else:
                table_menu_name = base_menu_name + \
                    tr.find('th').text.replace('（店内メニュー）', '')

            if table_menu_name != menu_name:
                print(menu_name, table_menu_name)
                try:
                    raise Exception
                except:
                    traceback.print_exc()
                    sys.exit(1)
            ###########CHECKおわり############

            td = tr.find_all('td')
            if td:
                kcal = int(td[0].text.rstrip(' kcal').replace(',', ''))
                protein = td[1].text.rstrip(' g')
                fat = td[2].text.rstrip(' g')
                carbohydrate = td[3].text.rstrip(' g')
                sodium = td[4].text.rstrip(' g')

            writer.writerow([menu_name, category, price, kcal,
                             protein, fat, carbohydrate, sodium])
