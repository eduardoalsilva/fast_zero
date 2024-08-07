from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (afirma)
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_create_user(client):
    response = client.post('/users/',  # UserSchema
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com'
        }
    )

    # Validar UserPublic
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1
        }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': 1,
        }
    )

    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}


def test_update_user_not_found(client):
    response = client.put('/users/-1')

    assert response.status_code == (
        HTTPStatus.NOT_FOUND and HTTPStatus.UNPROCESSABLE_ENTITY
    )
    # assert response.raise_for_status == 'User not found'


def test_delete_user_not_found(client):
    response = client.delete('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    # assert response.raise_for_status() == HTTPException()'User not found'


def test_read_root_deve_retornar_html_ola_mundo(client):
    response = client.get('/message')

    assert response.status_code == HTTPStatus.OK
    assert response.text == """
                            <html>
                                <head>
                                    <title>Meu olá mundo!</title>
                                </head>
                                <body>
                                    <h1>Olá Mundo!</h1>
                                </body>
                            </html>"""
