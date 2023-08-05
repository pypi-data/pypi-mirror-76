"""
This file contain wraps function that will check the input of the plot function.
will raise exceptions if the input is not valid.
This file is using the generic check input class 'CheckInput' that contains all the
input validation to all the functions

Created by: Nir Barazida
Good luck
"""

from functools import wraps
from ._check_input import CheckInput


def plot_missing_value_and_corr_heatmap_checker(func):
    """
    Wrapper function to validate the input for method 'plot_missing_value_heatmap'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database):
        CheckInput.check_database_input(database)
        func(database)
    return wrapper_checker


def count_and_distribution_plot_checker(func):
    """
    Wrapper function to validate the input for method 'count_plot' and 'distribution_plot'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database, column_list=None):
        CheckInput.check_database_input(database)
        CheckInput.check_categories_to_drop(column_list)
        for column in column_list:
            CheckInput.check_column_in_database(column, database)
        func(database, column_list)
    return wrapper_checker