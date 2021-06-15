
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('mode.chained_assignment', None)


# function which is reading a file and converts it to pandas DataFrame
def read_file(file_name, sep=',', csv=True, excel=False):

    '''
    :param file_name: file name in this directory to read in csv format or in excel format
    :param sep: a separator, default is comma
    :param csv: in default (True) read the file from a csv file
    :param excel: in default (False) don't read the file from a excel file, if set to True, read the file from an excel format
    :return: read dataset as a pandas DataFrame
    '''

    # define class Read_Error for raising this as en Exception
    class Read_Error(Exception):
        pass

    try:
        # if both parameters csv and excel are equal to each other, raise an Read_Error Exception
        if csv == excel or excel == csv:
            raise Read_Error

        # if csv=True, read the file like from a csv file
        if csv:
            dataset = pd.read_csv(file_name, sep=sep)

        # if excel=True, read the file like from an excel file
        elif excel:
            dataset = pd.read_excel(file_name)

        return dataset

    except Read_Error:
        print('')
        print('!!! Both parameters csv and excel must not be same, one should be True, the other False !!!')



def change_col_names(dataset, change_columns=None):

    '''
    :param dataset: a dataset in pandas format
    :param change_columns: dictionary, key = actual column in dataset, its value is the name you wanna change that column's name into
    :return: modified dataset with changed column names
    '''

    # error when user writes column which does not appear in the dataset
    class Change_Columns_Error(Exception):
        pass

    # error when user tries to change those columns other than in a dictionary
    class Type_Dictionary(Exception):
        pass

    # if everything is in right format
    if (change_columns is not None) and (type(change_columns) == dict):

        # list of column names in dataset
        list_column_names = list(dataset.columns)
        # list of column names in dataset but in lower case
        list_column_names_lower = [column.lower() for column in list_column_names]

        # go through each key in change_columns dictionary where each key a the actual dataset's column name
        for key_change_column in list(change_columns.keys()):

            # if that column in lower case does appear in the dataset (list of dataset\'s columns but all in lower case)
            if key_change_column.lower() in list_column_names_lower:
                # give the position of the that lower case where that column appears in the list of dataset's columns all in lower case
                position = list_column_names_lower.index(key_change_column.lower())
                # modify the actual list of dataset's column names with the position and assign it to the key's value
                list_column_names[position] = change_columns[key_change_column]

            # if that column in lower case does NOT appear in the dataset (list of dataset\'s columns but all in lower case)
            # raise an Change_Columns_Error to inform the user that the column does not appear in the dataset
            elif key_change_column.lower() not in list_column_names:
                raise Change_Columns_Error('!!! Column --> ^' + key_change_column + '^ does not appear in the dataset !!!')


        # if all goes alright and without Change_Columns_Error set the dataset's column names to be the modified list of column names (column_name_modified --> a value pair in dict)
        dataset.columns = list_column_names

        return dataset

    # if the type of the change_columns is not a dictionary then raise Type_Dictionary error
    elif type(change_columns) != dict:
        raise Type_Dictionary('!!! Type for changing column names is not a dictionary !!!')



