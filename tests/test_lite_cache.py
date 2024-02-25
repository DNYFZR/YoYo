# LiteCache Testing
import pytest

@pytest.mark.parameterize("case", [[0, 1], [1, 0], ])
def test_placeholder(case:list):

  if not any(case):
    raise AssertionError("Test failed...")