import unittest

import torch

from arraycontract.shape_contract import shape, _


@shape(x=(3, 4,'N1'), y=('N1', 2, _), z=('N2', ...))
def f1(x, y, z):
    pass

@shape((3,...))
def f2(x):
    pass

@shape((3, _), (_, ))
def f3(x, y):
    pass

@shape(x=(3, 'N'), y=('N',))
def f4(x, y):
    pass

@shape((1,...,3), (...,4,5))
def f5(x, y):
    pass

class ShapeTest(unittest.TestCase):
    def test_ok(self):
        N1 = 5
        N2 = 6
        f1(torch.rand(3, 4, N1), torch.rand(N1, 2, 10), z=torch.rand(N2, 3, 3))

    def test_ellipsis1(self):
        f2(torch.rand(3,4))
        f2(torch.rand(3,4,5))
        f2(torch.rand(3,4,5,6))
        f2(torch.rand(3,4,5,6,7))

    def test_ellipsis2_ok(self):
        f5(torch.rand(1, 4, 3), torch.rand(1,2,3,4,5))
        f5(torch.rand(1, 4, 6, 3), torch.rand(4, 5))


    def test_underscore(self):
        undefined = 4
        f3(torch.rand(3, undefined), torch.rand(undefined))

    def test_underscore_wrong1(self):
        try:
            f3(torch.rand(4,3), torch.rand(2,))
        except AssertionError as e:
            self.assertEqual('Expect x.shape[0] == 3, got 4', str(e))
            return
        self.assertTrue(False)

    def test_underscore_wrong2(self):
        try:
            f3(torch.rand(3, 4), torch.rand(2, 2))
        except AssertionError as e:
            self.assertEqual('Expect y.ndim == 1, got 2', str(e))
            return
        self.assertTrue(False)

    def test_variable_wrong(self):
        try:
            N = 5
            f4(torch.rand(3, N + 1), torch.rand(N))
        except AssertionError as e:
            self.assertEqual('Expect y.shape[0] == x.shape[1], got 5, 6 respectively', str(e))
            return
        self.assertTrue(False)