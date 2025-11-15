"""Utilities for decorating command handlers with consistent input error messages."""
from functools import wraps
from typing import Callable, Dict


errors: Dict[str, Dict[str, str]] = {
    "ValueError": {
        "add_contact": "Give me name and phone please.",
        "change_phone": "Give me name and phone please.",
        "show_phones": "Invalid name format.",
    },
    "IndexError": {
        "add_contact": "Give me name and phone please.",
        "change_phone": "Give me name and phone please.",
        "show_phones": "Enter user name",
    },
    "KeyError": {
        "change_phone": "Contact not found.",
        "show_phones": "Contact not found."
    },
    "TypeError": {
        "add_contact": "Invalid argument types. Name and phone must be text.",
        "change_phone": "Invalid argument types. Name and phone must be text.",
        "show_phones": "Invalid argument type for name."
    }
}

def get_error_message (
        err: Exception,
        func: Callable,
        default_error: str
    ):
    """Return a user-friendly error message based on the exception type and function name."""
    exception_name = type(err).__name__
    func_name = func.__name__
    message = errors.get(exception_name, {}).get(func_name, "")
    error_message = err.args[0] if len(err.args) > 0 else ""
    return f"{message}\n{error_message}" if message else f"{default_error}\n{error_message}"

def input_error(func):
    """Decorator that handles common input errors and provides user-friendly messages."""
    @wraps(func)
    def inner(*args, **kwargs):
        default_error = "An error occurred. Please check your input and try again."
        try:
            return func(*args, **kwargs)
        except KeyError as err:
            return get_error_message(err, func, default_error)
        except ValueError as err:
            return get_error_message(err, func, default_error)
        except IndexError as err:
            return get_error_message(err, func, default_error)
        except TypeError as err:
            return get_error_message(err, func, default_error)
    return inner
