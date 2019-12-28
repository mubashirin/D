import requests
import time
import sys

auth_params = {
    'key': '06d82c41882bb7964c316697321d3e27',
    'token': 'b87bafa8f68006bb2d5abf64ad2a572dc6d8a19f44426a72716dd0d36f4b0a94'
}

url = 'https://api.trello.com/1/{}'
board_id = '6hj6bh7e'

def read():
    column_data = requests.get(url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        print(column['name'])

        task_data = requests.get(url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        if not task_data:
            print('\t' + 'Нет задач!')
            continue

        for task in task_data:
            print('\t' + task['name'])

def create(name, column_name):
    column_data = requests.get(url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        if column['name'] == column_name:
            requests.post(url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

def move(name, column_name):
    column_data = requests.get(url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id = None
    for column in column_data:
        column_tasks = requests.get(url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    for column in column_data:
        if column['name'] == column_name:
            requests.put(url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
