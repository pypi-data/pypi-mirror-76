# ArrayContract

```python
from arraycontract import shape, _
import torch

@shape(x=(_, 'N'), y=('N', _))
def matrix_dot(x, y):
    return x @ y

matrix_dot(torch.rand(3,4), torch.rand(4,5)) # OK
matrix_dot(torch.rand(3,4), torch.rand(3,5)) # raise AssertionError
```

```python
from arraycontract import shape, _
import torch
from torch import nn

linear = nn.Linear(3, 4)

@shape((..., 3))
def forward_linear(x):
    """
    requires x.shape[-1] == 3
    """
    return linear(x)

forward_linear(torch.rand(4,5,3)) # OK
forward_linear(torch.rand(4,4)) # raise AssertionError
```

```python
from arraycontract import dtype
from arraycontract import ndim
import torch

@ndim(x=3, y=4)
def ndim_contract(x, y):
    print("requires x.ndim == 3 and y.ndim == 4")

@dtype(x=torch.long)
def dtype_contract(x):
    print("requires x.dtype == torch.long")
```

```python
from arraycontract import Trigger
from arraycontract import dtype
import torch

Trigger.dtype_check_trigger = False

@dtype(x=torch.long)
def dtype_contract(x):
    print("not requires x.dtype == torch.long")

dtype_contract(torch.rand(3, 4).float()) # OK
```