#!/usr/bin/env python3

from fractions import Fraction
import decimal


def arctan(x, terms=3):
    """
    Approximate arctan(x) using Taylor series

    """
    return sum((-1)**k * x**(2*k+1) / (2*k+1) for k in reversed(range(terms)))

def compute_pi(terms=3, make_number=float):
    """
    Approximate pi using Machin's formula

    """
    a = 1 / make_number(5)
    b = 1 / make_number(239)
    c = arctan(a, terms=terms)
    d = arctan(b, terms=terms)
    return 4 * (4*c - d)


DIGITS_OF_PI = """
3.14159265358979323846264338327950288419716939937510
58209749445923078164062862089986280348253421170679
82148086513282306647093844609550582231725359408128
""".strip()

def show_error(x, digits=40):
    decimal.getcontext().prec = digits + 20
    if isinstance(x, Fraction):
        y = decimal.Decimal(x.numerator) / decimal.Decimal(x.denominator)
    else:
        y = decimal.Decimal(x)
    x_as_str = str(y)

    output = []
    good = True
    for d, ref in zip(x_as_str, DIGITS_OF_PI):
        good = good and d == ref
        output.append(d if good else "-")

    return "".join(output)


def main():
    print("Approximate pi using IEEE 754 double precision floating point:")
    for i in [3, 5, 7, 10, 50]:
        print(i, "terms:", show_error(compute_pi(i, float)))

    print("\nApproximate pi using rational numbers:")
    for i in [3, 5, 7, 10, 15, 30, 50]:
        print(i, "terms:", show_error(compute_pi(i, Fraction)))

if __name__ == "__main__":
    main()
