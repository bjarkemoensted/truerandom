# -*- coding: utf-8 -*-

import json
import math
import numpy as np
from pprint import pprint
import urllib2
import sys
from time import sleep


def retry(n = 3, verbose = True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            count = 0
            result = None
            while result == None and count < n:
                try:
                    result = func(*args, **kwargs)
                except urllib2.URLError:
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
        response = urllib2.urlopen(url)
        html = response.read()
        bitstring += html


    return bitstring[:n]


class qgen(object):
    '''hest'''
    def __init__(self, method = 'quantum', buffer_size = 100):
        if method == 'quantum':
            self.get_bits = get_quantum_bits
        elif method == 'cosmic':
            self.get_bits == get_cosmic_bits
        elif method == 'all':
            #TODO Implementer at prøve dem efter hinandne
            pass
        else:
            raise ValueError("Unknown method")

        self.buffer_size = buffer_size
        self.buffer = ""

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
    indices = range(len(a))
    result = []
    for _ in xrange(n_elements):
        indptr = qrandint(len(indices))
        if replace:
            ind = indices[indptr]
        else:
            ind = indices.pop(indptr)
        result.append(a[ind])
    #
    return result


print get_quantum_bits()
candidates = "Bjarke, Niels, Siri, Freja, Emil".split(", ")
print qchoice(candidates, 2, replace = False)

# TODO skriv det om til et RandomState-objekt


