from functools import wraps
import time

def timer(func):
    """
    Measure and print function execution time.
    
    Usage:
        @timer
        def slow_function():
            time.sleep(1)
    
    Output: "slow_function took 1.0023 seconds"
    """
    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return result
    return timer_wrapper

def logger(func):
    """
    Log function calls with arguments and return value.
    
    Usage:
        @logger
        def add(a, b):
            return a + b
        
        add(2, 3)
    
    Output:
        "Calling add(2, 3)"
        "add returned 5"
    """
    @wraps(func)
    def logger_wrapper(*args, **kwargs):
        args_list = [repr(a) for a in args] # repr is used to give full obj identity
        kwarg = [f"{k}={v!r}" for k, v in kwargs] # !r is another way of saying repr(v)
        all_args = ",".join(args_list, kwargs)
        
        print(f"Calling {func.__name__} ({all_args})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return logger_wrapper

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Retry a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Seconds to wait between retries
        exceptions: Tuple of exceptions to catch
    
    Usage:
        @retry(max_attempts=3, delay=0.5)
        def flaky_api_call():
            # might fail sometimes
            pass
    """
    def retry_decorator(func):
        @wraps(func)
        def retry_wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise exceptions
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(delay)
        return retry_wrapper
    return retry_decorator

def cache(max_size=128):
    """
    Cache function results.
    Similar to lru_cache but with visible cache inspection.
    
    Usage:
        @cache(max_size=100)
        def expensive_computation(x):
            return x ** 2
        
        expensive_computation(5)  # Computes
        expensive_computation(5)  # Returns cached
        
        # Inspect cache
        expensive_computation.cache_info()
        expensive_computation.cache_clear()
    """
    def cache_decorator(func):
        cache = {}
        @wraps(func)
        def cache_wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            if key in cache:
                return cache[key]
            
            result = func(*args,**kwargs)
            if len(cache) >= max_size:
                cache.pop(next(iter(cache)))
            
            cache[key] = result
            return result
        
        
        def cache_info():
            return {
                "size": len(cache),
                "max_size": max_size,
                "keys": list(cache.keys())
            }

        def cache_clear():
            cache.clear()

        cache_wrapper.cache_info = cache_info
        cache_wrapper.cache_clear = cache_clear
        
        return cache_wrapper
    return cache_decorator
