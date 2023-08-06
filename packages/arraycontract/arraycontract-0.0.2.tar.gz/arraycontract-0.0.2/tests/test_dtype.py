import unittest

from arraycontract.dtype_contract import dtype
import torch


@dtype(x=torch.long, y=torch.float)
def f1(x, y):
    pass

class DtypeTest(unittest.TestCase):
    def test_ok(self):
        f1(torch.rand(3,4).long(), torch.rand(4,5))

    def test_wrong(self):
        try:
            f1(torch.rand(3,4), torch.rand(4,5))
        except AssertionError as e:
            self.assertEqual('Expect dtype of `x` is `torch.int64`, got `torch.float32`', str(e))
            return
        self.assertTrue(False)
