import unittest
import numpy as np
import random
import string
from types import ModuleType
from pathlib import Path
from complexitest import estimator


order = {
    estimator.CONSTANT: 1,
    estimator.LOG: 2,
    estimator.LINEAR: 3,
    estimator.QUADRATIC: 4,
    estimator.CUBIC: 5,
    estimator.EXPONENTIAL: 6,
    estimator.FACTORIAL: 7,
}


class LeetCodeEstimatorTestCase(unittest.TestCase):
    def solutions(self, problem, extra_code=''):
        problem_dir = Path(__file__).parent / 'leet_code' / problem
        for filename in problem_dir.glob('*.py'):
            print(filename)
            with open(filename) as f:
                solution_name = filename.name
                expected_times = [t for t in solution_name.split('_') if not t.isnumeric()]
                _module = ModuleType('user_module')
                exec('from typing import *', _module.__dict__)
                exec('import collections', _module.__dict__)
                exec('import math', _module.__dict__)
                exec('import itertools', _module.__dict__)
                exec(extra_code, _module.__dict__)
                exec(f.read(), _module.__dict__)
                solution = _module.Solution()
                yield solution, expected_times, solution_name

    def test_two_sum(self):
        def gen(choose_i1i2):
            def g(n):
                numbers = np.random.randint(1000, size=n).tolist()
                i1, i2 = choose_i1i2(n)
                ts = numbers[i1] + numbers[i2]
                for i in range(n):
                    if i not in (i1, i2):
                        numbers[i] += ts + 1
                return numbers, ts
            return g

        for solution, expected_times, solution_name in self.solutions('two_sum'):
            complexity = estimator.estimate_complexity(
                solution.twoSum,
                (
                    gen(lambda n: (n - 2, n - 1)),
                    gen(lambda n: (0, 1)),
                ),
                min_n=10,
                samples=1000
            )
            self.assertEqual(complexity, expected_times[0], msg=f"Didn't work for {solution_name}")

    def test_zigzag(self):
        def gen(n):
            letters = string.ascii_uppercase
            s = ''.join(random.choice(letters) for i in range(n))
            num_rows = random.randrange(1, n)
            return s, num_rows

        for solution, expected_times, solution_name in self.solutions('zigzag'):
            complexity = estimator.estimate_complexity(
                solution.convert,
                gen,
                min_n=10,
                samples=1000
            )
            self.assertLessEqual(order[complexity], order[expected_times[0]], msg=f"Didn't work for {solution_name}")

    def test_trapping_rain_water(self):
        def gen_len(n):
            return (np.random.randint(100, size=n).tolist(), )

        heights = np.random.randint(10, size=100).tolist()
        def gen_high(n):
            return ([h * n for h in heights], )

        for solution, expected_times, solution_name in self.solutions('trapping_rain_water'):
            complexity = estimator.estimate_complexity(
                solution.trap,
                gen_len,
                min_n=10,
                samples=1000
            )
            self.assertEqual(complexity, expected_times[0], msg=f"Didn't work for {solution_name}")

            complexity = estimator.estimate_complexity(
                solution.trap,
                gen_high,
                min_n=1,
                samples=1000
            )
            self.assertEqual(complexity, expected_times[1], msg=f"Didn't work for {solution_name}")

    def test_all_possible_full_binary_trees(self):
        extra_code = '''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        '''

        for solution, expected_times, solution_name in self.solutions('all_possible_full_binary_trees', extra_code):
            complexity = estimator.estimate_complexity(
                solution.allPossibleFBT,
                lambda n: (n if n % 2 == 1 else n + 1, ),  # Only makes sense for odd numbers
                min_n=1,
                samples=1000
            )
            self.assertEqual(complexity, expected_times[0], msg=f"Didn't work for {solution_name}")

    def test_bitwise_ors_of_subarrays(self):
        for solution, expected_times, solution_name in self.solutions('bitwise_ors_of_subarrays'):
            complexity = estimator.estimate_complexity(
                solution.subarrayBitwiseORs,
                lambda n: (np.random.randint(int(1e9), size=n).tolist(), ),
                min_n=1,
                samples=1000,
            )
            self.assertLessEqual(order[complexity], order[expected_times[0]], msg=f"Didn't work for {solution_name}")

    def test_kth_symbol_in_grammar(self):
        def gen_n(n):
            k = 1
            return n, k

        def gen_k(k):
            n = 15
            if k > 2**(n-1):
                k = 2**(n-1) - 1
            return n, k

        for solution, expected_times, solution_name in self.solutions('kth_symbol_in_grammar'):
            complexity = estimator.estimate_complexity(
                solution.kthGrammar,
                gen_n,
                min_n=1,
                samples=1000,
                max_non_poly=20,
            )
            self.assertLessEqual(order[complexity], order[expected_times[0]], msg=f"Didn't work for {solution_name}")

            complexity = estimator.estimate_complexity(
                solution.kthGrammar,
                gen_k,
                min_n=1,
                max_n=2**14,
                samples=1000,
            )
            self.assertLessEqual(order[complexity], order[expected_times[1]], msg=f"Didn't work for {solution_name}")

    def test_max_product_word_length(self):
        def gen_word(l):
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

        def gen_words(n):
            return [gen_word(10) for _ in range(n)],

        def gen_lengths(n):
            return [gen_word(n) for _ in range(10)],

        for solution, expected_times, solution_name in self.solutions('max_product_word_length'):
            complexity = estimator.estimate_complexity(
                solution.maxProduct,
                gen_words,
                min_n=2,
                samples=100,
            )
            self.assertLessEqual(order[complexity], order[expected_times[0]], msg=f"Didn't work for {solution_name}")

            complexity = estimator.estimate_complexity(
                solution.maxProduct,
                gen_lengths,
                min_n=2,
                samples=100,
            )
            self.assertLessEqual(order[complexity], order[expected_times[1]], msg=f"Didn't work for {solution_name}")

    def test_rotate_image(self):
        for solution, expected_times, solution_name in self.solutions('rotate_image'):
            complexity = estimator.estimate_complexity(
                solution.rotate,
                lambda n: (np.random.randint(256, size=(n, n)).tolist(), ),
                min_n=1,
                samples=100,
            )
            self.assertEqual(complexity, expected_times[0], msg=f"Didn't work for {solution_name}")

    def test_jump_game_ii(self):
        for solution, expected_times, solution_name in self.solutions('jump_game_ii'):
            complexity = estimator.estimate_complexity(
                solution.jump,
                lambda n: (np.random.randint(1, min(n, 5), size=n).tolist(), ),
                min_n=2,
                samples=500,
            )
            self.assertLessEqual(order[complexity], order[expected_times[0]], msg=f"Didn't work for {solution_name}")

    def test_first_missing_positive(self):
        def gen(n):
            l = list(range(1, n+1))
            random.shuffle(l)
            return l,

        for solution, expected_times, solution_name in self.solutions('first_missing_positive'):
            complexity = estimator.estimate_complexity(
                solution.firstMissingPositive,
                gen,
                min_n=1,
                samples=100,
            )
            self.assertEqual(order[complexity], order[expected_times[0]], msg=f"Didn't work for {solution_name}")

    def test_valid_parentheses(self):
        def gen(n):
            if n % 2 == 1:
                n += 1
            op = n // 2
            cl = n // 2
            ret = ''
            while op or cl:
                if op >= cl:
                    op -= 1
                    ret += '('
                elif op > 0:
                    if random.choice((0, 1)):
                        op -= 1
                        ret += '('
                    else:
                        cl -= 1
                        ret += ')'
                else:
                    cl -= 1
                    ret += ')'
            return ret,

        for solution, expected_times, solution_name in self.solutions('valid_parentheses'):
            complexity = estimator.estimate_complexity(
                solution.isValid,
                gen,
                min_n=2,
                samples=100,
            )
            self.assertEqual(order[complexity], order[expected_times[0]], msg=f"Didn't work for {solution_name}")
