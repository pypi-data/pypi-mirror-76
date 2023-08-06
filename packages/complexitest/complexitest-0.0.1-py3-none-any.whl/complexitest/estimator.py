import sys
import numpy as np
import itertools
import math
from .timer import timeout, Timer

CONSTANT = 'constant'  # Doesn't work... keeps mistaking it for log
LOG = 'logarithmic'
LINEAR = 'linear'
QUADRATIC = 'quadratic'
CUBIC = 'cubic'
EXPONENTIAL = 'exponential'
FACTORIAL = 'factorial'

NON_POLYNOMIAL = [
    EXPONENTIAL,
    FACTORIAL,
]

COMPLEXITY_CLASSES = {
    CONSTANT: lambda n: [1],
    LOG: lambda n: [math.log(n, 2), 1],
    LINEAR: lambda n: [n, 1],
    QUADRATIC: lambda n: [n**2, 1],
    CUBIC: lambda n: [n**3, 1],
    EXPONENTIAL: lambda n: [2**n, 1],
    FACTORIAL: lambda n: [math.factorial(n), 1],
}


def _test_complexities(times, is_non_poly=False):
    complexities = {}
    for complexity, func in COMPLEXITY_CLASSES.items():
        if (not is_non_poly and complexity in NON_POLYNOMIAL) or \
           (is_non_poly and complexity not in NON_POLYNOMIAL):
            continue
        a, b = zip(*[[func(n), t] for n, t in times.items()])
        try:
            x, residuals, _, _ = np.linalg.lstsq(a, b, rcond=None)
            if residuals.size > 0:
                complexities[complexity] = x, residuals
        except TypeError:
            pass
    return complexities


class NGenerator:
    def __init__(self, min_n=1, max_n=None, max_non_poly=30, samples=100):
        self.min_n = min_n
        self.max_n = max_n
        self.is_non_poly = False
        self.max_non_poly = max_non_poly
        self.samples = samples
        self._timed_out = False
        self.n = 0

    def generate(self):
        count = 0
        used = set()
        largest_n = self.min_n
        searching_largest = False

        start = self.min_n
        self.n = None
        self._timed_out = False
        while count < self.samples:
            if self.n is None:
                self.n = start
            elif self._timed_out:
                break
            else:
                largest_n = max(self.n, largest_n)
                self.n *= 2
            self._timed_out = False
            if self.n in used:
                break
            if self.max_n and self.n > self.max_n:
                largest_n = self.max_n
                break
            yield self.n
            used.add(self.n)
            count += 1

        largest_n = max(largest_n, self.max_non_poly)
        self.n = self.min_n
        while count < self.samples:
            if self.n >= largest_n or self._timed_out:
                self.n = self.min_n
            self._timed_out = False
            yield self.n
            count += 1
            self.n += 1

    def timed_out(self):
        if self.n < self.max_non_poly:
            self.is_non_poly = True
        self._timed_out = True


def estimate_complexity(f,
                        args_generator,
                        kwargs_generator=lambda n: {},
                        min_n=1,
                        max_n=None,
                        max_wait=0.01,
                        gen_max_wait=0.1,
                        samples=100,
                        max_non_poly=30,
                        show_plot=False,
                        ret_pts=False):
    """
    Estimates the complexity for function f

    Args:
        f: Target function
        args_generator: Function that returns the arguments for a given input size n or tuple of Functions (in this case we choose the worst time)
        kwargs_generator: Function that returns the arguments for a given input size n or tuple of Functions (in this case we choose the worst time)
        min_n: Starting value for n
        max_n: Maximum value for n (ignored if None)
        max_wait: Timeout duration
        gen_max_wait: Timeout for arguments generation
        samples: Number of samples to use for complexity estimation
        max_non_poly: Maximum number to consider factorial and exponential as possible solutions
        show_plot: Whether to show plot or not
        ret_pts: Whether to also return points
    """
    def make_return(ret, pts=None):
        if ret_pts:
            return ret, pts
        return ret

    if not isinstance(args_generator, tuple):
        args_generator = (args_generator, )
    if not isinstance(kwargs_generator, tuple):
        kwargs_generator = (kwargs_generator, )
    times = {}
    gen = NGenerator(min_n=min_n, max_n=max_n, samples=samples, max_non_poly=max_non_poly)
    timer = Timer()
    for n in gen.generate():
        if n > 2147483647:  # Some arbitrary big number (maxint)
            return make_return(CONSTANT)
        alt_times = []
        timed_out = False
        for args_g, kwargs_g in itertools.product(args_generator, kwargs_generator):
            try:
                with timeout(gen_max_wait):
                    args = args_g(n)
                with timeout(gen_max_wait):
                    kwargs = kwargs_g(n)
                with timeout(max_wait), timer:
                    f(*args, **kwargs)
                alt_times.append(timer.elapsed)
                if timer.elapsed > max_wait:  # This may occur when the code captures the TimeoutError in a try except.
                    gen.timed_out()
                    timed_out = True
            except (TimeoutError, RecursionError):
                gen.timed_out()
                timed_out = True
        if alt_times and not timed_out:
            new_time = max(alt_times)
            if n not in times or times[n] < new_time:
                times[n] = new_time
    complexities = _test_complexities(times, gen.is_non_poly)
    ret, (ret_x, _) = min(complexities.items(), key=lambda v: v[1][1])
    pts = [(k, v, COMPLEXITY_CLASSES[ret](k) @ ret_x) for k, v in times.items()]
    if show_plot:
        import matplotlib.pyplot as plt

        plt.plot(list(times.keys()), list(times.values()))
        for complexity, (x, _) in complexities.items():
            func = COMPLEXITY_CLASSES[complexity]
            plt.plot(list(times.keys()), [func(n) @ x for n in times])
        plt.show()
    return make_return(ret, pts)


if __name__ == "__main__":
    from random import randint

    def f(l):
        total = 0
        for i in l:
            for j in l:
                total += i + j
        return total

    complexity = estimate_complexity(f,
                                     lambda n:
                                     ([randint(0, 1000) for _ in range(n)], ),
                                     show_plot=True)
    print(complexity)
