
"""
This file contain wraps function that will check the input of the categorical function.
will raise exceptions if the input is not valid.
This file is using the generic check input class 'CheckInput' that contains all the
input validation to all the functions

Created by: Nir Barazida
Good luck
"""

from functools import wraps
from .check_input import CheckInput

def remove_categories_checker(func):
    """
    Wrapper function to validate the input for method 'remove_categories'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_name, categories_to_drop):
        CheckInput.check_database_input(database)
        CheckInput.check_column_name(column_name)
        CheckInput.check_column_in_database(column_name,database)
        CheckInput.check_categories_to_drop(categories_to_drop)
        func(database, column_name, categories_to_drop)

    return wrapper_checker


def fill_na_by_ratio_checker(func):
    """
    Wrapper function to validate the input for method 'fill_na_by_ratio'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_name):
        CheckInput.check_database_input(database)
        CheckInput.check_column_name(column_name)
        CheckInput.check_column_in_database(column_name, database)
        func(database, column_name)
    return wrapper_checker


def combine_categories_checker(func):
    """
    Wrapper function to validate the input for method 'combine_categories'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_name, category_name="other", threshold=0.01):
        CheckInput.check_database_input(database)
        CheckInput.check_column_name(column_name)
        CheckInput.check_column_name(category_name)
        CheckInput.check_column_in_database(column_name, database)
        CheckInput.check_threshold(threshold)
        return func(database, column_name, category_name, threshold)
    return wrapper_checker


def categories_not_in_common_checker(func):
    """
    Wrapper function to validate the input for method 'categories_not_in_common'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(train, test, column_name):
        CheckInput.check_database_input(train)
        CheckInput.check_database_input(test)
        CheckInput.check_column_name(column_name)
        CheckInput.check_column_in_database(column_name, train)
        CheckInput.check_column_in_database(column_name, test)
        return func(train, test, column_name)

    return wrapper_checker

# def category_ratio(database, columns_to_check=None, num_categories=5)
def category_ratio_checker(func):
    """
    Wrapper function to validate the input for method 'category_ratio'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, columns_to_check=None, num_categories=5):
        CheckInput.check_database_input(database)
        # CheckInput.check_categories_to_drop(columns_to_check) # todo: replace to a new check - list/tuple/None
        CheckInput.check_num_categories(num_categories)
        return func(database, columns_to_check, num_categories)

    return wrapper_checker