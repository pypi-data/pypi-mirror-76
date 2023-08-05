from math import sqrt

from typing import List, Iterator


def is_prime(n: int) -> bool:

    """ Checks if given number n is prime. """

    if n & 1 == 0 and n != 2:
        return False
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    else:
        return True


def primes_till(n: int) -> List[int]:

    """ Returns a list of all primes numbers up until n. """

    primes = [2]
    for i in range(3, n + 2, 2):
        if is_prime(i):
            primes.append(i)
    return primes


def n_primes(n: int) -> List[int]:

    """ Returns a list of first n natural primes numbers. """

    to_test = 3
    primes = [2]
    while len(primes) != n:
        if is_prime(to_test):
            primes.append(to_test)
        to_test += 2
    return primes


def n_prime(n: int) -> int:

    """ Returns the nth prime number. """

    if n == 1:
        return 2

    to_test = 3
    prime_count = 1

    while prime_count <= n:
        if is_prime(to_test):
            prime_count += 1
            if prime_count == n:
                return to_test
        to_test += 2


def prime_generator() -> Iterator[int]:

    """ Returns an iterable of ints with each next element being the next prime number. """

    yield 2
    begin = 3
    while True:
        if is_prime(begin):
            yield begin
        begin += 2
