import json
import pandas as pd
import rsa
import numpy as np
import math
from batch_gcd import batchgcd_faster
import random

from multiprocessing import Pool
from timeit import default_timer as timer


def partition(list_in, n):
    random.shuffle(list_in)
    return [list_in[jj::n] for jj in range(n)]


def choose_iteration(D, p, eps):
    return math.ceil(math.log(1-eps) / (math.log(D - D/p) - math.log(D-1)))


if __name__ == '__main__':
    print("Load data")
    with open('../Zad3/certs.02_2020.json') as json_file:
        data_certs = [json.loads(line) for line in json_file]
    df_certs = pd.DataFrame(data_certs, dtype='object')
    # remove elliptical curves (no RSA key)
    df_certs = df_certs[df_certs['rsa_PEM'].notnull()]
    # remove duplicates
    df_certs = df_certs.drop_duplicates(subset='rsa_PEM')

    pubkey_list = []
    for site in df_certs['rsa_PEM']:
        pubkey = rsa.PublicKey.load_pkcs1(site)
        pubkey_list.append(pubkey)

    numbers = []
    for pubkey in pubkey_list:
        numbers.append(pubkey.n)

    print("parallel gcd")
    num_processors = 8
    D = len(numbers)
    m = D/num_processors
    p = num_processors  # ceil(D/m)

    eps = 0.8
    k = choose_iteration(D, p, eps)
    print("D: {}, p: {}\n{} repetitions for {}% accuracy".format(D, p, k, eps*100))

    # # Applying the function sequentially
    # tic = timer()
    # for i in range(k):
    #     d = partition(numbers, p)
    #     v = [batchgcd_faster(X) for X in d]
    #     # print(v)
    #     V1 = v.pop()
    #     while v:
    #         V1 = np.union1d(V1, v.pop())
    # print("Final:")
    # print(V1)
    # tac = timer()
    # print("time for sequential sorting: ", tac - tic)

    # Using multiprocessing
    pool = Pool(processes=num_processors)
    tic = timer()
    V = []
    for ii in range(k):
        print("rep: {}".format(ii+1))
        d = partition(numbers, p)
        v = pool.map(batchgcd_faster, d)
        V1 = v.pop()
        while v:
            V1 = np.union1d(V1, v.pop())
        V.append(V1)
        print(V)
    result = V.pop()
    while V:
        result = np.union1d(result, V.pop())
    print("Final result:")
    print(result)
    tac = timer()
    print("# time for parallel sorting: {}s\t|| num_proc: {}\t|| k: {} \t|| D: {}".format(round(tac-tic,6), num_processors, k, D))

    with open('parallel_batchgcd_result.txt', 'w') as f:
        for item in result:
            f.write("%s\n" % item)

# sequential time
# time for sequential sorting:  282.9629608s || D: 3200

# 80% accuracy times
# time for parallel sorting: 141.20569s	|| num_proc: 2	|| k: 3 	|| D: 3200
# time for parallel sorting: 82.062475s	|| num_proc: 4	|| k: 6 	|| N: 3200
# time for parallel sorting: 79.740984s	|| num_proc: 6	|| k: 9 	|| D: 3200
# time for parallel sorting: 76.168169s || num_proc: 8  || k: 13    || D: 3200
# time for parallel sorting: 78.978624s || num_proc: 16 || k: 26    || D: 3200
# time for parallel sorting: 84.261154s || num_proc: 24 || k: 39    || D: 3200

# 95% accuracy times
# time for parallel sorting: 233.0475s	|| num_proc: 2	|| k: 5 	|| D: 3200
