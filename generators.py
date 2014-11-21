#!/usr/bin/env python3

"""
Generators

"generators are functions, but with the twist that they're resumable" (PEP 255)

References:
https://docs.python.org/3.4/howto/functional.html#iterators
https://www.python.org/dev/peps/pep-0255

"""

from collections.abc import Iterator


class MyRange(Iterator):
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        # return the iterator, ie. object with __next__ method
        # in simple cases, this can be the iterable object itself
        # if we want multiple independent iterators for one iterable,
        # we can return different object each time an iterator is requested
        return self

    def __next__(self):
        # return a value or raise StopIteration if there are no more values
        # note that this works like a state machine
        if self.i < self.n:
            j = self.i
            self.i += 1
            return j
        else:
            raise StopIteration


def my_range(n):
    # generator version of the same
    # calling this function returns an iterator
    i = 0
    while i < n:
        yield i
        i += 1

def my_count():
    # iterators allow for infinite sequences
    # note that there is no way to know if a "lazy" sequence is finite,
    # so collecting all elements in eg. list is generally not safe
    i = 0
    while True:
        yield i
        i += 1

def my_primes():
    # sequence of all prime numbers
    n = 2
    while True:
        if all(n % k != 0 for k in range(2, n)):
            yield n
        n += 1

def main():
    for i in range(3):
        print(i)

    for i in MyRange(3):
        print(i)

    for i in my_range(3):
        print(i)

    for i in my_count():
        if i < 3:
            print(i)
        else:
            break # breaks the infinite loop

    x = list(my_range(3))
    print(x)

    # create a list of all integers, don't try this at home
    # y = list(my_count())

    for i, p in enumerate(my_primes(), 1):
        if p < 20:
            print("Prime #%d is %d" % (i, p))
        else:
            break # don't print primes above 20


if __name__ == "__main__":
    main()
