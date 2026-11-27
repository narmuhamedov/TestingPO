import requests

BASE_URL = 'http://127.0.0.1:8000'


def test_create_task():
    payload = {'title': 'Сходить в кино', 'completed': False}
    response = requests.post(f'{BASE_URL}/tasks', json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data['title'] == payload['title']
    assert data['completed'] is False
    assert "id" in data


def test_get_tasks():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_task():
    create_res = requests.post(f'{BASE_URL}/tasks', json={'title': 'Старое название'})
    task_id = create_res.json()['id']

    update_payload = {'title': 'Новое название', 'completed': True}
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Новое название'
    assert data['completed'] is True


def test_delete_task():
    create_res = requests.post(f'{BASE_URL}/tasks', json={'title': 'Задача на удаление'})
    task_id = create_res.json()['id']

    del_response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert del_response.status_code == 204

    get_response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert get_response.status_code == 404


# negative tests

def test_get_nonexistent_task():
    response = requests.get(f'{BASE_URL}/tasks/99999')
    assert response.status_code == 404
    assert response.json()['detail']


def test_create_task_empty_title():
    response = requests.post(f'{BASE_URL}/tasks', json={'title': "   "})
    assert response.status_code == 400


def test_create_task_invalid_data_type():
    response = requests.post(f'{BASE_URL}/tasks', json={'title': 'Тест', 'completed': 'not_a_boolean'})
    assert response.status_code == 422
