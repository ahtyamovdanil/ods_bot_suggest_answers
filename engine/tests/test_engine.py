import pytest
import pandas as pd
from engine.app.semantic_engine import SemanticEngine
from testfixtures import TempDirectory
from pytest import fixture
from distutils import dir_util
import os
import torch


@fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


@fixture
def get_df(datadir):
    path = datadir.join("data.tsv")
    return pd.read_csv(path, sep="\t")


@pytest.mark.dependency
def test_load_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.load_embeddings(datadir.join("embeddings.pkl"))
    assert engine.embeddings is not None
    assert engine.embeddings.bool().all()


@pytest.mark.dependency
def test_calc_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.calc_embeddings(get_df.text.tolist())
    assert engine.embeddings is not None
    assert engine.embeddings.bool().all()


@pytest.mark.dependency(depends=["test_load_embeddings", "test_calc_embeddings"])
def test_save_embeddings(datadir, get_df):
    engine = SemanticEngine(get_df)
    engine.calc_embeddings(get_df.text.tolist())
    curr_emb = engine.embeddings
    emb_path = datadir.join("test_embeddings.pkl")
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

    engine.load_embeddings(datadir.join("embeddings.pkl"))
    result = engine.get_top_k(query, k)
    assert len(result) == k

