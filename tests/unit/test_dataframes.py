# test_dataframes.py


import scrape


def test_list_to_dataframe():
    """ Test list_to_dataframe

    Function tested:
    list_to_dataframe

    """
    alist = [1, 2, 3]
    columns = ['Col1']
    df = scrape.utils.dataframes.list_to_dataframe(alist, columns)

    # Column
    df_columns = df.columns.to_list()
    assert columns == df_columns

    # Values
    df_series = df[columns[0]]
    df_values = df_series.to_list()
    assert alist == df_values
