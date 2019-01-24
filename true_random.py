# -*- coding: utf-8 -*-

import json
import math
import numpy as np
import requests
from pprint import pprint
from urllib.request import urlopen
from urllib.error import URLError
import sys
from time import sleep

# URL for the ANU quantum random number generator API
API = "https://qrng.anu.edu.au/API/jsonI.php"

def retry(n = 3, verbose = True):
    '''Decorator to automatically retry failed API calls.'''

    def decorator(func):
        def wrapper(*args, **kwargs):
            count = 0
            result = None
            while result == None and count < n:
                try:
                    result = func(*args, **kwargs)
                except URLError:
                    count += 1
                    if verbose:
                        print("URL error. at attempt %d of %d." % (count, n))
                    sleep(3)
            return result
        return wrapper
    return decorator


def get_rand(n_bits=8):
    '''Returns random binary string of length 8 or 16.'''

    if n_bits not in (8, 16):
        raise ValueError
    params = {"type": "uint%d"%n_bits, "length": 1}
    response = requests.get(API, params=params)
    n = response.json()["data"][0]
    res = "{0:b}".format(n).zfill(n_bits)

    return res

#@retry(n=1)
def get_quantum_bits(n = 32):
    '''Returns a random binary string of length n.'''

    bitstring = ""
    while len(bitstring) < n:
        n_more = 8 if n - len(bitstring) <= 8 else 16
        fresh = get_rand(n_bits = n_more)
        bitstring += fresh

    return bitstring[:n]


def randint(low, high = None, size=None):
    '''Returns a random integer selected randomly between low and high.
    if high == None, interval is 0 to low.'''

    n_get = 1 if size is None else size
    result = []

    while len(result) < n_get:
        if high == None:
            high = low
            low = 0

        # Number of possible intergers we draw from
        span = high - low
        if span == 1:
            return low

        # Number of bits we need
        n_bits = int(math.ceil(math.log(span, 2)))

        # Keep redrawing if we draw outside the desired interval
        x = float('inf')
        while x >= span:
            random_bits = get_quantum_bits(n_bits)
            x = int(random_bits, 2)

        # Done. Add to the lower limit and return
        result.append(low + x)

    if size is None:
        return result[0]
    else:
        return result


def choice(a, size=None, replace=True):
    '''Chooses random elements from input list.'''

    indices = list(range(len(a)))
    result = []
    for _ in range(size):
        indptr = randint(len(indices))
        if replace:
            ind = indices[indptr]
        else:
            ind = indices.pop(indptr)
        result.append(a[ind])
    #
    if size is None:
        return result[0]
    else:
        return result


def qbool():
    '''Returns a random boolean.'''
    x = get_quantum_bits(n=1)
    return x == "1"


if __name__ == '__main__':
    x = get_quantum_bits(23)
    print(x, qbool())


