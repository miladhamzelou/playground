def fahrenheit(t):
    return float(9) / 5 * t + 32


def celsius(t):
    return (t - 32) * float(5) / 9


temperatures = (36.5, 37, 37.5, 38, 39)
F = map(fahrenheit, temperatures)
C = map(celsius, F)
temperatures_in_fahrenheit = list(map(fahrenheit, temperatures))
temperatures_in_celsius = list(map(celsius, temperatures_in_fahrenheit))
print(temperatures_in_fahrenheit)
print(temperatures_in_celsius)

a = [1, 2, 3, 4]
b = [17, 12, 11, 10]
c = [-1, -4, 5, 9]
list(map(lambda x, y: x + y, a, b))
list(map(lambda x, y, z: x + y + z, a, b, c))
list(map(lambda x, y, z: 2.5 * x + 2 * y - z, a, b, c))

a = [1, 2, 3]
b = [17, 12, 11, 10]
c = [-1, -4, 5, 9]
list(map(lambda x, y, z: 2.5 * x + 2 * y - z, a, b, c))

from math import sin, cos, tan, pi


def map_functions(x, functions):
    """ map an iterable of functions on the the object x """
    res = []
    for func in functions:
        res.append(func(x))
    return res


family_of_functions = (sin, cos, tan)
print(map_functions(pi, family_of_functions))

fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
odd_numbers = list(filter(lambda x: x % 2, fibonacci))
print(odd_numbers)

even_numbers = list(filter(lambda x: x % 2 == 0, fibonacci))
print(even_numbers)

# or alternatively:
even_numbers = list(filter(lambda x: x % 2 - 1, fibonacci))
print(even_numbers)

import functools
functools.reduce(lambda x, y: x + y, [47, 11, 42, 13], 0)

from functools import reduce
f = lambda a, b: a if (a > b) else b
reduce(f, [47, 11, 42, 102, 13])

reduce(lambda x, y: x + y, range(1, 101))

reduce(lambda x, y: x * y, range(1, 49))

reduce(lambda x, y: x * y, range(44, 50)) / reduce(lambda x, y: x * y,
                                                   range(1, 7))

orders = [["34587", "Learning Python, Mark Lutz", 4, 40.95],
          ["98762", "Programming Python, Mark Lutz", 5, 56.80],
          ["77226", "Head First Python, Paul Barry", 3, 32.95],
          ["88112", "Einführung in Python3, Bernd Klein", 3, 24.99]]
min_order = 100
invoice_totals = list(
    map(lambda x: x if x[1] >= min_order else (x[0], x[1] + 10),
        map(lambda x: (x[0], x[2] * x[3]), orders)))

print(invoice_totals)
