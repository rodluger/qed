from expressions import pairs, invalid
from qed import parse_latex, LaTeXParsingError
import pytest


@pytest.mark.parametrize("latex_string,sympy_expr", pairs)
def test_parseable(latex_string, sympy_expr):
    assert parse_latex(latex_string) == sympy_expr


@pytest.mark.parametrize("latex_string", invalid)
def test_not_parseable(latex_string):
    with pytest.raises(LaTeXParsingError):
        parse_latex(latex_string)
