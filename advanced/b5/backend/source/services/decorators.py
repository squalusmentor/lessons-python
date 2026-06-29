import functools
from typing import Callable
from loguru import logger
from fastapi import HTTPException


# Декоратор для обычной функции
def handle_errors(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок в обычных функциях
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(e)
            return False
    return wrapper


# Декоратор для метода класса
def handle_errors_method(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок в методах класса
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(e)
            return False
    return wrapper


# Декоратор для асинхронной функции
def handle_errors_async(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок в асинхронных функциях
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(e)
            return False
    return wrapper


# Декоратор для асинхронного метода класса
def handle_errors_async_method(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок в асинхронных методах класса
    """
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(e)
            return False
    return wrapper
