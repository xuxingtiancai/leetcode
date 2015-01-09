###
from itertools import *

class ArrayIter:
    def __init__(self, L, begin):
        self.L = L
        self.begin = begin
        self.current = begin

    def __iter__(self):
        return self

    def next(self):
        if self.current >= len(self.L):
            raise StopIteration
        result = self.L[self.current]
        self.current += 1
        return result
        
def collect(aggr, initial):
    def collect_main(fn):
        def wrapper(*args):
            return reduce(aggr, fn(*args), initial)
        return wrapper
    return collect_main


@collect(max, 0)
def LCS(A, B):
    if len(A) == 0 or len(B) == 0:
        yield 0
        return

    yield LCS_align(A, B)
    for i in range(1, len(A)):
        yield LCS_align(ArrayIter(A, i), B)
    for j in range(1, len(B)):
        yield LCS_align(A, ArrayIter(B, j))


@collect(max, 0)
def LCS_align(A, B):
    for key, group in groupby(izip(A, B), lambda (a, b) : a == b):
        if key:
            yield sum(1 for tup in group)


if __name__ == '__main__':
    print LCS('abcde', 'bcfd')
