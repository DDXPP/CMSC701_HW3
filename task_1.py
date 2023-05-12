# https://pypi.org/project/bloom-filter2/
# https://github.com/remram44/python-bloom-filter/tree/master 

from bloom_filter2 import BloomFilter
from random import shuffle
from random import choices
import string
import time
from numpy import array, average
import numpy as np



def test_run(size, false_positive_rate, pos_key_percentage):
    K = []
    K_prime = []
    K_absent = []

    count_false_positive = 0
    count_false_negative = 0
    count_present = 0
    count_not_present = 0

    BF = BloomFilter(size, false_positive_rate)

    t1 = time.time()
    for i in range(size):
        new_key = "".join(choices(string.ascii_lowercase, k=16))
        if new_key not in K:
            K.append(new_key)
            BF.add(new_key)
    t2 = time.time()
    # print("done creating K")
    # print(t2-t1)


    t3 = time.time()
    for i in range(int(size * (1 - pos_key_percentage))):
        new_key = "".join(choices(string.ascii_lowercase, k=16))
        if new_key not in K:
            K_absent.append(new_key)
    shuffle(K)
    K_prime = K_absent + K[0:int(size * pos_key_percentage)]
    shuffle(K_prime)
    t4 = time.time()
    # print("done creating K'")
    # print(t4-t3)

    time_start = time.time()
    for key in K_prime:
        if key in BF:
            if key in K_absent:
                count_false_positive += 1
            else:
                count_present += 1
        else:
            if key in K:
                count_false_negative += 1
                raise Exception("Date provided can't be in the past")
            else:
                count_not_present += 1
    time_end = time.time()
    time_elapsed = time_end - time_start

    actual_false_positive_rate = count_false_positive/size


    # print(actual_false_positive_rate)
    # print(time_elapsed)
    # print(BF.num_bits_m)

    return [actual_false_positive_rate, time_elapsed, BF.num_bits_m]        


sizes = [1000, 10000, 100000]
false_positive_rates = [1/pow(2, 7), 1/pow(2, 8), 1/pow(2, 10)]
pos_key_percentages = [0.1, 0.25, 0.5]

for size in sizes:
    for false_positive_rate in false_positive_rates:
        fpr_string = "1/(2^7)" if (false_positive_rate == false_positive_rates[0]) else ("1/(2^8)" if (false_positive_rate == false_positive_rates[1]) else "1/(2^10)"      )
        for pos_key_percentage in pos_key_percentages:
            results = []
            for i in range(1 if size == 100000 else 5):
                results.append(test_run(size, false_positive_rate, pos_key_percentage))
            average_results = [sum(sub_list) / len(sub_list) for sub_list in zip(*results)]
            print("Results for querying {} keys with {} expected FPR and {} positive keys rate in K': {} actual FPR, {} seconds, {} bits BF"
                  .format(size, fpr_string, pos_key_percentage, round(average_results[0], 8), round(average_results[1], 8), round(average_results[2]) ))
                
                
                