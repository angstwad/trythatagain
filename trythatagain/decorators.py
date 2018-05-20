# -*- coding: utf-8 -*-
from functools import partial, wraps

from .exc import CaughtException
from .waiters import exp_backoff, linear_backoff

SECONDS = 1
MILLISECONDS = .1

NoneType = type(None)


def retry(func=None, self=None, retries=3, raise_for=None, reraise=True,
          wait_func=None, unit=MILLISECONDS):
    """
    Retry decorator.  Wraps a function or method and retries a function or
    method until max_retries is hit, an ignored exception is raised, or it
    function completes without raising an exception.

    :param func: decorated function
    :param self: instance, if applicable
    :param retries: int number of times to retry decorated function. If 0,
        retry forever.
    :param raise_for: list or single exception class, if encountered, retries
        will not be attempted
    :param reraise: bool if True, re-raise last caught exception
    :param wait_func: function to implement some waiter logic
    :param unit: unit of measure to use when calculating wait time between
        retries; requires `wait_func`

    """
    local = {
        "tries": 0,
        "exc": None
    }

    if raise_for is None:
        raise_for = NoneType

    if func is None:
        return partial(retry, self=self, retries=retries, raise_for=raise_for,
                       unit=unit, reraise=reraise, wait_func=wait_func)

    @wraps(func)
    def wrapped(*args, **kwargs):
        while local['tries'] < retries or retries == 0:
            local['tries'] += 1
            try:
                if self is not None:
                    return func(self, *args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                local['exc'] = e

                try:
                    if isinstance(e, raise_for):
                        raise e
                except TypeError:
                    raise TypeError(
                        "'ignore' kwarg must be a class, type, or tuple of "
                        "classes and types"
                    )

                if wait_func:
                    wait_func(local['tries'], unit)

        if reraise and local['exc']:
            raise CaughtException('Caught exception from decorated function',
                                  local['exc'])

    return wrapped


retry_linear_backoff = partial(retry, wait_func=linear_backoff)
retry_exp_backoff = partial(retry, wait_func=exp_backoff)
