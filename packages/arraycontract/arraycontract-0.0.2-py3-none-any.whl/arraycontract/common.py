import inspect


class Trigger:
    dtype_check_trigger: bool = __debug__
    ndim_check_trigger: bool = __debug__
    shape_check_trigger: bool = __debug__


class __Closure:
    def __init__(self, func, constraints, kwconstraints):
        self.func = func
        self.func_signature: inspect.Signature = inspect.signature(func)
        self.bound_constraints = self.func_signature.bind_partial(*constraints, **kwconstraints).arguments

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()
