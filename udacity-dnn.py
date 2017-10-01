import numpy as np
from numpy.testing import assert_almost_equal
from math import log

def softmax(L):
    # https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
    return np.exp(L) / np.exp(L).sum()

def cross_entropy(Y, P):
    result = 0
    for ind in range(len(Y)):
        result -= Y[ind] * log(P[ind]) + (1 - Y[ind]) * log(1 - P[ind])
    return result

# from udacity solution:
def cross_entropy_elegant(Y, P):
    Y = np.float_(Y)
    P = np.float_(P)
    return -np.sum(Y * np.log(P) + (1 - Y) * np.log(1 - P))

def main():
    sm = softmax([5,6,7])
    # https://stackoverflow.com/questions/3302949/whats-the-best-way-to-assert-for-numpy-array-equality
    assert_almost_equal ([0.090030573170380462, 0.24472847105479764, 0.6652409557748219], sm)
    ce = cross_entropy([1, 0, 1, 1], [0.4,0.6,0.1,0.5])
    assert_almost_equal (4.8283137373, ce)
    
    print (" well done !")
if __name__ == "__main__":
    main()