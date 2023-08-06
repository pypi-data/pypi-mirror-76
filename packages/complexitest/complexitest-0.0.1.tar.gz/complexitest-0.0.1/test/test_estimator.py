import unittest
import numpy as np
import random
from complexitest import estimator


class EstimatorTestCase(unittest.TestCase):
    def test_constant(self):
        def do_nothing(n):
            return n

        complexity = estimator.estimate_complexity(
            do_nothing,
            lambda n: (n, ),
        )
        self.assertEqual(complexity, estimator.CONSTANT)

    def test_log_function(self):
        def add_log(l, start=0):
            if start == len(l) - 1:
                return 0
            return l[start] + add_log(l, (start + len(l)) // 2)

        complexity = estimator.estimate_complexity(
            add_log,
            lambda n: (np.random.randint(1000, size=n).tolist(), ))
        self.assertEqual(complexity, estimator.LOG)

    def test_linear_function(self):
        def add_all(l):
            s = 0
            for i in l:
                s += i
            return s

        complexity = estimator.estimate_complexity(
            add_all, lambda n: (np.random.randint(1000, size=n).tolist(), ))
        self.assertEqual(complexity, estimator.LINEAR)

    def test_quadratic_function(self):
        def add_all(l):
            s = 0
            for i in l:
                for j in l:
                    s += i + j
            return s

        complexity = estimator.estimate_complexity(
            add_all, lambda n: (np.random.randint(1000, size=n).tolist(), ))
        self.assertEqual(complexity, estimator.QUADRATIC)

    def test_cubic_function(self):
        def add_all(l):
            s = 0
            for i in l:
                for j in l:
                    for k in l:
                        s += i + j + k
            return s

        complexity = estimator.estimate_complexity(
            add_all, lambda n: (np.random.randint(1000, size=n).tolist(), ))
        self.assertEqual(complexity, estimator.CUBIC)

    def test_exponential_function(self):
        def rec(n, i=0):
            if i == n:
                return 1
            return rec(n, i + 1) + rec(n, i + 1)

        complexity = estimator.estimate_complexity(rec, lambda n: (n, ))
        self.assertEqual(complexity, estimator.EXPONENTIAL)

    def test_factorial_function(self):
        def permutations(l):
            if not l:
                return []
            ret = []
            for i, el in enumerate(l):
                ret.append([el] + permutations(l[:i] + l[i + 1:]))
            return ret

        complexity = estimator.estimate_complexity(
            permutations, lambda n: (np.random.randint(1000, size=n).tolist(), ))
        self.assertEqual(complexity, estimator.FACTORIAL)
