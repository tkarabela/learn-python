#!/usr/bin/env python3

import functools
import timeit


def fact_rec(n):
    if n == 0:
        return 1
    else:
        return n * fact_rec(n-1)

@functools.lru_cache()
def fact_rec_memoized(n):
    if n == 0:
        return 1
    else:
        return n * fact_rec_memoized(n-1)

def fact_iter(n):
    res = 1
    for i in range(2, n+1):
        res *= i
    return res


def binom_rec(n, k):
    if k == 0 or k == n:
        return 1
    else:
        return binom_rec(n-1, k-1) + binom_rec(n-1, k)

@functools.lru_cache()
def binom_rec_memoized(n, k):
    if k == 0 or k == n:
        return 1
    else:
        return binom_rec_memoized(n-1, k-1) + binom_rec_memoized(n-1, k)

def binom_fact(n, k, fact=fact_iter):
    return fact(n) // (fact(k) * fact(n-k))


def pascal(nmax, binom=binom_fact):
    triangle = []

    for n in range(nmax+1):
        line = []
        for k in range(n+1):
            line.append(binom(n, k))
        triangle.append(line)

    return triangle

def print_triangle(triangle, width=60):
    for line in triangle:
        print(("{0:^%d}" % width).format(" ".join(map(str, line))))


def main():
    N = 10

    for k in range(N+1):
        assert binom_rec(N, k) == binom_rec_memoized(N, k)
        assert binom_rec(N, k) == binom_fact(N, k)

    print_triangle(pascal(N))


    print("\nTo compute Pascal triangle for N=15:")

    x = timeit.timeit("pascal(15, binom_rec)", "from __main__ import pascal, binom_rec", number=1)
    print(x, "sec (recursive binomial function)")

    x = timeit.timeit("pascal(15, binom_rec_memoized)", "from __main__ import pascal, binom_rec_memoized", number=1)
    print(x, "sec (recursive binomial function w/ memoization)")

    x = timeit.timeit("pascal(15, binom_fact)", "from __main__ import pascal, binom_fact", number=1)
    print(x, "sec (factorial-based binomial function)")


    print("\nTo compute factorial of N=300, 1000 repeats:")

    # blows the stack for N=1000 (recursion depth limit)
    x = timeit.timeit("fact_rec(300)", "from __main__ import fact_rec", number=1000)
    print(x, "sec (recursive factorial function)")

    # blows the stack for N=400 (extra wrapper calls)
    x = timeit.timeit("fact_rec_memoized(300)", "from __main__ import fact_rec_memoized", number=1000)
    print(x, "sec (recursive factorial function w/ memoization, cache isn't flushed between repeats)")

    x = timeit.timeit("fact_iter(300)", "from __main__ import fact_iter", number=1000)
    print(x, "sec (iterative factorial function)")

if __name__ == "__main__":
    main()
