# PyPrimer

A simple collection of prime number related functions.

## Install

```shell script
$ pip install pyprimer
```

For bleeding edge

```shell script
$ pip install git+https://github.com/mentix02/pyprimer
```

## Docs

+ `is_prime(int) -> bool`
    + Checks if given number n is prime.

```pydocstring
>>> from pyprimer import is_prime
>>> is_prime(3)
True
```

+ `primes_till(int) -> List[int]`
    + Returns a list of all primes numbers up until n.

```pydocstring
>>> from pyprimer import primes_till
>>> primes_till(6)
[2, 3, 5, 7]
```

+ `n_primes(int) -> List[int]`
    + Returns a list of first n natural primes numbers.

```pydocstring
>>> from pyprimer import n_primes
>>> n_primes(6)
[2, 3, 5, 7, 11, 13]
```

+ `n_prime(int) -> int`
    + Returns the nth prime number.

```pydocstring
>>> from pyprimer import n_prime
>>> n_prime(13)
41
```

+ `prime_generator() -> Iterator[int]`
    + Returns an iterable of ints with each next element being the next prime number.

```pydocstring
>>> from pyprimer import prime_generator
>>> total = 0
>>> g = prime_generator()
>>> for n in g:
...   if n == 13:
...     break
...   total += n
>>> print(total)
28
```
