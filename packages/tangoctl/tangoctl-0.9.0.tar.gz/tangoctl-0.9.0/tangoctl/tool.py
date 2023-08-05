# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018-2020 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

import time
import functools


def timed_lru_cache(seconds: int, maxsize: int = 128, typed: bool = False):
    def _wrapper(func):
        func = functools.lru_cache(maxsize=maxsize, typed=False)(func)
        func._created = time.monotonic()
        func._expired = lambda: time.monotonic() >= (func._created + seconds)

        @functools.wraps(func)
        def _wrapped(*args, **kwargs):
            if func._expired():
                func.cache_clear()
                func._created = time.monotonic()
            return func(*args, **kwargs)

        _wrapped.cache_info = func.cache_info
        _wrapped.cache_clear = func.cache_clear
        return _wrapped

    return _wrapper


def test_timed_lru_cache():
    count = 0

    @timed_lru_cache(seconds=0.1)
    def test(arg1):
        nonlocal count
        count += 1
        return count

    assert test(1) == 1, "Function should be called the first time we invoke it"
    assert test(1) == 1, "Function should not be called because it is already cached"

    # Let's now wait for the cache to expire
    time.sleep(0.1)

    assert test(1) == 2, "Function should be called because the cache already expired"
