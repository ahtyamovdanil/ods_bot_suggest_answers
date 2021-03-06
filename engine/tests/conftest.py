import tempfile
import shutil
import os
from distutils import dir_util
from pytest import fixture
from pathlib import Path


@fixture(scope="module", autouse=True)
def datadir(request):
    """
    Fixture responsible for searching a folder with name `data`
    and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    tmpdir = Path(tempfile.mkdtemp())
    test_dir = Path(os.path.join(request.fspath.dirname, 'data'))

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    yield tmpdir
    shutil.rmtree(tmpdir)
