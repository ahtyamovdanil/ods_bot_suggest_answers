from engine.app import engine_api
import pytest


@pytest.fixture
def client(datadir):
    app = engine_api.create_app(
        data_path=datadir.joinpath("data.tsv"),
        embeddings_path=datadir.joinpath("embeddings.pkl")
    )
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def get_messages(client, text, k):
    return client.post('/api/get_messages', json={"text": text, "top_k": k})


def test_get_messages(client):
    text = "посоветуйте курсов по python"
    k = 3
    response = get_messages(client, text, k)
    assert response.status_code == 200
    assert len(response.json) == k
