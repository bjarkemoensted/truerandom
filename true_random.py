# -*- coding: utf-8 -*-

import json
import math
import numpy as np
from pprint import pprint
from urllib.request import urlopen
from urllib.error import URLError
import sys
from time import sleep

def convert_bytes_to_int(byt):
    return int(byt, 2)

def retry(n = 3, verbose = True):
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
                    sleep(5)
            return result
        return wrapper
    return decorator


#@retry
def get_quantum_bits(n = 32):
    '''Returns random 32-bit integer from ANU Quantum Random Numbers Server'''
    url = 'https://qrng.anu.edu.au/ran_bin.php'
    bitstring = ""
    while len(bitstring) < n:
        response = urlopen(url)
        html = response.read()
        bitstring += html.decode("utf-8")


    return bitstring[:n]


def qrandint(low, high = None):
    '''Returns a random integer selected randomly between low and high.
    if high == None, interval is 0 to low.'''

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
    result = low + x
    return result

def qchoice(a, n_elements = 1, replace = True):
    indices = list(range(len(a)))
    result = []
    for _ in range(n_elements):
        indptr = qrandint(len(indices))
        if replace:
            ind = indices[indptr]
        else:
            ind = indices.pop(indptr)
        result.append(a[ind])
    #
    return result

def qbool():
    x = get_quantum_bits(n=1)
    return x == "1"


print(qbool())


