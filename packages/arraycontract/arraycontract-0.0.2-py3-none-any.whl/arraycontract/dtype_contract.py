from collections import OrderedDict
from functools import wraps

from arraycontract.common import Trigger, __Closure


class DtypeClosure(__Closure):
    def __call__(self, *args, **kwargs):
        bound_arguments: OrderedDict = self.func_signature.bind(*args, **kwargs).arguments
        for name, dtype in self.bound_constraints.items():
            assert bound_arguments[name].dtype == dtype, \
                f'Expect dtype of `{name}` is `{dtype}`, got `{bound_arguments[name].dtype}`'
        return self.func(*args, **kwargs)


def dtype(*constraints, **kwconstraints):
    def decorator(func):
        __enabled__ = kwconstraints.pop('__enabled__') if '__enabled__' in kwconstraints else True
        if not Trigger.dtype_check_trigger or not __enabled__:
            return func
        return wraps(func)(DtypeClosure(func, constraints, kwconstraints))
    return decorator