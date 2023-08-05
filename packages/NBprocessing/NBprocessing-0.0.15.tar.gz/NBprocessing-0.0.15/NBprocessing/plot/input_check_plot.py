import pandas as pd
from functools import wraps


def plot_missing_value_and_corr_heatmap_checker(func):
    """
    Wrapper function to validate the input for method 'plot_missing_value_heatmap'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        func(database)
    return wrapper_checker


def count_and_distribution_plot_checker(func):
    """
    Wrapper function to validate the input for method 'count_plot' and 'distribution_plot'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_list=None):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(column_list) != list and type(column_list) != tuple:
            raise ValueError("categories_to_drop must be a list or a tuple - please enter as list / tuple")
        for col in column_list:
            if col not in database.columns:
                raise KeyError("column_name not in database - please enter column that exists in database")
        func(database, column_list)
    return wrapper_checker