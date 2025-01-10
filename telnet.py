import requests
import json

# Указываем URL и учетные данные для доступа к Zabbix API
url = 'http://192.168.89.222:8088/api_jsonrpc.php'
headers = {'Content-Type': 'application/json-rpc'}
auth = ('a.zubrev', 'e2e4devilSonger')

# Формируем тело запроса для удаления элементов данных в состоянии "Не поддерживается"
data = {
    'jsonrpc': '2.0',
    'method': 'item.get',
    'params': {
        'filter': {
            'state': 1  # 1 - "Не поддерживается"
        },
        'output': 'extend'
    },
    'auth': None,
    'id': 1
}

# Отправляем запрос на получение элементов данных в состоянии "Не поддерживается"
response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))

try:
    items = response.json()['result']
    for item in items:
        item_id = item['itemid']
        delete_data = {
            'jsonrpc': '2.0',
            'method': 'item.delete',
            'params': [item_id],
            'auth': None,
            'id': 1
        }
        delete_response = requests.post(url, headers=headers, auth=auth, data=json.dumps(delete_data))
        print(delete_response.json())
except KeyError:
    print("Ошибка: ключ 'result' отсутствует в ответе от Zabbix API")