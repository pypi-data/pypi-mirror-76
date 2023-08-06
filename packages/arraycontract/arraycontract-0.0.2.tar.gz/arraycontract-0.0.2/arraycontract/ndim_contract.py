from collections import OrderedDict
from functools import wraps

from arraycontract.common import Trigger, __Closure


class NdimClosure(__Closure):
    def __call__(self, *args, **kwargs):
        bound_arguments: OrderedDict = self.func_signature.bind(*args, **kwargs).arguments
        for name, ndim in self.bound_constraints.items():
            assert bound_arguments[name].ndim == ndim, \
                f'Expect ndim of `{name}` is `{ndim}`, got `{bound_arguments[name].ndim}`'
        return self.func(*args, **kwargs)


def ndim(*constraints, **kwconstraints):
    def decorator(func):
        __enabled__ = kwconstraints.pop('__enabled__') if '__enabled__' in kwconstraints else True
        if not Trigger.ndim_check_trigger or not __enabled__:
            return func
        return wraps(func)(NdimClosure(func, constraints, kwconstraints))
    return decorator