def drop_columns_rows(dataset, columns_drop=None, rows_from=None, rows_to=None, reset_index=True):

    '''
    :param dataset: a dataset in pandas format
    :param columns_drop: a list of column names in dataset you want to remove
    :param rows_from: an integer value from what index you want to remove  rows (if not defined and the range_to is, it is set to be the start, 0)
    :param rows_to: an integer value to what index you want to remove rows (if not defined and the range_from is, it is set to be the end, len(dataset) (n_rows))
    :param reset_index: True as default, when removing rows, you can choose if you wnt to reset the index or not (reset_index=False)
    :return: modified dataset with delete columns or rows or both
    '''

    # error when user types column to drop and it does not appear in the dataset
    class Drop_Columns_Error(Exception):
        pass

    # if the column_drop parameter is ont in list type raise this error
    class Type_List(Exception):
        pass

    # if rows_from parameter is larger than rows_to parameter raise this error
    class Row_Range_Error(Exception):
        pass

    # if at least one of rows_from adn rows_to parameters is defined as NOT integer raise this error
    class Type_Int(Exception):
        pass


    # here are the column names in list
    column_names = list(dataset.columns)

    # column names all in lower case
    column_names_lower = [column.lower() for column in column_names]
    # from here set all the column names in the dataset in lower case
    dataset.columns = column_names_lower

    # columns drop is not None and in list type
    if (columns_drop is not None) and (type(columns_drop) == list):

        # go through each column user wants to drop
        for column in columns_drop:

            # if that column appears in the dataset
            if column.lower() in column_names_lower:

                # give the position of the appearence of that column in lower case in list of dataset's column names all in lower case
                position = column_names_lower.index(column.lower())

                # remove in actual list of column names the column player wants to remove
                column_names.pop(position)
                # also remove this column in the list of column names all in lower case
                column_names_lower.pop(position)

                # drop the actual column which is in lower case for now
                dataset.drop([column.lower()], axis=1, inplace=True)

            # if does not appear raise Drop_Columns_Error
            elif column.lower() not in column_names_lower:
                raise Drop_Columns_Error('!!! Column: ^' + column + '^ does not appear in the dataset !!!')

        # after that set the column names to be how they were before maing themn lower case
        dataset.columns = column_names

    # if column_drop is not in list type raise an Type_list error
    elif type(columns_drop) != list:
        raise Type_List('!!! Type for columns_drop parameter is not a list !!!')


    # if at least one of them is defined
    if (rows_from is not None) or (rows_to is not None):

        # if rows_from is not defined set it as the starting point, 0
        if rows_from is None:
            rows_from = 0

        # else if rows_to is not defined set it to be the end of the dataset the n_rows in the dataset
        elif rows_to is None:
            rows_to = len(dataset)


        # all of them are in integer type
        if (type(rows_from) == int) and (type(rows_to) == int):

            # if rows_from is larger than rows_to raise Row_Range_Error
            if rows_from >= rows_to:
                raise Row_Range_Error('!!! rows_from must be fewer than rows_to !!!')

            # drop the range of rows which are indexed from 0 to n_rows
            dataset.drop(dataset.index[rows_from:rows_to], inplace=True)

            # if reset_index is defined as True (default) reset the index
            if reset_index:
                dataset.reset_index(drop=True, inplace=True)


        # if one of them is not in integer type raise Type_Int error
        elif (type(rows_from) != int) or (type(rows_to) != int):
            raise Type_Int('!!! Type for rows_from and for rows_to should be integer !!!')


    return dataset



def drop_replace_na(dataset, other_than_na=None, replace_na_with=None):

    '''
    :param dataset: dataset passed which user wants to drop or replace NaN values in
    :param other_than_na: if there are values indexed other than np.nan type a list of those values and replace them with np.nan
    :param replace_na_with: if None (default) NaN won't be replaced with anything, they will be removed from the dataset, if is not None, NaN will be replaced with value you pass in
    :return: modified dataset
    '''

    # if user types other_than_na parameter in different format than list raise this error
    class Type_List(Exception):
        pass

    # if something went wrong with replacing NaN values with something which was specified in replace_na_with parameter
    class Replace_Value(Exception):
        pass


    # if other_than_na is not None and it is a list
    if (other_than_na is not None) and (type(other_than_na) == list):

        # go through each element in that list and replace that value in dataset with np.nan
        for other_than_na_value in other_than_na:
            dataset.replace(other_than_na_value, np.nan, inplace=True)

    # if other_than_na is not None and it is NOT a list raise Type_List error
    elif (other_than_na is not None) and (type(other_than_na) != list):
        raise Type_List('!!! Type for other_than_na must be a list !!!')

    # if not defined let it pass (default)
    elif other_than_na is None:
        pass


    # if set as default, when replace_na_with is None, drop all rows which have NaN values in them and reset the index
    if replace_na_with is None:
        dataset.dropna(inplace=True)
        dataset.reset_index(drop=True, inplace=True)

    # if replace_na_with is not None
    elif replace_na_with is not None:

        try:
            # replace those NaN values with something what is specified in replace_na_with parameter, if something goes wrong raise Replace_Value error
            dataset.replace(np.nan, replace_na_with, inplace=True)
        except:
            raise Replace_Value('!!! Something went wrong with replacing NaN values with your ' + str(replace_na_with) + ' value(s), must be a single value !!!')


    return dataset



