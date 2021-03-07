from expressions import pairs, invalid
from qed import parse_latex, LaTeXParsingError
import pytest


@pytest.mark.parametrize("pair", pairs)
def test_parseable(pair):
    assert parse_latex(pair[0]) == pair[1]


@pytest.mark.parametrize("expr", invalid)
def test_not_parseable(expr):
    with pytest.raises(LaTeXParsingError):
        parse_latex(expr)
