# CMSC701 Homework 3 : Evaluating two different AMQs

Name: Elliot Huang

GitHub repo: https://github.com/DDXPP/CMSC701_HW3



## References

- [bloom-filter2](https://github.com/remram44/python-bloom-filter): a Python bloom filter builder
- [pybbhash](https://github.com/dib-lab/pybbhash): a Python (Cython) wrapper for the BBHash codebase for building minimal perfect hash functions
- General Python references: [Python official docs](https://docs.python.org/3/reference/), [W3Schools](https://www.w3schools.com/python/python_reference.asp)
- [Stack Overflow](https://stackoverflow.com/questions/12372531/reading-and-writing-a-stdvector-into-a-file-correctly) for miscellaneous issues.
- Lecture [slides](https://rob-p.github.io/CMSC701_S23/lectures/)



## Instructions

### Task 1 — Empirical evaluation of the bloom filter

- Install `bloom-filter2`  using the command `pip install bloom-filter2`. 
- Run this task using the command `python task_1.py`.
- The results will be printed out in the command line. The results include the observed false positive rate, time used, and the bloom filter size when querying on sets with various key sizes and with various mixtures of “positive” and “negative” keys. The results also include the same three output values when the expected false positive rates are set different. 

### Task 2 — Empirical evaluation of a minimal perfect hash

- Install `pybbhash`, a Python wrapper for `BBHash`, using the command `pip install bbhash`.
- Run this task using the command `python task_2.py`.
- The results will be printed out in the command line. The results include the observed false positive rate, time used, and the MPHF size.



### Task 3 — Augment the MPHF with a “fingerprint array”

- Run this task using the command `python task_3.py`.
- The results will be printed out in the command line. The results include the observed false positive rate, time used, and the combined size of MPHF and the fingerprint array. 

