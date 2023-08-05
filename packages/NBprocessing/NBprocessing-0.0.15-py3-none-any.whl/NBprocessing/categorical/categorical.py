from .input_check_categorical import remove_categories_checker, fill_na_by_ratio_checker, combine_categories_checker, \
    categories_not_in_common_checker
import pandas as pd
import numpy as np


@remove_categories_checker
def remove_categories(database, column_name, categories_to_drop):
    """
    General Information
    ----------
    Remove all indexes in the database that contain the categories from the categories_to_drop.
    Before removing the indexes will print a message to the user with the number of indexes that
    will be remove and the percent of the database that will be lost.
    the user will input 'y'(yes) to pressed and 'n'(no) to cancel the action.
    If the user choose 'yes' the method will continue to drop the indexes and will
    plot the new database shape.

    Parameters
    ----------
    :param database: pandas Data Frame
    the database must contain the column that was sent to the method 'column_name'

    :param column_name: string
    The name of the column where the values ​​are and from which we will be parsing the categories.
    the column_name must be identical to the column name in the database.
    This column must be a categorical column.

    :param categories_to_drop: list or tuple of string int of float
    The name of the categories the user wish to drop.

    Returns
    -------
    None
    This method prints information to help the user decide rather to drop the categories or not.
    eventually returns None

    Raises
    ------
    ValueError : If input value not as mentioned above.

    Exemples
    -------
    Will be added in version 0.2
    """

    remove_df = database[database[column_name].isin(categories_to_drop)]

    user_input = input(f'Using remove_categories will result in deletion of {len(remove_df)}\n'
                       f'Which is {round(len(remove_df) * 100 / len(database), 2)} % of the database.\n'
                       f'Do you wish to continue? [y/n]')

    while user_input != 'y' and user_input != 'n':
        user_input = input(f'Using remove_categories will result in deletion of {len(remove_df)}\n'
                           f'Which is {round(len(remove_df) * 100 / len(database), 2)}% of the database.\n'
                           f'Do you wish to continue? please enter y for yes and n for no')
    if user_input == 'y':
        for value in categories_to_drop:
            database.drop(database.loc[database[column_name] == value].index, inplace=True)
        print(f"the new database shape is{database.shape}")


@fill_na_by_ratio_checker
def fill_na_by_ratio(database, column_name):
    """
    General Information
    ----------
    Fill all missing values in the given column by the ratio of the categories in the column.
    Because the ratio sum is not a perfect one - the extra missing values will
    be filled with the most common category in the column.

    Parameters
    ----------
    :param database: pandas Data Frame
    the database must contain the column that was sent to the method 'column_name'

    :param column_name:  string
    The name of the column where method will fill the missing values in.
    This column must be a categorical column

    Returns
    -------
    None
    fill the missing values in the column inplace.

    Raises
    ------
    ValueError : If input value not as mentioned above.

    Exemples
    -------
    Will be added in version 0.2
    """

    categories_names = list(database[column_name].value_counts(normalize=True, dropna=True).index)
    categories_ratio = list(database[column_name].value_counts(normalize=True, dropna=True).values)

    database[column_name] = database[column_name].fillna(
        pd.Series(np.random.choice(categories_names, p=categories_ratio, size=len(database))))

    # Fill the extra missing values
    database[column_name].fillna(database[column_name].value_counts().index[0], inplace=True)


@combine_categories_checker
def combine_categories(database, column_name, category_name="other", threshold=0.01):
    """
    General Information
    ----------
    Receives a threshold that is the minimum relative part of the category within the column.
    all categories that are less than this threshold will be combined under the same category
    under the name 'category_name'.
    the method will return a list with all the name of categories that were combined under 'category_name'
    with this list the user will be able to make the same action on the test set (assuming that the data
    was already splitted to train and test sets)

    Parameters
    ----------
    :param database: pandas Data Frame
    the database must contain the column that was sent to the method 'column_name'

    :param column_name: string
    The name of the column where method will fill the missing values in.
    This column must be a categorical column

    :param category_name: string
     The name of the new category of the combined categories

    :param threshold: float - 0 < threshold_percentage < 1
    Threshold that represent the ratio value the categories under it will be combined

    Returns
    -------
    the method will return a list with all the name of categories that were combined under 'category_name'
    with this list the user will be able to make the same action on the test set (assuming that the data
    was already splitted to train and test sets)

    for exemple: (LIST - the returned list from the function)
    X_test["column_name"].replace(LIST, category_name, inplace=True)

    Raises
    ------
    ValueError : If input value not as mentioned above.

    Exemples
    -------
    Will be added in version 0.2

    """

    values_to_combine = database[column_name].value_counts()[
        database[column_name].value_counts(normalize=True) < threshold].index
    database[column_name].replace(values_to_combine, category_name, inplace=True)
    return values_to_combine


@categories_not_in_common_checker
def categories_not_in_common(train, test, column_name):
    """
    General Information
    ----------
    To avoid different shapes of train and test data sets after creating dummies, the user is able to
    check if one categories is missing in the data sets.
    It will check all categories name of the two data sets and returns the name of the categories not
    in common for every data set.
    The information from this method will be returned as list of tuples:
        [(exists only in the first data set),(exists only in the second data set)]
    will also print every list as a message to the user.

    Parameters
    ----------
    :param train: pandas Data Frame
    First data set to check columns names from

    :param test: pandas Data Frame
    Second data set to check columns names from

    :param column_name: string
    The name of the column to preform the check.
    This column must be a categorical column

    :return:
    The information from this method will be returned as list of tuples:
        [(exists only in the first data set),(exists only in the second data set)]

    Raises
    ------
    ValueError : If input value not as mentioned above.

    Exemples
    -------
    Will be added in version 0.2
    """
    in_test = set(test[column_name]) - set(train[column_name])
    in_train = set(train[column_name]) - set(test[column_name])
    print(f"values existing only in the first data set {in_test}")
    print(f"values existing only in the second data set {in_train}")


if __name__ == '__main__':
    data = pd.read_csv('dataset_cars.csv')

    # remove_categories
    # print(len(data[data['year'] == 2019]))
    # remove_categories(data, 'year', [2019])
    # print(len(data[data['year'] == 2019]))

    # fill_na_by_ratio
    fill_na_by_ratio(data, 'fuel')

    # combine_categories
    print(combine_categories(data, 'fuel', category_name="Nir", threshold=0.01))
