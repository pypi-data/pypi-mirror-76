from collections import OrderedDict
from functools import wraps
from typing import Tuple, Dict, Optional

from arraycontract.common import Trigger, __Closure

_ = '_'

class TwoManyEllipsisException(Exception):
    pass

def shape_to_constraints(shape: tuple) -> Tuple[dict, Optional[int]]:
    """
    :param shape:
    :return:
        - constraints
        - ddim: if not None: then assert argument[idx].ndim == ndim; else not check
    """
    ellipsis_count = shape.count(Ellipsis)
    assert ellipsis_count <= 1, f'Number of Ellipsis should be <= 1'
    if ellipsis_count == 0:
        return {idx: dim for idx, dim in enumerate(shape) if dim != '_'}, len(shape)
    if len(shape) == 0:
        return dict(), None
    #
    constraints = dict()
    idx = 0
    while shape[idx] != Ellipsis:
        if shape[idx] != _:
            constraints[idx] = shape[idx]
        idx += 1
    limit = idx - len(shape)
    for idx in range(-1, limit, -1):
        if shape[idx] != _:
            constraints[idx] = shape[idx]
    return constraints, None


def refine_bound_constraints(bound_constraints: OrderedDict) -> OrderedDict:
    """
    :param bound_constraints:
    :return:
        OrderedDict[str, Dict[int, Union[int, Tuple[str, int]]]
            - key: name of argument
            - value:
                - key: dim_idx
                - value: dim (int) or (name of another argument, dim_idx)
    """
    dim_nameidx_reverse_map: Dict[int, Tuple[str, int]] = dict()
    new_bound_constraints = OrderedDict()
    for name, constraints in bound_constraints.items():
        new_constraints = dict()
        for idx, dim in constraints.items():
            if type(dim) == str:
                if dim not in dim_nameidx_reverse_map:
                    dim_nameidx_reverse_map[dim] = (name, idx)
                else:
                    new_constraints[idx] = dim_nameidx_reverse_map[dim]
            else:
                new_constraints[idx] = dim
        new_bound_constraints[name] = new_constraints
    return new_bound_constraints


class ShapeClosure(__Closure):
    def __init__(self, func, constraints, kwconstraints):
        super().__init__(func, constraints, kwconstraints)
        name2constraints = {name: shape_to_constraints(shape) for name, shape in self.bound_constraints.items()}
        self.name2ndim = {name: ndim for name, (constraints, ndim) in name2constraints.items() if ndim is not None}
        self.bound_constraints = OrderedDict(
            (name, constraints)
            for name, (constraints, ndim) in name2constraints.items()
            if len(constraints) != 0
        )
        self.bound_constraints = refine_bound_constraints(self.bound_constraints)


    def __call__(self, *args, **kwargs):
        arguments: OrderedDict = self.func_signature.bind(*args, **kwargs).arguments
        for name, ndim in self.name2ndim.items():
            assert arguments[name].ndim == ndim, f'Expect {name}.ndim == {ndim}, got {arguments[name].ndim}'
        for name, constraints in self.bound_constraints.items():
            for dim_idx, dim in constraints.items():
                if type(dim) == tuple:
                    name_ref, dim_idx_ref = dim
                    assert arguments[name].shape[dim_idx] == arguments[name_ref].shape[dim_idx_ref], \
                        f'Expect {name}.shape[{dim_idx}] == {name_ref}.shape[{dim_idx_ref}], ' \
                        f'got {arguments[name].shape[dim_idx]}, {arguments[name_ref].shape[dim_idx_ref]} respectively'
                else:
                    assert arguments[name].shape[dim_idx] == dim, \
                        f'Expect {name}.shape[{dim_idx}] == {dim}, got {arguments[name].shape[dim_idx]}'
        return self.func(*args, **kwargs)


def shape(*constraints, **kwconstraints):
    def decorator(func):
        __enabled__ = kwconstraints.pop('__enabled__') if '__enabled__' in kwconstraints else True
        if not Trigger.shape_check_trigger or not __enabled__:
            return func
        return wraps(func)(ShapeClosure(func, constraints, kwconstraints))
    return decorator

