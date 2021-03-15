from equations import correct, incorrect, indeterminate
from qed import parse_equation
import pytest


@pytest.mark.parametrize("equation", correct)
def test_correct(equation):
    assert parse_equation(equation) is True


@pytest.mark.parametrize("equation", incorrect)
def test_incorrect(equation):
    assert parse_equation(equation) is False


@pytest.mark.parametrize("equation", indeterminate)
def test_indeterminate(equation):
    assert parse_equation(equation) is None
