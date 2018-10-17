from coffee_shop.auth.schemas import UserSchema


def test_user_schema(session):
    request_json = {'name': 'john doe', 'email': 'john@doe.com', 'password': '123mudar', 'role': 'admin'}
    __import__('ipdb').set_trace()
    user = UserSchema(session=session).load(request_json).data

    assert user.name == request_json['name']
    assert user.email == request_json['email']
    assert user.active == request_json['active']
    assert user.password == request_json['password']


def test_user_create_schema():
    pass
