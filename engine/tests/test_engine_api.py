from engine.app import engine_api
import pytest


@pytest.fixture
def client():
    app = engine_api.create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
