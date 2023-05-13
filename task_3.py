# https://github.com/dib-lab/pybbhash
# https://pypi.org/project/bbhash/
# pip install bbhash

import os
import bbhash
from random import shuffle
from random import choices
import random
import time

def test_run(size, pos_key_percentage, b):
    K = []
    K_prime = []
    K_absent = []
    fingerprint_array = [0 for i in range(size)]

    count_false_positive = 0
    count_false_negative = 0
    count_present = 0
    count_not_present = 0

    # generate K and K'
    for i in range(size):
        new_key = random.randint(0, 2**32-1)
        if new_key not in K:
            K.append(new_key)
            
    for i in range(int(size * (1 - pos_key_percentage))):
        new_key = random.randint(0, 2**32-1)
        if new_key not in K:
            K_absent.append(new_key)
    shuffle(K)
    K_prime = K_absent + K[0:int(size * pos_key_percentage)]
    shuffle(K_prime)

    # build MPHF
    num_threads = 1 
    gamma = 1.0     
    MPH = bbhash.PyMPHF(K, len(K), num_threads, gamma)
    
    tmp_filename = "temp_file"
    MPH.save(tmp_filename)
    MPH_size = os.path.getsize(tmp_filename)
    
    # build fingerprint_array
    for key in K:
        index_h = MPH.lookup(key)
        last_bits = bin(hash(key))[-int(b):]
        fingerprint_array[index_h] = last_bits
        
    fingerprint_size = 0
    for fingerprint in fingerprint_array:
        fingerprint_size += len(str(fingerprint))
    
    # Query
    time_start = time.time()
    for key in K_prime:
        read = MPH.lookup(key)
        
        if read != None:
            fingerprint = fingerprint_array[read]
            h = bin(hash(key))[-int(b):]
            if fingerprint == h:    
                if key in K:
                    count_present += 1
                else:
                    count_false_positive += 1
            else:
                if key in K:
                    count_false_negative += 1
                    raise Exception("Date provided can't be in the past")
                else:
                    count_not_present += 1
        else:
            if key in K:
                count_false_negative += 1
                raise Exception("Date provided can't be in the past")
            else:
                count_not_present += 1
    time_end = time.time()
    time_elapsed = time_end - time_start

    actual_false_positive_rate = count_false_positive/size
    # print(count_false_positive, count_false_negative, count_present, count_not_present, actual_false_positive_rate)
    return [actual_false_positive_rate, time_elapsed, MPH_size * 8 + fingerprint_size]        


sizes = [1000, 10000, 100000]
pos_key_percentages = [0.1, 0.25, 0.5, 0.75]
bs = [7, 8, 10]

for size in sizes:
    for pos_key_percentage in pos_key_percentages:
        for b in bs:
            results = []
            for i in range(1 if size == 100000 else 5):
                results.append(test_run(size, pos_key_percentage, b))
            average_results = [sum(sub_list) / len(sub_list) for sub_list in zip(*results)]
            print("Results for querying {} keys with b = {} and with {} positive keys rate in K': {} observed FPR, {} seconds, total size {} bits"
                    .format(size, b, pos_key_percentage, round(average_results[0], 8), round(average_results[1], 8) , round(average_results[2]) ))            
 
 