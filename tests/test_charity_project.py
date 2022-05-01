import pytest


def test_get_charity_project(user_client, charity_project):
    response = user_client.get('/charity_project/')
    assert response.status_code == 200, (
        'При GET запросе для проекта должен возвращаться статус-код 200'
    )
    assert isinstance(response.json(), list), (
        'При GET запросе для проекта должен возвращаться объект типа `list`'
    )
    assert len(response.json()) == 1, (
        'При GET запросе для проекта список в ответе пуст. '
        'Это означает что фикстура не создала запись в базе данных, '
        'проверьте вашу модель `CharityProject`'
    )
    data = response.json()[0]
    keys = sorted([
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
        'close_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При GET запросе для проекта в ответе должны быть ключи `{keys}`'
    )
    assert response.json() == [{
        'close_date': '2019-08-24T14:15:22',
        'create_date': '2019-08-24T14:15:22',
        'description': 'Huge fan of chimichangas. Wanna buy a lot',
        'full_amount': 1000000,
        'fully_invested': False,
        'id': 1,
        'invested_amount': 0,
        'name': 'chimichangas4life',
    }], 'При GET запросе для проекта тело ответа API отличается от ожидаемого.'


def test_get_all_charity_project(user_client, charity_project, charity_project_nunchaku):
    response = user_client.get('/charity_project/')
    assert response.status_code == 200, (
        'При получении всех проектов должен возвращаться статус-код 200'
    )
    assert isinstance(response.json(), list), (
        'При получении всех проектов должен возвращаться объект типа `list`'
    )
    assert len(response.json()) == 2, (
        'При получении всех проектов список в ответе пуст. '
        'Это означает что фикстура не создала запись в базе данных, '
        'проверьте вашу модель `CharityProject`'
    )
    data = response.json()[0]
    keys = sorted([
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
        'close_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При получении всех проектов в ответе должны быть ключи `{keys}`'
    )
    assert response.json() == [
        {
            'close_date': '2019-08-24T14:15:22',
            'create_date': '2019-08-24T14:15:22',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life',
        },
        {
            'close_date': '2019-08-24T14:15:22',
            'create_date': '2019-08-24T14:15:22',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
            'fully_invested': False,
            'id': 2,
            'invested_amount': 0,
            'name': 'nunchaku',
        }], 'При получении всех проектов тело ответа API отличается от ожидаемого.'


def test_create_charity_project(superuser_client):
    response = superuser_client.post('/charity_project/', json={
        'name': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
        'full_amount': 1000000,
    })
    assert response.status_code == 200, (
        'При создании проекта должен возвращаться статус-код 200'
    )
    data = response.json()
    keys = sorted([
        'name',
        'description',
        'full_amount',
        'create_date',
        'fully_invested',
        'id',
        'invested_amount',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При создании проекта в ответе должны быть ключи `{keys}`'
    )
    data.pop('create_date')
    assert data == {
        'description': 'Deadpool inside',
        'full_amount': 1000000,
        'fully_invested': False,
        'id': 1,
        'invested_amount': 0,
        'name': 'Мертвый Бассейн',
    }, 'При создании проекта тело ответа API отличается от ожидаемого.'


@pytest.mark.parametrize('json', [
    {
        'name': 'Мертвый Бассейн',
        'full_amount': '1000000',
    },
    {
        'description': 'Deadpool inside',
        'full_amount': '1000000',
    },
    {
        'name': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
    },
    {
        'name': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
        'full_amount': 'Donat'
    },
    {
        'name': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
        'full_amount': '',
    },
    {},
])
def test_create_charity_project_validation_error(json, superuser_client):
    response = superuser_client.post('/charity_project/', json=json)
    assert response.status_code == 422, (
        'При некорректном создании проекта должен возвращаться статус-код 422. '
        f'При теле запроса: {json}'
    )
    data = response.json()
    assert 'detail' in data.keys(), (
        'При некорректном создании проекта в ответе должен быть ключ `detail`'
    )


def test_delete_charity_project(superuser_client, charity_project):
    response = superuser_client.delete(f'/charity_project/{charity_project.id}')
    assert response.status_code == 200, (
        'При удалении проекта должен возвращаться статус-код 200'
    )
    data = response.json()
    keys = sorted([
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
        'close_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При удалении проекта в ответе должны быть ключи `{keys}`'
    )
    assert data == {
        'name': 'chimichangas4life',
        'description': 'Huge fan of chimichangas. Wanna buy a lot',
        'full_amount': 1000000,
        'id': 1,
        'invested_amount': 0,
        'fully_invested': False,
        'create_date': '2019-08-24T14:15:22',
        'close_date': '2019-08-24T14:15:22',
    }, 'При удалении проекта тело ответа API отличается от ожидаемого.'


def test_delete_charity_project_invalid_id(superuser_client):
    response = superuser_client.delete('/charity_project/999a4')
    assert response.status_code == 422, (
        'При некорректном удалении проекта должен возвращаться статус-код 422'
    )
    data = response.json()
    assert 'detail' in data.keys(), (
        'При некорректном удалении проекта в ответе должен быть ключ `detail`'
    )


@pytest.mark.parametrize('json, expected_data', [
    ({'full_amount': 10}, {
        'name': 'chimichangas4life',
        'description': 'Huge fan of chimichangas. Wanna buy a lot',
        'full_amount': 10,
        'id': 1,
        'invested_amount': 0,
        'fully_invested': False,
        'create_date': '2019-08-24T14:15:22',
        'close_date': '2019-08-24T14:15:22',
    }),
    ({'name': 'chimi'}, {
        'name': 'chimi',
        'description': 'Huge fan of chimichangas. Wanna buy a lot',
        'full_amount': 1000000,
        'id': 1,
        'invested_amount': 0,
        'fully_invested': False,
        'create_date': '2019-08-24T14:15:22',
        'close_date': '2019-08-24T14:15:22',
    }),
    ({'description': 'Give me the money!'}, {
        'name': 'chimichangas4life',
        'description': 'Give me the money!',
        'full_amount': 1000000,
        'id': 1,
        'invested_amount': 0,
        'fully_invested': False,
        'create_date': '2019-08-24T14:15:22',
        'close_date': '2019-08-24T14:15:22',
    }),
])
def test_update_charity_project(superuser_client, charity_project, json, expected_data):
    response = superuser_client.patch('/charity_project/1', json=json)
    assert response.status_code == 200, (
        'При обновлении проекта должен возвращаться статус-код 200'
    )
    data = response.json()
    keys = sorted([
        'name',
        'description',
        'full_amount',
        'id',
        'invested_amount',
        'fully_invested',
        'create_date',
        'close_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При обновлении проекта в ответе должны быть ключи `{keys}`'
    )
    assert data == expected_data, (
        'При обновлении проекта тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'desctiption': ''},
    {'name': ''},
    {'full_amount': ''},
])
def test_update_charity_project_invalid(superuser_client, charity_project, json):
    response = superuser_client.patch('/charity_project/1', json=json)
    assert response.status_code == 422, (
        'При некорректном обновлении проекта должен возвращаться статус-код 422.'
        f'При теле запроса: {json}'
    )


def test_create_charity_project_usual_user(user_client):
    response = user_client.post('/charity_project/', json={
        'name': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
        'full_amount': 1000000,
    })
    assert response.status_code == 401, (
        'При создании проекта не суперпользователем должен возвращаться статус-код 401'
    )
    data = response.json()
    assert 'detail' in data, (
        'При создании проекта не суперпользователем в ответе должен быть ключ `detail`'
    )
    assert data == {
        'detail': 'Unauthorized',
    }, 'При создании проекта не суперпользователем тело ответа API отличается от ожидаемого.'


def test_patch_charity_project_usual_user(user_client):
    response = user_client.patch('/charity_project/1', json={'full_amount': 10})
    assert response.status_code == 401, (
        'При обновлении проекта не суперпользователем должен возвращаться статус-код 401'
    )
    data = response.json()
    assert 'detail' in data, (
        'При обновлении проекта не суперпользователем в ответе должен быть ключ `detail`'
    )
    assert data == {
        'detail': 'Unauthorized',
    }, 'При обновлении проекта не суперпользователем тело ответа API отличается от ожидаемого.'


def test_patch_charity_project_fully_invested(superuser_client, small_fully_charity_project):
    response = superuser_client.patch('/charity_project/1', json={'full_amount': 10})
    assert response.status_code == 400, (
        'При обновлении проекта который был полностью проинвестирован '
        'должен возвращаться статус-код 400'
    )
    data = response.json()
    assert 'detail' in data, (
        'При обновлении проекта который был полностью проинвестирован '
        'в ответе должен быть ключ `detail`'
    )
    assert data == {
        'detail': 'Закрытый проект нельзя редактировать!',
    }, (
        'При обновлении проекта который был полностью '
        'проинвестирован тело ответа API отличается от ожидаемого.'
    )


def test_create_charity_project_same_name(superuser_client, charity_project):
    response = superuser_client.post('/charity_project/', json={
        'name': 'chimichangas4life',
        'description': 'Huge fan of chimichangas. Wanna buy a lot',
        'full_amount': 1000000,
    })
    assert response.status_code == 400, (
        'При создании проекта который уже был ранее создан '
        'должен возвращаться статус-код 400'
    )
    data = response.json()
    assert 'detail' in data, (
        'При создании проекта который уже был ранее создан '
        'в ответе должен быть ключ `detail`'
    )
    assert data == {
        'detail': 'Проект с таким именем уже существует!',
    }, (
        'При создании проекта который уже был ранее создан '
        'тело ответа API отличается от ожидаемого.'
    )