def change_number_format(dataset, column_names=None):

    '''
    :param dataset: dataset user wants to modify
    :param column_names: column names which are in dataset, must be written in list type
    :return: modified dataset
    '''


    # when column specified in column_names parameter does not appear in the dataset raise this Error
    class Column_Not_Present(Exception):
        pass

    # when column_names parameter is not None but it's not specified as a list raise this Error
    class Type_List(Exception):
        pass


    # if column_names is not None and is in right format, a list
    if (column_names is not None) and (type(column_names) == list):

        # actual column names stored here
        actual_column_names = list(dataset.columns)

        # column names but all in lower case
        lower_case_columns = [column.lower() for column in actual_column_names]
        # temporarily set all column names into lower case
        dataset.columns = lower_case_columns


        # Check for any exceptions
        try:
            # go through each column name in column_names
            for column_name in column_names:

                # if there is typed 'all' in column_names list and that list has only this element, this means that we go through every column in dataset
                if (column_name.lower() == 'all') and (len(column_names) == 1):

                    # before making any changing we must convert a whole dataset into string because we are going to use regex to modify it and that's for strings
                    dataset = dataset.astype(str)

                    for dataset_column_name in list(dataset.columns):

                        # make a copy of this dataset which is not modified yet
                        dataset_copy = dataset.copy()

                        # '^[0-9]+,[0-9]+$' --> regex format, ^ means the start $ means the end, we don't use ^, because there could be a negative value which starts with -
                        # [0-9] means any number from 0 to 9, can be a string also which is from 0 to 9
                        # + mean one or more occurences if those nums
                        # '^[0-9]+,[0-9]+$' --> number which has some one or more numbers at the start before the comma (,), then comma(,), a after the comma one or more numbers which also ends with some number
                        # regex --> will apply this regex formatting in pandas --> regex=True
                        mask = dataset[dataset_column_name.lower()].str.contains('[0-9]+,[0-9]+$', regex=True)

                        # so now we select an series with the column which has this format (instead 1.5 it has 1,5)
                        # an then replace this comma ',' with a dot '.'
                        replace = dataset.loc[mask, dataset_column_name.lower()].str.replace(',', '.')

                        # and then make those changes count that it will set those changed values into that column in the dataset,
                        # but the values which are right, which doesn't have 1,5, which actually have 1.5 (a dot), they will be converted into NaN values
                        dataset[dataset_column_name.lower()] = replace

                        # now to combine that data, because we have converted the right values int NaN values, so now all the NaN in the changed dataset will be filled with the right values which are in the copied dataset
                        dataset = dataset.combine_first(dataset_copy)

                    # after all changes convert that dataframe into floats
                    dataset = dataset.astype(float)


                else:

                    # if that column name does not appear in the dataset raise Column_Not_Present error
                    if column_name.lower() not in lower_case_columns:
                        raise Column_Not_Present('!!! Column --> ^' + column_name + '^ does not appear in the dataset !!!')


                    # before making any changing we must convert a column into string because we are going to use regex to modify it and that's for strings
                    dataset[column_name.lower()] = dataset[column_name.lower()].astype(str)

                    # make a copy of this dataset which is not modified yet
                    dataset_copy = dataset.copy()

                    # '^[0-9]+,[0-9]+$' --> regex format, ^ means the start $ means the end, we don't use ^, because there could be a negative value which starts with -
                    # [0-9] means any number from 0 to 9, can be a string also which is from 0 to 9
                    # + mean one or more occurences if those nums
                    # '^[0-9]+,[0-9]+$' --> number which has some one or more numbers at the start before the comma (,), then comma(,), a after the comma one or more numbers which also ends with some number
                    # regex --> will apply this regex formatting in pandas --> regex=True
                    mask = dataset[column_name.lower()].str.contains('[0-9]+,[0-9]+$', regex=True)

                    # so now we select an series with the column which has this format (instead 1.5 it has 1,5)
                    # an then replace this comma ',' with a dot '.'
                    replace = dataset.loc[mask, column_name.lower()].str.replace(',', '.')

                    # and then make those changes count that it will set those changed values into that column in the dataset,
                    # but the values which are right, which doesn't have 1,5, which actually have 1.5 (a dot), they will be converted into NaN values
                    dataset[column_name.lower()] = replace

                    # now to combine that data, because we have converted the right values int NaN values, so now all the NaN in the changed dataset will be filled with the right values which are in the copied dataset
                    dataset = dataset.combine_first(dataset_copy)

                    # after all changes convert that column into floats
                    dataset[column_name.lower()] = dataset[column_name.lower()].astype(float)


            # set dataset's column names to be the actual column names
            dataset.columns = actual_column_names

            return dataset

        except Exception:
            raise Exception('!!! Oops, something went wrong with changing numbers format !!!')


    elif (column_names is not None) and (type(column_names) != list):
        raise Type_List('!!! Type for column_names parameter must be a list !!!')



