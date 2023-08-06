import inspect

import torch
import unittest

from arraycontract.ndim_contract import ndim


@ndim(x=3, y=4)
def f1(x, y, z):
    pass

@ndim(x=0)
def f2(x):
    pass

class NdimTest(unittest.TestCase):
    def test_ok(self):
        f1(torch.rand(2,3,4), y=torch.rand(2,3,4,5), z=torch.rand(1))
        f2(torch.tensor(1))

    def test_wrong(self):
        try:
            f1(torch.rand(2,3,4), y=torch.rand(4,5), z=torch.rand(1))
        except AssertionError as e:
            self.assertEqual('Expect ndim of `y` is `4`, got `2`', str(e))
            return
        self.assertTrue(False)
