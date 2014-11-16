#!/usr/bin/env python3

"""
Primes

Features:
process-based parallelism
comprehensions
map

Requirements:
Python 3.3+

"""

from multiprocessing.pool import Pool
import os
from timeit import default_timer as timer


def is_prime(n):
    """
    Find whether n is a prime number

    The function uses trial division, ie. n is prime if and only if
    it's not divisible by any k such that 2 <= k < n.

    Note that this algorithm is rather slow and inefficient.

    """
    return all(n % k != 0 for k in range(2, n))


def find_primes_sequentially(nmax):
    # return [n for n in range(2, nmax) if is_prime(n)]

    numbers = range(2, nmax)
    primes = []

    for n, n_is_prime in zip(numbers, map(is_prime, numbers)):
        if n_is_prime:
            primes.append(n)

    return primes

def find_primes_with_process_pool(nmax, p):
    numbers = range(2, nmax)
    primes = []
    chunksize = 500  # each worker gets ~500 numbers at once (chunksize=1 is very slow)

    with Pool(processes=p) as pool:
        for n, n_is_prime in zip(numbers, pool.imap(is_prime, numbers, chunksize)):
            if n_is_prime:
                primes.append(n)

    return primes


def main():
    N = 10**4
    p = 3
    print("Finding primes up to", N)

    t0 = timer(); primes1 = find_primes_sequentially(N); t1 = timer(); ts = t1-t0
    print("Simple code with no parallelism took", ts, "s")

    t0 = timer(); primes2 = find_primes_with_process_pool(N, p); t1 = timer(); tp = t1-t0
    print("Execution with", p, "parallel processes took", tp, "s")
    print("Number of available CPUs:", os.cpu_count())
    print("Parallel speed-up:", ts/tp)

    assert primes1 == primes2

if __name__ == "__main__":
    main()
