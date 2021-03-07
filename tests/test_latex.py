from expressions import *
from qed import parse_latex
import pytest


@pytest.mark.parametrize("pair", GOOD_PAIRS)
def test_parseable(pair):
    assert parse_latex(pair[0]) == pair[1]


@pytest.mark.xfail
def test_failing_parseable():
    for latex_str, sympy_expr in FAILING_PAIRS:
        with raises(Exception):
            assert parse_latex(latex_str) == sympy_expr


# These bad LaTeX strings should raise a LaTeXParsingError when parsed
BAD_STRINGS = [
    r"(",
    r")",
    r"\frac{d}{dx}",
    r"(\frac{d}{dx})",
    r"\sqrt{}",
    r"\sqrt",
    r"\overline{}",
    r"\overline",
    r"{",
    r"}",
    r"\mathit{x + y}",
    r"\mathit{21}",
    r"\frac{2}{}",
    r"\frac{}{2}",
    r"\int",
    r"!",
    r"!0",
    r"_",
    r"^",
    r"|",
    r"||x|",
    r"()",
    r"((((((((((((((((()))))))))))))))))",
    r"-",
    r"\frac{d}{dx} + \frac{d}{dt}",
    r"f(x,,y)",
    r"f(x,y,",
    r"\sin^x",
    r"\cos^2",
    r"@",
    r"#",
    r"$",
    r"%",
    r"&",
    r"*",
    r"" "\\",
    r"~",
    r"\frac{(2 + x}{1 - x)}",
]


@pytest.mark.xfail
def test_not_parseable():
    from qed import parse_latex, LaTeXParsingError

    for latex_str in BAD_STRINGS:
        with raises(LaTeXParsingError):
            parse_latex(latex_str)


# At time of migration from latex2sympy, should fail but doesn't
FAILING_BAD_STRINGS = [
    r"\cos 1 \cos",
    r"f(,",
    r"f()",
    r"a \div \div b",
    r"a \cdot \cdot b",
    r"a // b",
    r"a +",
    r"1.1.1",
    r"1 +",
    r"a / b /",
]


@pytest.mark.xfail
def test_failing_not_parseable():
    from qed import parse_latex, LaTeXParsingError

    for latex_str in FAILING_BAD_STRINGS:
        with raises(LaTeXParsingError):
            parse_latex(latex_str)
