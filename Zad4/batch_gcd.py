import numpy as np
import math


def producttree(X):
    result = [X]
    while len(X) > 1:
        X = [np.prod(X[int(i*2):int((i+1)*2)]) for i in range(int((len(X)+1)/2))]
        result.append(X)
    return result


def batchgcd_faster(X, verbose=True):
    counter = 1
    prods = producttree(X)
    R = prods.pop()
    while prods:
        X = prods.pop()
        R = [R[math.floor(i/2)] % X[i]**2 for i in range(len(X))]
        counter += counter
        if verbose and counter % 1000 == 0:
            print(counter)
    return [math.gcd(r//n, n) for r, n in zip(R, X)]
