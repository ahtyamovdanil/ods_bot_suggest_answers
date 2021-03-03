import pytest
from engine.app.semantic_engine import SemanticEngine
import torch


@pytest.mark.dependency
def test_load_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.load_embeddings(datadir.joinpath("embeddings.pkl"))
    assert engine.embeddings is not None
    # assert engine.embeddings.bool().all()


@pytest.mark.dependency
def test_calc_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.calc_embeddings(get_df.text.tolist())
    assert engine.embeddings is not None
    # assert engine.embeddings.bool().all()


@pytest.mark.dependency(depends=["test_load_embeddings", "test_calc_embeddings"])
def test_save_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.calc_embeddings(get_df.text.tolist())
    curr_emb = engine.embeddings
    emb_path = datadir.joinpath("test_embeddings.pkl")
    engine.save_embeddings(emb_path)
    engine.embeddings = None
    engine.load_embeddings(emb_path)
    assert torch.all(torch.eq(curr_emb, engine.embeddings))


@pytest.mark.dependency(depends=["test_load_embeddings"])
def test_get_top_k(datadir, get_df):
    engine = SemanticEngine(get_df)
    query = "посоветуйте курсов по питону"
    k = 5

    with pytest.raises(ValueError):
        engine.get_top_k(query, k)

    engine.load_embeddings(datadir.joinpath("embeddings.pkl"))
    result = engine.get_top_k(query, k)
    assert len(result) == k
