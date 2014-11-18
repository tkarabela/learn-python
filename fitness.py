#!/usr/bin/env python3

"""
Fitness

Description:
Suppose there's a fish which can do two things: put up weight and lay eggs.
At the start, it has weight of one pound.
Every year, it must allocate a fixed number of "units" into either breeding or consumption.
During the year, it lays eggs. Number of eggs is weight * (units allocated to breeding in that year).
At the end of the year, it has 1/6 chance to die.
Otherwise, it survives and increases its weight by units allocated to consumption in that year.
After a set number of years, the experiment ends.

Given the maximum number of years and "units" for allocation every year,
what is the optimal allocation strategy with respect to the expected number of eggs laid within a lifetime?

Features:
modeling probability
itertools

"""


from itertools import product


def generate_strategies(yrs=6, units=5):
    return product([(i, units-i) for i in range(units+1)], repeat=yrs)

def rank(strategy):
    total_gain = 0
    weighted_gain = 0
    psum = 0
    mass = 1

    for year, (growth, production) in enumerate(strategy, 1):
        p = (5/6)**(year-1) * 1/6 if year != yrs else 1-psum
        psum += p

        total_gain += production * mass
        mass += growth

        weighted_gain += p * total_gain

    return weighted_gain


def main():
    yrs = 6

    best_rank = 0
    best = set()
    for strategy in generate_strategies(yrs=yrs):
        x = rank(strategy)
        if x >= best_rank:
            if x > best_rank:
                best.clear()
                best_rank = x
            best.add(strategy)

    print(best)
    print(best_rank)

if __name__ == "__main__":
    main()
