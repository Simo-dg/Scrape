from bs4 import BeautifulSoup
from datetime import datetime
import urllib3
http = urllib3.PoolManager()
from requests_html import HTMLSession
import sqlite3
import re
import time

COLOR_TRANSLATION = {
    'rosso': 'red',
    'productred': 'red',
    'blu': 'blue',
    'verde': 'green',
    'nero': 'black',
    'bianco': 'white',
    'viola': 'purple',
    'rosa': 'pink',
    'grigio':'spacegray',
    'argento':'silver',
    'giallo':'yellow',
    'grigio siderale':'spacegray',
    'grigio': 'spacegray',
    'oro': 'gold',
    'grafite': 'graphite',
    'azzurro':'blue'
}

hdr = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Accept": "*/*",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
    }

DATABASE_FILE_PATH = 'data.db'

def fetch_and_parse(url):
    with session.get(url) as response:
        response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def get_product_links(soup, codes):
    return ['https://www.backmarket.it' + soup.find('li', attrs={'data-qa': code}).find('a')['href'] for code in codes]

def get_color_links(soup, colors):
    return ['https://www.backmarket.it' + soup.find('li', attrs={'data-qa': color}).find('a')['href'] for color in colors]

def insert_into_db(conn, url,model, storage_capacity, color):
    match = re.search(pattern, url)
    if match:
        current_datetime = datetime.today()
        current_date = current_datetime.strftime('%Y-%m-%d')
        current_time = current_datetime.strftime('%H:%M:%S')
        conn.execute('''
            INSERT INTO scrapped_data (code, model, storage, color,date, time, price, marketplace, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (model + storage_capacity + color+'b', model, storage_capacity, color,current_date, current_time, None, "BackMarket", "IT"))
        conn.execute('''
            INSERT OR REPLACE INTO product_url (code, date, time, url)
            VALUES (?, ?, ?, ?)
        ''', (model + storage_capacity + color+'b', current_date, current_time, url))
    else:
        print("Pattern not found in the URL:", url)

def get_price_backmarket(soup):
    price = soup.find('div', {'data-test': 'normal-price'}).get_text(strip=True)
    return(float(''.join(filter(str.isdigit, price))) / 100)

def get_price_refurbed(soup):
    price_element = soup.find('div', class_='text-2xl leading-none text-emphasize-03')
    if price_element:
        price_text = price_element.get_text(strip=True)
        price_text = price_text.replace('.', '').strip()
        return float(price_text.replace('€', '').replace(',', '.').strip())
    return None

def get_region(url):
    pattern_region = 'www.[a-z]+.[a-z]+'
    region_match = re.search(pattern_region, url)
    return region_match.group()[-2:] if region_match else None

def get_options(soup, pattern):
    options = soup.find_all('option', {'value': re.compile(pattern)})
    return {option.text.strip(): option['value'] for option in options}



conn = sqlite3.connect(DATABASE_FILE_PATH)
with conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS product_url (
            code TEXT PRIMARY KEY,
            url TEXT,
            date TEXT,
            time TEXT
        )
    ''')
with conn:
    conn.execute('''
            CREATE TABLE IF NOT EXISTS scrapped_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        model TEXT,
        storage TEXT,
        color TEXT,
        date TEXT,
        time TEXT,
        price NUMERIC,
        marketplace TEXT,
        region TEXT
            )
        ''')
    
models = {
    'iphone11': {
        'pattern': r'/p/iphone-11+-(\d+)-go-(\w+)-'
    },
    'iphone11pro': {
        'pattern': r'/p/iphone-11-pro+-(\d+)-go-(\w+)-'
    },
    'iphone12': {
        'pattern': r'/p/iphone-12+-(\d+)-go-(\w+)-'
    },
    'iphone12pro': {
        'pattern': r'/p/iphone-12-pro+-(\d+)-go-(\w+)-'
    },
    'iphonex': {
        'pattern': r'/p/iphone-x+-(\d+)-go-(\w+)-'
    },
    'iphone13pro': {
        'pattern': r'/p/iphone-13-pro+-(\d+)-go-(\w+)-'
    },
    'iphone13': {
        'pattern': r'/p/iphone-13+-(\d+)-go-(\w+)'
    }
}

session = HTMLSession()
conn = sqlite3.connect(DATABASE_FILE_PATH)

for model, data in models.items():
    url = 'https://www.backmarket.it/it-it/search?q='+model
    soup = fetch_and_parse(url)
    url2 = 'https://www.backmarket.it' + soup.find('div', class_='productCard').find('a', class_='focus:outline-none group md:box-border relative')['href']
    soup = fetch_and_parse(url2)
    ottimo_element = soup.find(lambda tag: tag.name == 'span' and 'Ottimo' in tag.text)
    url3 = []
    if ottimo_element:
        a_element = ottimo_element.find_parent('a')
        if a_element:
            url3.append('https://www.backmarket.it'+a_element['href'])
            
    linkgb = []
    for link in url3:
        soup = fetch_and_parse(link)
        li_elements = soup.find_all('li', class_='mb-3')
        for li_element in li_elements:
            gb_element = li_element.find('span', text=lambda text: text and 'GB' in text)
            if gb_element:
                a_element = gb_element.find_parent('a', href=True)
                if a_element:
                    linkgb.append(a_element['href'])

    result_dict = {}
    for link in linkgb:
        url = 'https://www.backmarket.it' + link
        soup = fetch_and_parse(url)
        li_elements = soup.find_all('li', class_='mb-3')
        for li_element in li_elements:
            span_element = li_element.find('span', class_='text-center')
            if span_element:
                color = span_element.get_text(strip=True)
                a_element = li_element.find('a')
                if a_element is not None:
                    link = a_element['href']
                    pattern = data['pattern']
                    match = re.search(pattern, link)
                    if match:
                        storage_capacity = match.group(1)
                        result_dict[color+' '+storage_capacity] = {'link': link, 'storage_capacity': storage_capacity}
    with conn:
        for color, data in result_dict.items():
            url = 'https://www.backmarket.it' + data['link']
            storage_capacity = data['storage_capacity']
            color = color.lower().split(' ')[0]
            color = COLOR_TRANSLATION.get(color, color)
            insert_into_db(conn, url,model, storage_capacity, color)
        conn.commit()
    time.sleep(60)

models = {'iphone-x': r'/p/iphone-x/\d{4,5}',
          'iphone-11': r'/p/iphone-11/\d{4,5}',
          'iphone-12': r'/p/iphone-12/\d{4,5}',
          'iphone-13': r'/p/iphone-13/\d{4,5}',
          'iphone-14': r'/p/iphone-14/\d{4,5}',
          'iphone-11-pro': r'/p/iphone-11-pro/\d{4,5}',
          'iphone-12-pro': r'/p/iphone-12-pro/\d{4,5}',
          'iphone-13-pro': r'/p/iphone-13-pro/\d{4,5}',
          'iphone-14-pro': r'/p/iphone-14-pro/\d{4,5}'}

known_colors = ['bianco', 'blu', 'nero', 'rosso', 'verde', 'viola','rosa','giallo','argento','grigio siderale','oro','grigio']

for key,pattern in models.items():
    model = key.replace('-','')
    url = 'https://www.refurbed.it/p/'+key
    
    if model in ['iphone14', 'iphone14pro']:
        base_urls = [url]
    else:
        soup = fetch_and_parse(url)
        very_good_options = soup.find_all('option', string=lambda text: 'Molto buono' in text)
        if very_good_options:
            values = [option.get('value') for option in very_good_options]
            base_urls = ['https://www.refurbed.it' + value for value in values]
        else:
            continue
        
    for base_url in base_urls:
        soup = fetch_and_parse(base_url)
        linkr = get_options(soup, pattern)
        colors_link = {color: 'https://www.refurbed.it' + link if link.startswith('/p/') else link for color, link in linkr.items() if color in known_colors}
        linkgb = {} 
        for key, value in colors_link.items():
            soup = fetch_and_parse(value)
            options = get_options(soup, pattern)
            linkgb.update({key+option: link for option, link in options.items() if 'GB' in option})

    filtered_keys = {key: link for key, link in linkgb.items() if 'GB' in key}

    with conn:
        for key, value in filtered_keys.items():
            color, storage_capacity = re.match(r'(\D+)(\d+)\s*GB', key).groups()
            url = 'https://www.refurbed.it' + value

            current_datetime = datetime.today()
            current_date = current_datetime.strftime('%Y-%m-%d')
            current_time = current_datetime.strftime('%H:%M:%S')
            color = COLOR_TRANSLATION.get(color, color)

            conn.execute('''
            INSERT INTO scrapped_data (code, model, storage, color, date, time, price, marketplace, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (model + storage_capacity + color + 'r', model, storage_capacity, color, current_date, current_time, None, "Refurbed", 'IT'))

            conn.execute('''
            INSERT OR REPLACE INTO product_url (code, date, time, url)
            VALUES (?, ?, ?, ?)
        ''', (model + storage_capacity + color + 'r', current_date, current_time, url))

price_extractors = {
    'www.backmarket.it/it-it': get_price_backmarket,
    'www.refurbed.': get_price_refurbed
}

with conn:
    url_query = conn.execute("SELECT code, url FROM product_url")
    urls = url_query.fetchall()

for code, url in urls:
    try:
        price = None
        with session.get(url, headers=hdr) as response:
            response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        region = get_region(url)

        for website, extractor in price_extractors.items():
            if website in url:
                price = extractor(soup)
                break

        with conn:
            conn.execute('''
                UPDATE scrapped_data
                SET price = ?
                WHERE code = ?
            ''', (price, code))
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
conn.close()