def handle_non_numeric(dataset, column_names=None):

    '''
    :param dataset: dataset to be modified
    :param column_names: column names user wants to encode, categorize data in, f.e. True/False --> 1/0
    :return: modified dataset
    '''

    # when column does not appear in the dataset raise this error
    class Column_Not_Present(Exception):
        pass

    # if column_names parameter is not a list raise this error
    class Type_List(Exception):
        pass

    # actual column names
    dataset_columns = list(dataset.columns)

    # column names but in lower case
    dataset_columns_lower = [column.lower() for column in dataset_columns]
    # temporarily set al column names in dataset to be lower case
    dataset.columns = dataset_columns_lower

    # if that column_names is not None and in list type
    if (column_names is not None) and (type(column_names) == list):

        # go through each element in column_names
        for column_name in column_names:

            # if that column does not appear in the dataset raise Column_Not_Present error
            if column_name.lower() not in dataset_columns_lower:
                raise Column_Not_Present('!!! Column --> ^' + column_name + '^ does not appear in the dataset !!!')

            print('')

            # unique values of that column in a list
            unique_values = list(dataset[column_name.lower()].unique())

            # go in enumerate where it takes the index of the unique value in that list nd that exact unique value
            for index, unique_value in enumerate(unique_values):
                # also print info how it encoded the column
                print(unique_value, '-->', index)
                # replace that unique value for that index, for its unique number
                dataset.replace(unique_value, index, inplace=True)

        print('')

        # set the actual column names into dataset
        dataset.columns = dataset_columns

        return dataset

    # if that columns_names is not None BUT is not in list type raise Type_List error
    elif (column_names is not None) and (type(column_names) != list):
        raise Type_List('!!! Type for column_names parameter must be a list !!!')



def balance(dataset, balance_by=None):

    '''
    :param dataset: dataset for balancing
    :param balance_by: a column name which user wants to make balancing with
    :return: balanced dataset
    '''

    # when column does not appear in the dataset raise this error
    class Column_Not_Present(Exception):
        pass


    # actual column names
    column_names = list(dataset.columns)

    # column names but all in lower case
    column_names_lower = [column.lower() for column in column_names]
    # set to the dataset column names all in lower case
    dataset.columns = column_names_lower


    # if balance_by is not None and does occur in the dataset
    if (balance_by is not None) and (balance_by.lower() in column_names_lower):

        # print the changed/or_not dataframe with the same counts for each category
        print('')
        print('Amount for each category in balance_by column BEFORE BALANCING')
        print(dataset[balance_by.lower()].value_counts())
        print('')

        # a dictionary of counts of balance_by column, each category has it's count
        dict_counts = dict(dataset[balance_by.lower()].value_counts())

        # the min value a unique categories has in balance_by column
        min_balance_by_count = min(np.array(dataset[balance_by.lower()].value_counts()))
        # the sum of counts of unique categories in balance_by column
        sum_balance_by_count = np.sum(np.array(dataset[balance_by.lower()].value_counts()))

        # go through each category and its count
        for category, its_count in dict_counts.items():
            # mask where dataset has those unique values in that balance_by column
            mask = (dataset[balance_by.lower()] == category)

            # make a temporary dataset where the dataset is only with those values, of that unique category
            df_temp = dataset.loc[mask]
            # also reset the index of that dataframe
            df_temp.reset_index(drop=True, inplace=True)

            # if its count is equal to the min count between all unique values let it pass, other wise
            if its_count == min_balance_by_count:
                pass

            else:
                # drop the range of rows from the min_balance_by_count to the its count
                df_temp.drop(range(min_balance_by_count, its_count), inplace=True)

            # add that temporary dataframe into that unique dataset
            dataset = dataset.append(df_temp, ignore_index=True)

        # also at the end we must drop all the rows from the start and to the end where it was first time before making balancing,
        # so delete all rows from 0 to the sum of counts of all unique values
        dataset.drop(range(sum_balance_by_count), inplace=True)
        # also reset the index of that dataset
        dataset.reset_index(drop=True, inplace=True)

        # print the changed dataframe with the same counts for each category
        print('')
        print('Amount for each category in balance_by column AFTER BALANCING')
        print(dataset[balance_by.lower()].value_counts())
        print('')

        # set the actual column names into the dataset
        dataset.columns = column_names

        return dataset

    # if that balance_by column does not occur in the dataset raise Column_Not_Present error
    elif (balance_by is not None) and (balance_by.lower() not in column_names_lower):
        raise Column_Not_Present('!!! Column --> ^' + balance_by + '^ does not appear in the dataset !!!')
