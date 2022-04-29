import pytest


# TODO [] - Помоему тут не правильное поле. Должно быть invested_amound
@pytest.mark.parametrize('json, keys, expected_data', [
    (
        {'full_amount': 10},
        ['full_amount', 'id', 'create_date'],
        {'full_amount': 10, 'id': 1},
    ),
    (
        {'full_amount': 5, 'comment': 'To you for chimichangas'},
        ['full_amount', 'id', 'create_date', 'comment'],
        {'full_amount': 5, 'id': 1, 'comment': 'To you for chimichangas'},
    ),
])
def test_create_donation(user_client, json, keys, expected_data):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 200, (
        'При создании доната должен возвращаться статус-код 201'
    )
    data = response.json()
    assert sorted(list(data.keys())) == sorted(keys), (
        f'При создании доната в ответе должны быть ключи `{keys}`'
    )
    data.pop('create_date')
    assert data == expected_data, (
        'При создании доната тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'comment': 'To you for chimichangas'},
    {'full_amount': -1},
    {'full_amount': None},
])
def test_create_donation_incorrect(user_client, json):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 422, (
        'При некорректном теле POST-запроса к эндпоинту `/donation/` в ответ '
        'должен вернуться статус-код 422.'
    )


def test_get_user_donation(user_client, dead_pool_donation):
    response = user_client.get('/donation/my')
    assert response.status_code == 200, (
        'При получении списка донатов пользователя должен возвращаться статус-код 200'
    )
    assert isinstance(response.json(), list), (
        'При получении списка донатов пользователя должен возвращаться объект типа `list`'
    )
    assert len(response.json()) == 1, (
        'При GET запросе для донатов пользователя список в ответе пуст. '
        'Это означает что фикстура не создала запись в базе данных, '
        'проверьте вашу модель `Donation`'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При получении списка донатов пользователя в ответе должны быть ключи `{keys}`'
    )
    # TODO [] - Почему тут поле full_amount?
    assert response.json() == [{
        'comment': 'To you for chimichangas',
        'create_date': '2019-09-24T14:15:22',
        'full_amount': 1000000,
        'id': 1,
    }], 'При получении списка донатов пользователя тело ответа API отличается от ожидаемого.'


def test_get_all_donations(superuser_client, donation):
    response = superuser_client.get('/donation/')
    assert response.status_code == 200, (
        'При получении списка всех донатов должен возвращаться статус-код 200'
    )
    assert isinstance(response.json(), list), (
        'При получении списка всех донатов должен возвращаться объект типа `list`'
    )
    assert len(response.json()) == 1, (
        'При GET запросе для всех донатов список в ответе пуст. '
        'Это означает что фикстура не создала запись в базе данных, '
        'проверьте вашу модель `Donation`'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
        'user_email',
        'invested_amount',
        'fully_invested',
        'close_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При получении списка всех донатов в ответе должны быть ключи `{keys}`'
    )
    assert response.json() == [{
        'close_date': '2019-08-24T14:15:22',
        'comment': 'To you for chimichangas',
        'create_date': '2019-09-24T14:15:22',
        'full_amount': 1000000,
        'fully_invested': False,
        'id': 1,
        'invested_amount': 0,
        'user_email': 'evil@pool.com',
    }], 'При получении списка всех донатов тело ответа API отличается от ожидаемого.'
