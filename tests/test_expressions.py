from expressions import basic, invalid
from qed import parse_latex, LaTeXParsingError
import pytest


@pytest.mark.parametrize("latex_string,sympy_expr", basic)
def test_basic(latex_string, sympy_expr):
    assert parse_latex(latex_string) == sympy_expr


@pytest.mark.parametrize("latex_string,sympy_expr", invalid)
def test_invalid(latex_string, sympy_expr):
    with pytest.raises(LaTeXParsingError):
        parse_latex(latex_string)
