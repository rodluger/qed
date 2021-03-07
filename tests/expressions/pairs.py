from sympy import (
    Symbol,
    Mul,
    Add,
    Abs,
    sin,
    asin,
    cos,
    Pow,
    csc,
    sec,
    Limit,
    oo,
    Derivative,
    Integral,
    factorial,
    sqrt,
    root,
    conjugate,
    StrictLessThan,
    LessThan,
    StrictGreaterThan,
    GreaterThan,
    Sum,
    Product,
    E,
    log,
    tan,
    Function,
    binomial,
    exp,
    floor,
    ceiling,
    Unequality,
)
from sympy.core.relational import Eq, Ne, Lt, Le, Gt, Ge
from sympy.physics.quantum.state import Bra, Ket
from sympy.abc import x, y, z, a, b, c, t, k, n


theta = Symbol("theta")
f = Function("f")


def _Add(a, b):
    return Add(a, b, evaluate=False)


def _Mul(a, b):
    return Mul(a, b, evaluate=False)


def _Pow(a, b):
    return Pow(a, b, evaluate=False)


def _Sqrt(a):
    return sqrt(a, evaluate=False)


def _Conjugate(a):
    return conjugate(a, evaluate=False)


def _Abs(a):
    return Abs(a, evaluate=False)


def _factorial(a):
    return factorial(a, evaluate=False)


def _exp(a):
    return exp(a, evaluate=False)


def _log(a, b):
    return log(a, b, evaluate=False)


def _binomial(n, k):
    return binomial(n, k, evaluate=False)


