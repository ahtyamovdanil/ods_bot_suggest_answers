import pytest
import torch
import pandas as pd
from engine.app.semantic_engine import SemanticEngine


@pytest.fixture(scope="module", autouse=True)
def get_df(datadir):
    """load data.tsv file and return pandas dataframe"""
    return pd.read_csv(datadir.joinpath("data.tsv"), sep="\t")


@pytest.fixture(scope="session")
def get_sentences(faker, faker_seed, faker_locale):
    return faker.text()


@pytest.mark.dependency
def test_load_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.load_embeddings(datadir.joinpath("embeddings.pkl"))
    assert isinstance(engine.embeddings, torch.Tensor)


@pytest.mark.dependency
def test_calc_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)

    with pytest.raises(ValueError):
        engine.calc_embeddings([])

    engine.calc_embeddings(get_df.text.tolist())
    assert isinstance(engine.embeddings, torch.Tensor)


@pytest.mark.dependency(depends=["test_load_embeddings", "test_calc_embeddings"])
def test_save_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.calc_embeddings(get_df.text.tolist())
    curr_emb = engine.embeddings
    emb_path = datadir.joinpath("test_embeddings.pkl")
    engine.save_embeddings(emb_path)
    engine.embeddings = None
    engine.load_embeddings(emb_path)
    # check that previous calculated embeddings are the same as loaded ones
    assert torch.all(torch.eq(curr_emb, engine.embeddings))


@pytest.mark.parametrize('k', (0, 7, 15))
@pytest.mark.dependency(depends=["test_load_embeddings"])
def test_get_top_k(datadir, get_df, k):
    engine = SemanticEngine(get_df)
    query = "посоветуйте курсов по python"

    with pytest.raises(ValueError):
        engine.get_top_k(query, k)

    engine.load_embeddings(datadir.joinpath("embeddings.pkl"))
    result = engine.get_top_k(query, k)
    assert len(result) == min(k, len(get_df))
