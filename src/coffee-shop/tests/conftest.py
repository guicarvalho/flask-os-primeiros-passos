import pytest

from coffee_shop import create_app


@pytest.fixture(scope='session')
def app():
    return create_app('Testing')

