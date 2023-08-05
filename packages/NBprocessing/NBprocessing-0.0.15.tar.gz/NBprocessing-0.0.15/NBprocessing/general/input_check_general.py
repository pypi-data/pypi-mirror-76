import pandas as pd
from functools import wraps

def missing_values_checker(func):
    """
    Wrapper function to validate the input for method 'missing_values'
    Will raise Exception if input incorrect
    """

    @wraps(func)
    def wrapper_checker(database):
        if type(database) != pd.core.frame.DataFrame:
            raise ValueError("Database input is not valid - Please enter pandas dataframe")
        func(database)
    return wrapper_checker