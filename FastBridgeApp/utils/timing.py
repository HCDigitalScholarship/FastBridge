"""
Timing utilities for performance measurement
"""
import time
from functools import wraps
import asyncio


def timer_decorator(func):
    """
    Decorator to measure execution time of both sync and async functions.
    Prints the execution time to console.

    Usage:
        @timer_decorator
        async def my_async_function():
            ...

        @timer_decorator
        def my_sync_function():
            ...
    """
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            print(f"{func.__name__} took {elapsed_time:.4f} seconds")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            print(f"{func.__name__} took {elapsed_time:.4f} seconds")
            return result
        return sync_wrapper


def timer_decorator_detailed(func):
    """
    Decorator that returns both the result and elapsed time.
    Useful when you need to access the timing data programmatically.

    Usage:
        @timer_decorator_detailed
        def my_function():
            ...

        result, elapsed = my_function()
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        return result, elapsed_time
    return wrapper
