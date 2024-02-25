# LiteCache Testing
import pytest

@pytest.mark.parametrize("case", [[0, 1], [1, 0], ["something", None], [False, True, False]])
def test_placeholder(case:list):

  if not any(case):
    raise AssertionError("Test failed...")