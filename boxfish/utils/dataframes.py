# dataframes.py

"""Dataframes is a module that contains functions for pandas dataframes

"""

import csv
import os

import pandas as pd

from boxfish.utils.strings import filename_append_date
from boxfish.utils.utils import create_folder_if_not_exist


def list_to_dataframe(alist: list, columns: list) -> pd.DataFrame:
    """Convert list to dataframe with single column

    df = list_to_dataframe(alist,columns)

    Args:
        alist (list): List of items
        columns (list): List with column name
    Returns:
        df (pandas.DataFrame): Dataframe with list as column

    Example:
        alist = [1, 2, 3]
        columns = ['Col1']
        df = list_to_dataframe(alist,columns)
        >>    Col1
        >>0      1
        >>1      2
        >>3      3
    """

    df = None
    if len(alist) > 0:
        df = pd.DataFrame(alist)
        df.columns = list(columns)
    return df


def save(
    df: pd.DataFrame,
    filename: str,
    date_format: str = "",
    overwrite: bool = False,
    quoting: int = csv.QUOTE_NONNUMERIC,
) -> str:
    """Save dataframe to csv file

    fullname = save(df, filename, date_format, overwrite, quoting)

    Args:
        df (pandas.DataFrame): Dataframe
        filename (str): Filename
        date_format (str): Date format in strftime formats
        overwrite (bool): Overwrite existing file if True else append
        quoting (int): CSV quoting constant
    Returns:
        fullname (str): Full filename including date

    Example:
        fullname = save(df, 'filename.txt', date_format='%Y%m%d', overwrite=True, quoting=csv.QUOTE_NONNUMERIC)
    """
    if (df is not None) and os.path.basename(filename):
        create_folder_if_not_exist(os.path.dirname(filename))
        fullname = filename_append_date(filename, date_format)

        if os.path.exists(fullname) and not overwrite:
            df.to_csv(fullname, mode="a", header=False, quoting=quoting)
        else:
            df.to_csv(fullname, mode="w", quoting=quoting)
    else:
        fullname = ""
    return fullname
