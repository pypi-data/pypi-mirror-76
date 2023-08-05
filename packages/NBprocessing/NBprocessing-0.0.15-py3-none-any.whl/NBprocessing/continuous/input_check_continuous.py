import pandas as pd
from functools import wraps
from pandas.api.types import is_datetime64_any_dtype as is_datetime


def fill_na_timedate_checker(func):
    """
    Wrapper function to validate the input for method 'fill_na_timedate'
    Will raise Exception if input incorrect or data type not date time.
    """

    @wraps(func)
    def wrapper_checker(database, column_name):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(column_name) != str and type(column_name) != int and type(column_name) != float:
            raise ValueError("column_name input is not valid - Please enter a string")
        elif not is_datetime(database[column_name]):
            raise ValueError(f"The column {column_name} is not date-time type.")  # todo: MUST check this!!!
        elif column_name not in database.columns:
            raise KeyError("column_name not in database - please enter column that exists in database")
        return func(database, column_name)

    return wrapper_checker


def remove_outliers_by_boundaries_checker(func):
    """
    Wrapper function to validate the input for method 'remove_outliers_by_boundaries'
    Will raise Exception if input incorrect or data type not date time.
    """

    @wraps(func)
    def wrapper_checker(database, column_name, bot_qu, top_qu):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(column_name) != str and type(column_name) != int and type(column_name) != float:
            raise ValueError("column_name input is not valid - Please enter a string")
        elif (type(bot_qu) != float and type(bot_qu) != int) or bot_qu > 1 or bot_qu < 0:
            raise ValueError("bot_qu input is not valid - Please enter a float in range 0-1")
        elif (type(top_qu) != float and type(top_qu) != int) or top_qu > 1 or top_qu < 0:
            raise ValueError("top_qu input is not valid - Please enter a float in range 0-1")
        elif column_name not in database.columns:
            raise KeyError("column_name not in database - please enter column that exists in database")
        return func(database, column_name, bot_qu, top_qu)

    return wrapper_checker


def remove_and_get_num_outliers_by_value_checker(func):
    """
    Wrapper function to validate the input for methods 'get_num_outliers_by_value' and 'remove_outliers_by_value'
    Will raise Exception if input incorrect or data type not date time.
    """

    @wraps(func)
    def wrapper_checker(database, filter_dict_up=None, filter_dict_down=None):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        elif type(filter_dict_up) != dict:
            raise ValueError("filter_dict_up input is not valid - Please enter a dictionary")
        elif type(filter_dict_down) != dict:
            raise ValueError("filter_dict_down input is not valid - Please enter a dictionary")
        return func(database, filter_dict_up, filter_dict_down)

    return wrapper_checker