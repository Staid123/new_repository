import requests
import time


API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN: str = '6206897348:AAENqclh-o1SObNCLJV69uJCTL5VUVOgjUc'
ERROR_TEXT: str = 'Здесь должна была быть картинка с котиком :('

MAX_COUNTER: int = 1000

offset: int = -2
counter: int = 0
chat_id: int


while counter < MAX_COUNTER:

    print('attempt =', counter)  # Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            user_text: str = updates['result'][0]['message']['text']
            user_firstname: str = updates['result'][0]['message']['from']['first_name']
            print({user_firstname: user_text})
            if cat_response.status_code == 200:
                link_to_cats = cat_link = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={user_text} конечно хорошо, но вот картинки с котиками')
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={link_to_cats}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1
