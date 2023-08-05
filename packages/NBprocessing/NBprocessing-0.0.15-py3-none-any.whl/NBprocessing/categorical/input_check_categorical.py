import pandas as pd
from functools import wraps


def remove_categories_checker(func):
    """
    Wrapper function to validate the input for method 'remove_categories'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_name, categories_to_drop):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(column_name) != str and type(column_name) != int and type(column_name) != float:
            raise ValueError("column_name input is not valid - Please enter a string")
        elif type(categories_to_drop) != list and type(categories_to_drop) != tuple:
            raise ValueError("categories_to_drop must be a list or a tuple - please enter as list / tuple")
        elif column_name not in database.columns:
            raise KeyError("column_name not in database - please enter column that exists in database")
        func(database, column_name, categories_to_drop)

    return wrapper_checker


def fill_na_by_ratio_checker(func):
    """
    Wrapper function to validate the input for method 'fill_na_by_ratio'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_name):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(column_name) != str and type(column_name) != int and type(column_name) != float:
            raise ValueError("column_name input is not valid - Please enter a string")
        elif column_name not in database.columns:
            raise KeyError("column_name not in database - please enter column that exists in database")
        func(database, column_name)

    return wrapper_checker


def combine_categories_checker(func):
    """
    Wrapper function to validate the input for method 'combine_categories'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_name, category_name="other", threshold=0.01):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(column_name) != str and type(column_name) != int and type(column_name) != float:
            raise ValueError("column_name input is not valid - Please enter a string")
        elif type(category_name) != str and type(category_name) != int and type(category_name) != float:
            raise ValueError("category_name input is not valid - Please enter a string/int/float")
        elif (type(threshold) != float and type(threshold) != int) or threshold > 1 or threshold < 0:
            raise ValueError("category_name input is not valid - Please enter a float in range 0-1")
        elif column_name not in database.columns:
            raise KeyError("column_name not in database - please enter column that exists in database")
        return func(database, column_name, category_name, threshold)
    return wrapper_checker


def categories_not_in_common_checker(func):
    """
    Wrapper function to validate the input for method 'categories_not_in_common'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(train, test, column_name):
        if type(train) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        if type(test) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(column_name) != str and type(column_name) != int and type(column_name) != float:
            raise ValueError("column_name input is not valid - Please enter a string")
        elif column_name not in train.columns or column_name not in test.columns:
            raise KeyError("column_name not in databases - please enter column that exists in both databases")
        return func(train, test, column_name)

    return wrapper_checker

