import random
from collections import Counter


def sample_mean(xs):
    return sum(xs) / len(xs)

def sample_variance(xs, mean=None):
    if mean is None:
        mean = sample_mean(xs)

    return sum((x - mean)**2 for x in xs) / (len(xs) - 1)

def sample_stdev(xs, mean=None):
    return sample_variance(xs, mean)**0.5

def median(xs):
    n = len(xs)
    ys = xs[:]
    ys.sort()
    return ys[n//2]

def mode(xs):
    ctr = Counter(xs)
    return ctr.most_common(1)[0]


def main():
    mu, sigma = 170, 20

    for n in [3, 15, 300]:
        data = [random.gauss(mu, sigma) for _ in range(n)]

        print("Generated", n, "samples from normal distribution (mu, sigma) =", (mu, sigma))

        xbar = sample_mean(data)
        xdev = sample_stdev(data, xbar)
        xmed = median(data)

        print("Sample mean =", xbar)
        print("Sample standard deviation =", xdev)
        print("Median =", xmed)
        print()

if __name__ == "__main__":
    main()
