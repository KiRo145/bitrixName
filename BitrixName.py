import requests


def get_all_smart_process_items():
    all_items = []
    start = 0
    limit = 50  # Количество элементов на странице

    while True:
        url = 'https://bitrix.aliton.ru/rest/2460/0wgpqk9iyrtl5t8r/crm.item.list.json?entityTypeId=164'
        params = {
            'select': ['title', 'id', 'ufCrm44_1706138158'],
            'start': start
        }

        # Отладочный вывод вебхука
        print(f"Sending request to: {url} with params: {params}")

        response = requests.post(url, json=params)

        # Выводим статус ответа и его содержимое для отладки
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response Data: {data}")  # Отладочный вывод данных ответа

            items = data.get('result', {}).get('items', [])
            all_items.extend(items)

            if len(items) < limit:
                break

            start += limit
        else:
            print(f"Error fetching items: {response.status_code} - {response.text}")
            break

    return all_items


def filter_and_update_items(items):
    filtered_items = []

    for item in items:
        if item.get('title') == 'ЛО, , . , д. , ':  # Фильтруем по нужному значению title
            # Заменяем title на значение из ufCrm44_1706138158
            item['title'] = item.get('ufCrm44_1706138158', item['title'])
            filtered_items.append(item)

    return filtered_items


def update_items_in_bitrix(items):
    url = 'https://bitrix.aliton.ru/rest/2460/0wgpqk9iyrtl5t8r/crm.item.update.json?entityTypeId=164'

    for item in items:
        update_params = {
            'id': item['id'],
            'fields': {
                'title': item['title']
            }
        }
        response = requests.post(url, json=update_params)

        # Добавлен отладочный вывод ID элемента
        print(f"Attempting to update item with ID: {item['id']} and new title: {item['title']}")

        if response.status_code == 200:
            print(f"Updated item with ID {item['id']} successfully.")
        else:
            print(f"Failed to update item with ID {item['id']}: {response.text}")


# Пример вызова функции
if __name__ == "__main__":
    items = get_all_smart_process_items()
    print(f"Total items fetched: {len(items)}")

    updated_items = filter_and_update_items(items)
    print(f"Filtered and updated items count: {len(updated_items)}")

    # Обновляем элементы в Битрикс24
    update_items_in_bitrix(updated_items)
