import pytest

from music.app_factory import create_app


@pytest.fixture()
def get_test_app():
    return create_app().test_client()
