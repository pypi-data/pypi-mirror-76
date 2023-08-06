"""
This file contain wraps function that will check the input of the general function.
will raise exceptions if the input is not valid.
This file is using the generic check input class 'CheckInput' that contains all the
input validation to all the functions

Created by: Nir Barazida
Good luck
"""

from functools import wraps
from .check_input import CheckInput

def missing_values_checker(func):
    """
    Wrapper function to validate the input for method 'missing_values'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database):
        CheckInput.check_database_input(database)
        func(database)
    return wrapper_checker