pairs = [
    (r"0", 0),
    (r"1", 1),
    (r"-3.14", _Mul(-1, 3.14)),
    (r"(-7.13)(1.5)", _Mul(_Mul(-1, 7.13), 1.5)),
    (r"x", x),
    (r"2x", 2 * x),
    (r"x^2", x ** 2),
    (r"x^{3 + 1}", x ** _Add(3, 1)),
    (r"-c", -c),
    (r"a \cdot b", a * b),
    (r"a / b", a / b),
    (r"a \div b", a / b),
    (r"a + b", a + b),
    (r"a + b - a", _Add(a + b, -a)),
    (r"a^2 + b^2 = c^2", Eq(a ** 2 + b ** 2, c ** 2)),
    (r"(x + y) z", _Mul(_Add(x, y), z)),
    (r"\left(x + y\right) z", _Mul(_Add(x, y), z)),
    (r"\left( x + y\right ) z", _Mul(_Add(x, y), z)),
    (r"\left(  x + y\right ) z", _Mul(_Add(x, y), z)),
    (r"\left[x + y\right] z", _Mul(_Add(x, y), z)),
    (r"\left\{x + y\right\} z", _Mul(_Add(x, y), z)),
    (r"1+1", _Add(1, 1)),
    (r"0+1", _Add(0, 1)),
    (r"1*2", _Mul(1, 2)),
    (r"0*1", _Mul(0, 1)),
    (r"x = y", Eq(x, y)),
    (r"x \neq y", Ne(x, y)),
    (r"x < y", Lt(x, y)),
    (r"x > y", Gt(x, y)),
    (r"x \leq y", Le(x, y)),
    (r"x \geq y", Ge(x, y)),
    (r"x \le y", Le(x, y)),
    (r"x \ge y", Ge(x, y)),
    (r"\lfloor x \rfloor", floor(x)),
    (r"\lceil x \rceil", ceiling(x)),
    (r"\langle x |", Bra("x")),
    (r"| x \rangle", Ket("x")),
    (r"\sin \theta", sin(theta)),
    (r"\sin(\theta)", sin(theta)),
    (r"\sin^{-1} a", asin(a)),
    (r"\sin a \cos b", _Mul(sin(a), cos(b))),
    (r"\sin \cos \theta", sin(cos(theta))),
    (r"\sin(\cos \theta)", sin(cos(theta))),
    (r"\frac{a}{b}", a / b),
    (r"\frac{a + b}{c}", _Mul(a + b, _Pow(c, -1))),
    (r"\frac{7}{3}", _Mul(7, _Pow(3, -1))),
    (r"(\csc x)(\sec y)", csc(x) * sec(y)),
    (r"\lim_{x \to 3} a", Limit(a, x, 3)),
    (r"\lim_{x \rightarrow 3} a", Limit(a, x, 3)),
    (r"\lim_{x \Rightarrow 3} a", Limit(a, x, 3)),
    (r"\lim_{x \longrightarrow 3} a", Limit(a, x, 3)),
    (r"\lim_{x \Longrightarrow 3} a", Limit(a, x, 3)),
    (r"\lim_{x \to 3^{+}} a", Limit(a, x, 3, dir="+")),
    (r"\lim_{x \to 3^{-}} a", Limit(a, x, 3, dir="-")),
    (r"\infty", oo),
    (r"\lim_{x \to \infty} \frac{1}{x}", Limit(_Pow(x, -1), x, oo)),
    (r"\frac{d}{dx} x", Derivative(x, x)),
    (r"\frac{d}{dt} x", Derivative(x, t)),
    (r"f(x)", f(x)),
    (r"f(x, y)", f(x, y)),
    (r"f(x, y, z)", f(x, y, z)),
    (r"\frac{d f(x)}{dx}", Derivative(f(x), x)),
    (r"\frac{d\theta(x)}{dx}", Derivative(Function("theta")(x), x)),
    (r"x \neq y", Unequality(x, y)),
    (r"|x|", _Abs(x)),
    (r"||x||", _Abs(Abs(x))),
    (r"|x||y|", _Abs(x) * _Abs(y)),
    (r"||x||y||", _Abs(_Abs(x) * _Abs(y))),
    (r"\pi^{|xy|}", Symbol("pi") ** _Abs(x * y)),
    (r"\int x dx", Integral(x, x)),
    (r"\int x d\theta", Integral(x, theta)),
    (r"\int (x^2 - y)dx", Integral(x ** 2 - y, x)),
    (r"\int x + a dx", Integral(_Add(x, a), x)),
    (r"\int da", Integral(1, a)),
    (r"\int_0^7 dx", Integral(1, (x, 0, 7))),
    (r"\int_a^b x dx", Integral(x, (x, a, b))),
    (r"\int^b_a x dx", Integral(x, (x, a, b))),
    (r"\int_{a}^b x dx", Integral(x, (x, a, b))),
    (r"\int^{b}_a x dx", Integral(x, (x, a, b))),
    (r"\int_{a}^{b} x dx", Integral(x, (x, a, b))),
    (r"\int^{b}_{a} x dx", Integral(x, (x, a, b))),
    (r"\int_{f(a)}^{f(b)} f(z) dz", Integral(f(z), (z, f(a), f(b)))),
    (r"\int (x+a)", Integral(_Add(x, a), x)),
    (r"\int a + b + c dx", Integral(_Add(_Add(a, b), c), x)),
    (r"\int \frac{dz}{z}", Integral(Pow(z, -1), z)),
    (r"\int \frac{3 dz}{z}", Integral(3 * Pow(z, -1), z)),
    (r"\int \frac{1}{x} dx", Integral(Pow(x, -1), x)),
    (
        r"\int \frac{1}{a} + \frac{1}{b} dx",
        Integral(_Add(_Pow(a, -1), Pow(b, -1)), x),
    ),
    (
        r"\int \frac{3 \cdot d\theta}{\theta}",
        Integral(3 * _Pow(theta, -1), theta),
    ),
    (r"\int \frac{1}{x} + 1 dx", Integral(_Add(_Pow(x, -1), 1), x)),
    (r"x_0", Symbol("x_{0}")),
    (r"x_{1}", Symbol("x_{1}")),
    (r"x_a", Symbol("x_{a}")),
    (r"x_{b}", Symbol("x_{b}")),
    (r"h_\theta", Symbol("h_{theta}")),
    (r"h_{\theta}", Symbol("h_{theta}")),
    (
        r"h_{\theta}(x_0, x_1)",
        Function("h_{theta}")(Symbol("x_{0}"), Symbol("x_{1}")),
    ),
    (r"x!", _factorial(x)),
    (r"100!", _factorial(100)),
    (r"\theta!", _factorial(theta)),
    (r"(x + 1)!", _factorial(_Add(x, 1))),
    (r"(x!)!", _factorial(_factorial(x))),
    (r"x!!!", _factorial(_factorial(_factorial(x)))),
    (r"5!7!", _Mul(_factorial(5), _factorial(7))),
    (r"\sqrt{x}", sqrt(x)),
    (r"\sqrt{x + b}", sqrt(_Add(x, b))),
    (r"\sqrt[3]{\sin x}", root(sin(x), 3)),
    (r"\sqrt[y]{\sin x}", root(sin(x), y)),
    (r"\sqrt[\theta]{\sin x}", root(sin(x), theta)),
    (r"\sqrt{\frac{12}{6}}", _Sqrt(_Mul(12, _Pow(6, -1)))),
    (r"\overline{z}", _Conjugate(z)),
    (r"\overline{\overline{z}}", _Conjugate(_Conjugate(z))),
    (r"\overline{x + y}", _Conjugate(_Add(x, y))),
    (r"\overline{x} + \overline{y}", _Conjugate(x) + _Conjugate(y)),
    (r"x < y", StrictLessThan(x, y)),
    (r"x \leq y", LessThan(x, y)),
    (r"x > y", StrictGreaterThan(x, y)),
    (r"x \geq y", GreaterThan(x, y)),
    (r"\mathit{x}", Symbol("x")),
    (r"\mathit{test}", Symbol("test")),
    (r"\mathit{TEST}", Symbol("TEST")),
    (r"\mathit{HELLO world}", Symbol("HELLO world")),
    (r"\sum_{k = 1}^{3} c", Sum(c, (k, 1, 3))),
    (r"\sum_{k = 1}^3 c", Sum(c, (k, 1, 3))),
    (r"\sum^{3}_{k = 1} c", Sum(c, (k, 1, 3))),
    (r"\sum^3_{k = 1} c", Sum(c, (k, 1, 3))),
    (r"\sum_{k = 1}^{10} k^2", Sum(k ** 2, (k, 1, 10))),
    (
        r"\sum_{n = 0}^{\infty} \frac{1}{n!}",
        Sum(_Pow(_factorial(n), -1), (n, 0, oo)),
    ),
    (r"\prod_{a = b}^{c} x", Product(x, (a, b, c))),
    (r"\prod_{a = b}^c x", Product(x, (a, b, c))),
    (r"\prod^{c}_{a = b} x", Product(x, (a, b, c))),
    (r"\prod^c_{a = b} x", Product(x, (a, b, c))),
    (r"\exp x", _exp(x)),
    (r"\exp(x)", _exp(x)),
    (r"\ln x", _log(x, E)),
    (r"\ln xy", _log(x * y, E)),
    (r"\log x", _log(x, 10)),
    (r"\log xy", _log(x * y, 10)),
    (r"\log_{2} x", _log(x, 2)),
    (r"\log_{a} x", _log(x, a)),
    (r"\log_{11} x", _log(x, 11)),
    (r"\log_{a^2} x", _log(x, _Pow(a, 2))),
    (r"[x]", x),
    (r"[a + b]", _Add(a, b)),
    (r"\frac{d}{dx} [ \tan x ]", Derivative(tan(x), x)),
    (r"\binom{n}{k}", _binomial(n, k)),
    (r"\tbinom{n}{k}", _binomial(n, k)),
    (r"\dbinom{n}{k}", _binomial(n, k)),
    (r"\binom{n}{0}", _binomial(n, 0)),
    (r"a \, b", _Mul(a, b)),
    (r"a \thinspace b", _Mul(a, b)),
    (r"a \: b", _Mul(a, b)),
    (r"a \medspace b", _Mul(a, b)),
    (r"a \; b", _Mul(a, b)),
    (r"a \thickspace b", _Mul(a, b)),
    (r"a \quad b", _Mul(a, b)),
    (r"a \qquad b", _Mul(a, b)),
    (r"a \! b", _Mul(a, b)),
    (r"a \negthinspace b", _Mul(a, b)),
    (r"a \negmedspace b", _Mul(a, b)),
    (r"a \negthickspace b", _Mul(a, b)),
    (r"\int x \, dx", Integral(x, x)),
    #
    # -- Issues below --
    #
    (r"\log_2 x", _log(x, 2)),
    (r"\log_a x", _log(x, a)),
]
