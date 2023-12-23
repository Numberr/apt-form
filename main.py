import requests
import re
from fake_useragent import UserAgent
from loguru import logger
import random
import time

time_for_sleep = [30,80]

def read_file(file_path):
    with open(file_path, 'r') as f:
        return [obj.strip() for obj in f.readlines()]
    
def sleep():
    randomm = random.randint(time_for_sleep[0], time_for_sleep[1])
    logger.info(f'''Спим {randomm} секунд
                ''')
    time.sleep(randomm)
    
wallets = read_file('wallets.txt')
proxies = read_file('proxies.txt')

for current_index, wallet in enumerate(wallets):
    logger.info(f'Текущий кошелек: {wallet}, номер: {current_index + 1}')

    proxy = proxies[current_index]
    req = requests.get('https://docs.google.com/forms/d/e/1FAIpQLSdqJ85C1YS_wQjKJjtavmit9v4pEtexgKblbwc-2M6q5IwCxg/viewform')
    page = req.text
    resid = str(re.search('name="fbzx" value="(.*?)">', page).group(1))

    headers = {
    'authority': 'docs.google.com',
    'accept-language': 'ru,en;q=0.9,ru-RU;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://docs.google.com',
    'pragma': 'no-cache',
    'referer': f'https://docs.google.com/forms/d/e/1FAIpQLSdqJ85C1YS_wQjKJjtavmit9v4pEtexgKblbwc-2M6q5IwCxg/viewform?fbzx={resid}',
    'user-agent': UserAgent().random,
    }
    current_proxy = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    data = {
        'entry.908064693': f'{wallet}',
        'fvv': '1',
        'partialResponse': f'[null,null,"{resid}"]',
        'pageHistory': '0',
        'fbzx': f'{resid}',
    }

    try:
        response = requests.post('https://docs.google.com/forms/u/0/d/e/1FAIpQLSdqJ85C1YS_wQjKJjtavmit9v4pEtexgKblbwc-2M6q5IwCxg/formResponse',
                                headers=headers,
                                data=data,
                                proxies=current_proxy)
        
        if response.status_code != 200:
            logger.error(f'''Форма для кошелька {wallet} не заполнена''')
            with open('errors.txt', 'a', encoding='utf-8') as r:
                r.write(f'{wallet}\n')
            sleep()
        else:
            logger.success(f'''{wallet} заполнен''')
            sleep()
    except Exception:
        logger.error(f'''Форма для кошелька {wallet} не заполнена''')
        with open('errors.txt', 'a', encoding='utf-8') as r:
            r.write(f'{wallet}\n')