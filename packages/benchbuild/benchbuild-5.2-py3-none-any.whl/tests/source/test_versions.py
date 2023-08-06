import pytest

import attr

import benchbuild.source as bs
from benchbuild.source import versions

@pytest.fixture
def test_src() -> bs.BaseSource:
    test_cls = attr.make_class('TestSource', {}, (bs.BaseSource,))

def test_prefix_versions():
    flt = versions.SingleVersionFilter('a')
