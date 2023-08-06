import os
import json
import pytest
from structures.trees import FolderTree

FILES = None
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEST_DIR, 'data')
with open(os.path.join(DATA_DIR, 'fake_files.json'), 'r') as f:
    FILES = json.load(f)

@pytest.fixture
def root():
    return FolderTree(FILES[0])


@pytest.fixture
def tree():
    root = FolderTree(FILES[0])
    for f in FILES:
        if not f['is_root']:
            root.add_node(f)
    return root


@pytest.mark.xfail
def test_duplicate_roots(root):
    try:
        root.add_node(FILES[0])
    except IndexError:
        assert False


def test_search_id_not_found(root):
    r = root.search_id('c4b90385-5c43-4589-8183-0ef62eb819a0')
    assert r is None


def test_search_id_found(tree):
    r = tree.search_id('6')
    assert r is not None


def test_print_node(tree):
    tree.print_node()
