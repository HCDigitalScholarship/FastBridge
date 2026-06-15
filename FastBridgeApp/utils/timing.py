"""
Timing utilities for performance measurement
"""
import time
from functools import wraps
import asyncio


def timer_decorator(runs=10):
    """
    Decorator to measure execution time of both sync and async functions.
    Runs functions multiple times and prints average.

    Args:
        runs: Number of times to run the function for averaging (default: 10)

    Usage:
        @timer_decorator()  # Default: 10 runs
        async def my_async_function():
            ...

        @timer_decorator(runs=5)  # Custom: 5 runs
        def my_sync_function():
            ...

        @timer_decorator(runs=1)  # Single run, no averaging
        async def production_endpoint():
            ...
    """
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                results = []
                for _ in range(runs):
                    start_time = time.time()
                    result = await func(*args, **kwargs)
                    elapsed_time = time.time() - start_time
                    results.append(elapsed_time)
                    print(f"{func.__name__} took {elapsed_time:.4f} seconds")

                if runs > 1:
                    print(f"Avg time over {runs} runs = {sum(results)/len(results):.4f} seconds")

                return result
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                results = []
                for _ in range(runs):
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    elapsed_time = time.time() - start_time
                    results.append(elapsed_time)
                    print(f"{func.__name__} took {elapsed_time:.4f} seconds")

                if runs > 1:
                    print(f"Avg time over {runs} runs = {sum(results)/len(results):.4f} seconds")

                return result
            return sync_wrapper

    return decorator
