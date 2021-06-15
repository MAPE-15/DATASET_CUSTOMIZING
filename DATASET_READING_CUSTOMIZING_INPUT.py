
import pandas as pd
import numpy as np


# show all columns in the dataframe while printing it
pd.set_option('display.max_columns', None)
# to avoid a specific error, which is not important at all
pd.set_option('mode.chained_assignment', None)


# what_dataset --> the path of the file, or an exact file name
# separator --> by default = ','
# change_column_names --> by default = 'NO'

def read_change_columns(what_dataset, separator=',', change_column_names='NO'):

    # -------------------------------------------- READ/CHANGE_COL_NAMES -----------------------------------------------
    # EXCEPTION CHECK
    try:
        # engine = 'python' --> will ignore some errors that are accountable in pandas but not while using python, so it will ignore some pointless warnings
        df = pd.read_csv(what_dataset, sep=separator, engine='python')

        if change_column_names == 'YES':
            print('')
            print('THESE ARE YOUR COLUMNS NAMES:', list(df.columns))
            print('')

            # here you type the columns you wanna rename
            ask_which_columns_to_change = input('What columns in your dataset you wanna change? (split with comma + space): ').split(', ')
            # here you type what to rename them to, ORDER must be respected !!!
            change_columns_into = input('Type what you wanna change them into, order must be precise !!! (split with comma + space): ').split(', ')

            # this is the list of columns, yet unchanged
            list_columns = list(df.columns)

            # no loop through the columns you wanna change and column_name you want them to be named of
            for which_to_change, change_into in zip(ask_which_columns_to_change, change_columns_into):
                # the position/index where the current column names is in the list column
                position = list_columns.index(which_to_change)
                # change that column
                list_columns[position] = change_into

            # set the change list of columns to be the columns names for the dataset
            df.columns = list_columns

        # if don't wanna change the column do nothing
        elif change_column_names == 'NO':
            pass

        else:
            print('')
            print('Yes/No typed wrong in the input try all again (rerun the whole program) !!!')
            make_dataset()

        # return the modified/unmodified dataset
        return df

    # if there any error occurs, try again
    except Exception:
        print('')
        print('Oops something went wrong, try again (rerun the whole program) !!!')
        make_dataset()
    # ---------------------------------------- READ/CHANGE_COL_NAMES END -----------------------------------------------


# dataset --> takes the dataset, which was previously read, and modified (or not)
# modify --> by default = 'NO'
def clean_drop_sort(dataset_clean):

    print('')
    print(dataset_clean)

    # ----------------------------------------- DROP ROWS AND COLUMNS --------------------------------------------------
    # ask if user wants to drop some columns
    print('')
    ask_drop_column = input('Do you want drop some whole COLUMNS permanently from your dataset? Yes/No: ').upper()

    if ask_drop_column == 'YES':
        # print column names
        print('')
        print('THESE ARE YOUR COLUMNS NAMES:', list(dataset_clean.columns))
        print('')
        # give names of columns in the dataset
        drop_what_columns = input('Type names of column you want to drop (split with comma + space): ').split(', ')

        # Check for exceptions
        try:
            # drop those column which are in the list
            dataset_clean.drop(columns=drop_what_columns, axis=1, inplace=True)

            print('')
            print(dataset_clean)

        except Exception:
            print('')
            print('Oops something went wrong, probably you have typed column(s) which does not occur in the dataset, try again (rerun the whole program) !!!')
            make_dataset()


    elif ask_drop_column == 'NO':
        pass

    else:
        print('')
        print('Yes/No typed wrong, try again (rerun the whole program)!!!')
        make_dataset()


    # ask the user if wants to drop some rows
    print('')
    ask_drop_rows = input('Do you want drop some whole ROWS permanently from your dataset? Yes/No: ').upper()

    if ask_drop_rows == 'YES':
        # announce user that row indexing starts from 0
        print('')
        print('Your rows are indexed from 0 to the last row, row count starts from 0 !!!')
        # give the range of rows user wants to drop (format --> 5-10 --> removes rows indexed from 5 to 10)
        ask_drop_rows_range = input('OK, give me the range of indexes you want to delete (f.e., 5-10; 23-450;...) format is demonstrated in parentheses: ')

        # if there is no pomlcka in the given input range raise an error
        if '-' not in ask_drop_rows_range:
            print('')
            print('Oops wrong format, try again (rerun the whole program)!!!')
            make_dataset()

        # if there is more than one pomlcka in the given input range raise an error
        elif len([x for x in ask_drop_rows_range if x == '-']) != 1:
            print('')
            print('Oops wrong format, try again (rerun the whole program)!!!')
            make_dataset()

        # if no problem then, give the index position in the given input range of pomlcka
        else:
            pomlcka_position = ask_drop_rows_range.index('-')

        # check for any exceptions
        try:
            # range, 1st number is the start of the range so take all numbers from the input to pomlcka
            range_from = int(ask_drop_rows_range[:pomlcka_position])
            # 2ns number is the end of the range so take all number that start from pomlcka position + 1 to the end
            range_to = int(ask_drop_rows_range[pomlcka_position + 1:])

            # if number in that range which is the end of the range is smaller than the starting range number, raise an error
            if range_from >= range_to:
                raise Exception

            # drop all indexes/rows in that dataset with given range
            dataset_clean.drop(dataset_clean.index[range_from:range_to], inplace=True)
            # then reset the index
            dataset_clean.reset_index(drop=True, inplace=True)

            print('')
            print(dataset_clean)

        except Exception:
            print('')
            print('Oops wrong format, try again (rerun the whole program)!!!')
            make_dataset()

    elif ask_drop_rows == 'NO':
        pass

    else:
        print('')
        print('Yes/No typed wrong, try again (rerun the whole program)!!!')
        make_dataset()
    # ------------------------------------- DROP ROWS AND COLUMNS END --------------------------------------------------


    # ----------------------------------------- DROP/REPLACE NaN VALUES ------------------------------------------------
    print('')
    ask_modify_NaN = input('Do you want to clean this dataset before you use it? (dropping NaN etc...) Yes/No: ').upper()

    if ask_modify_NaN == 'YES':
        # ask if there is any other missing value indexed differently as NaN, f.e. == Missing, NA, Empty, ...
        ask_NaN = input('Do you have missing values indexed differently than NaN? Yes/No: ').upper()

        if ask_NaN == 'YES':
            print('')
            # type down how there are indexed differently those values
            ask_replace_NaN = input('If you don"t have NaN values indexed as missing values, then type how your missing values are indexed (Missing/NA/None/?/-200/...) (split with slash): ').split('/')
            print('Now all those values are replaced as NaN.')

            # go for each indexed values as NaN but differently
            for empty_val in ask_replace_NaN:

                # if there is found a numeric value in the input, try to replace it also with an integer, not only with string
                if empty_val[1:].isnumeric():
                    dataset_clean.replace(int(empty_val), np.nan, inplace=True)

                # replace them to NaN
                dataset_clean.replace(empty_val, np.nan, inplace=True)

        elif ask_NaN == 'NO':
            pass

        else:
            print('')
            print('Yes/No typed wrong in the input try all over again (rerun the whole program) !!!')
            make_dataset()


        # ask player if wants to drop those column permanently which have NaN values or replace with some integer number those NaN values
        print('')
        ask_drop_replace = input('Do you want to permanently delete rows which has NaN in them, or just want them to be replaced as outliers? Drop/Replace: ').upper()

        # if wants to remove
        if ask_drop_replace == 'DROP':
            print('OK, you decided to drop all rows which have NaN is them.')

            # drop all rows which has NaN in them, and reset the index
            dataset_clean.dropna(inplace=True)
            dataset_clean.reset_index(drop=True, inplace=True)

        # if wants to replace
        elif ask_drop_replace == 'REPLACE':

            try:
                # ask for the value he wants those NaNs to be replaced with
                ask_outlier = int(input('OK, so type a value which SHOULD be considered as an OUTLIER (f.e. -99 999...): '))
                # replace np.nan(NaN values) with the input
                dataset_clean.replace(np.nan, ask_outlier, inplace=True)

            except ValueError:
                print('')
                print('An outlier must be an integer, not a text or character or any decimal number, try all again!!!')
                clean_drop_sort(dataset_clean)

        else:
            print('')
            print('Drop/Replace typed wrong in the input try all over again (rerun the whole program) !!!')
            make_dataset()


    elif ask_modify_NaN == 'NO':
        pass

    else:
        print('')
        print('Yes/No typed wrong in the input try all again (rerun the whole program) !!!')
        clean_drop_sort(dataset_clean)
    # ------------------------------------- DROP/REPLACE NaN VALUES END ------------------------------------------------


    # ---------------------------------------- TAKE A LOOK AT THE DATASET ----------------------------------------------
    print()
    print('THIS IS HOW THE DATAFRAME LOOKS RIGHT NOW!!!')
    print('')
    print(dataset_clean)
    # ------------------------------------ TAKE A LOOK AT THE DATASET END ----------------------------------------------


    # ----------------------------- CHANGE NUMBERS FORMAT (FROM 1,5 TO 1.5) --------------------------------------------
    # ask the user if wants to make a format change from 1,5 to 1.5
    print('')
    ask_modify_numbers = input('''Do you want to modify columns which has numeric values but in different format? 
Specifically instead of 1.5 it has 1,5; instead of a dot (.) it has comma (,), and it is supposed to be a float number
Yes/No: ''').upper()

    if ask_modify_numbers == 'YES':
        # print the dataset how it look, and also the column names
        print('')
        print(dataset_clean)
        print('')
        print('THESE ARE YOUR COLUMNS NAMES:', list(dataset_clean.columns))
        print('')

        # ask the user for the specific column names he/she wants to modify numbers format in
        ask_modify_numbers_columns = input('OK, so specify column names which you want to change from format 1,5 into 1.5 (split with comma + space): ').split(', ')

        # CHECK FOR ANY EXCEPTIONS
        try:

            # for each column the player has input
            for col_name in ask_modify_numbers_columns:

                # if there does not occur this column in the dataset, raise an error
                if col_name not in list(dataset_clean.columns):
                    raise Exception

                # make a copy of the dataset which won't be modified, before the modification
                dataset_clean_copied = dataset_clean.copy()

                # '^[0-9]+,[0-9]+$' --> regex format, ^ means the start $ means the end
                # [0-9] means any number from 0 to 9, can be a string also which is from 0 to 9
                # + mean one or more occurences if those nums
                # '^[0-9]+,[0-9]+$' --> number which has some one or more numbers at the start before the comma (,), then comma(,), a after the comma one or more numbers which also ends with some number
                # regex --> will apply this regex formatting in pandas --> regex=True
                mask = dataset_clean[col_name].str.contains('^[0-9]+,[0-9]+$', regex=True)

                # so now we select an series with the column which has this format (instead 1.5 it has 1,5)
                # an then replace this comma ',' with a dot '.'
                replace = dataset_clean.loc[mask, col_name].str.replace(',', '.')
                # and then make those changes count that it will set those changed values into that column in the dataset,
                # but the values which are right, which doesn't have 1,5, which actually have 1.5 (a dot), they will be converted into NaN values
                dataset_clean[col_name] = replace

                # now to combine that data, because we have converted the right values int NaN values, so now all the NaN in the changed dataset will be filled with the right values which are in the copied dataset
                dataset_clean = dataset_clean.combine_first(dataset_clean_copied)

            return dataset_clean


        except Exception:
            print('')
            print('Column name does not occur in the dataset, try all over again (rerun the whole program) !!!')
            make_dataset()


    elif ask_modify_numbers == 'NO':
        return dataset_clean

    else:
        print('')
        print('Yes/No typed wrong in the input try all again (rerun the whole program) !!!')
        clean_drop_sort(dataset_clean)

    # ------------------------- CHANGE NUMBERS FORMAT (FROM 1,5 TO 1.5) END --------------------------------------------



# dataset --> dataset previously cleaned (or not, just read)
# X --> feature X, takes the column names
# Y --> label Y, takes column name
def set_convert_categorize(dataset, X, Y):

    # ----------------------------------- SET THE DATASET WITH COLUMNS SPECIFIED ---------------------------------------
    # EXCEPTION CHECK
    try:
        # make a dataframe with only those column names
        df_variables = dataset[[x for x in X] + [y for y in Y]]

        # if there is more or less than 1 label raise an exception
        if len(Y) != 1:
            raise Exception

    except Exception:
        print('')
        print('Oops something went wrong, try all over again (rerun the whole program) !!!')
        print('Most likely your dataset is not cleaned properly (Type Yes when you asked to clean it !!!), or you typed more than 1 label, or you just typed column names wrong.')
        make_dataset()
    # ------------------------------- SET THE DATASET WITH COLUMNS SPECIFIED END ---------------------------------------


    # --------------------------------------------- PRINT SOME INFO ----------------------------------------------------
    # this is just for decorating purposes, just on the label is written (y), to see exactly what's label
    list_columns = list(df_variables.columns)
    list_columns[-1] = list_columns[-1] + ' (y)'
    df_variables.columns = list_columns

    print()
    print('THIS IS THE DATAFRAME YOU HAVE CHOSEN !!!')
    print('')
    print(df_variables)

    # when our label has written to it (y), then remove that (y), to not making changes to the dataframe without any approval of user
    list_columns = list(df_variables.columns)
    list_columns[-1] = list_columns[-1][:-4]
    df_variables.columns = list_columns
    # ----------------------------------------- PRINT SOME INFO END ----------------------------------------------------



    # --------------------------------------- CONVERT NUMERIC VALUES INTO FLOATS ---------------------------------------
    # ask the user if wants to convert the entire dataset into floats, necessary for the algorithm to work with numeric data !!!
    print('')
    ask_convert = input('''Do you want to convert all numeric values of specified columns into floats? 
!!! When there is a value found NOT numeric, it will be converted as NaN (WATCHOUT for categorical columns) !!!
Yes/No: ''').upper()

    if ask_convert == 'YES':

        print('')
        print('THESE ARE YOUR COLUMNS NAMES:', list(df_variables.columns))
        print('')

        # ask fro column user wants to convert into float
        ask_columns = input('''OK, so type column which their numeric values will be converted into floats, and non numeric values will be converted into NaN (split with comma + space)
or type "all" when all columns will be converted into numeric: ''').split(', ')


        # if user types 'all' then do it for all columns
        if (len(ask_columns) == 1) and (ask_columns[0].lower() == 'all'):

            # pd.to_numeric() --> works for series only so that's why we iterate through each column to change each column into floats values
            # if they are numeric then convert them into float, if not --> error='coerce' --> will not numeric turn into NaN values
            for column_name in list(df_variables.columns):
                df_variables[column_name] = pd.to_numeric(df_variables[column_name], errors='coerce')

        else:
            # pd.to_numeric() --> works for series only so that's why we iterate through each column to change each column into floats values
            # if they are numeric then convert them into float, if not --> error='coerce' --> will not numeric turn into NaN values
            for column_name in ask_columns:

                if column_name not in list(df_variables.columns):
                    print('')
                    print('Oops, you typed column which does not occur in the dataset, try all over again (rerun the whole program) !!!')
                    make_dataset()

                else:
                    df_variables[column_name] = pd.to_numeric(df_variables[column_name], errors='coerce')


        # ask if NaN want to drop or replace with some integer
        print('')
        ask_drop_replace = input('''Ok, so now with converted values as floats, and not numeric converted as NaN.
Do you want to permanently delete rows which has NaN in them, or just want them to be replaced as outliers? Drop/Replace: ''').upper()

        if ask_drop_replace == 'DROP':
            print('OK, you decided to drop all rows which have NaN in them.')
            # drop all rows which has NaN values, and reset the index
            df_variables.dropna(inplace=True)
            df_variables.reset_index(drop=True, inplace=True)


        elif ask_drop_replace == 'REPLACE':

            try:
                # ask for the replacement which will be treated as an outlier
                ask_outlier = int(input('OK, so type a value which SHOULD be considered as an OUTLIER (f.e. -99 999...): '))
                # replace those NaNs with that outlier
                df_variables.replace(np.nan, ask_outlier, inplace=True)

            # if the outlier is input as a string or float
            except ValueError:
                print('')
                print('An outlier must be an integer, not a text or character or any decimal number, try all again (rerun the whole program) !!!')
                make_dataset()

        else:
            print('')
            print('Drop/Replace typed wrong in the input try all over again (rerun the whole program) !!!')
            make_dataset()

    elif ask_convert == 'NO':
        pass

    else:
        print('')
        print('Yes/No typed wrong in the input try all over again (rerun the whole program) !!!')
        make_dataset()
    # ----------------------------------- CONVERT NUMERIC VALUES INTO FLOATS END ---------------------------------------


    # ---------------------------------------- TAKE A LOOK AT THE DATASET ----------------------------------------------
    print()
    print('THIS IS HOW THE DATAFRAME LOOKS RIGHT NOW!!!')
    print('')
    print(df_variables)
    # ------------------------------------ TAKE A LOOK AT THE DATASET END ----------------------------------------------


    # ------------------------------------- CATEGORIZE/ENCODE SPECIFIC COLUMNS -----------------------------------------
    while True:

        # write down column names
        print('')
        print('AND THESE ARE THE COLUMN NAMES YOU HAVE CHOSEN:', list(df_variables.columns))

        # ask if wanna categorize the data meaning Male --> 1; Female --> 0 etc...
        ask_categorize = input('''
So now to categorize your data, write which of those variables written above (you have chosen), you want to categorize
Meaning if your data ain't numeric (north/east/west/south; True/False) you SHOULD categorize it.
Do you wanna make a categorization of any of your columns? Yes/No: ''').upper()

        if ask_categorize == 'YES':
            print('')
            ask_categorize = input('Write down variables (column names, you have) you want to categorize (split with comma + space): ').split(', ')

            # to check if it's written any of chosen variables to be categorized, returning boolean True or False, check if each column user input does appear in dataset
            # --> any takes only True, must be NONE False
            any_list = [x in list(df_variables.columns) for x in ask_categorize]

            # if wanna categorize
            if ((len(ask_categorize) > 0) and (len(ask_categorize) <= len(list(df_variables.columns)))) and any(any_list):

                # where unique values in each column will be stored in the list
                unique_vals_list = []
                for column_categorize in ask_categorize:
                    # add a list of unique values in each column, which wants to be categorized
                    unique_vals_list.append(list(df_variables[column_categorize].unique()))

                print('')
                print('!!! THIS IS HOW IT CATEGORIZED FOR EACH CATEGORY WRITE IT DOWN OR MEMORIZE IT !!!')

                # loop through each unique values list for each column which wants to be categorized, and column names written in input which wants to be categorized
                for unique_list, column_name in zip(unique_vals_list, ask_categorize):

                    # loop through each unique element in unique list of each column, and the length of that unique list
                    for element, num in zip(unique_list, range(len(unique_list))):
                        # write down element, what it was categorized into, that's why range(len), because we wanna categorize into 1s and 0s etc...
                        print(element, ' --> ', num)
                        # each that column replace each unique element with its unique numeric category
                        df_variables[column_name].replace(element, num, inplace=True)

                break

            else:
                print('')
                print('Wrong, input, check if that column actually is in that DataFrame, try again !!!')

        elif ask_categorize == 'NO':
            print('')
            print('OK, so no categorization.')
            break


        else:
            print('')
            print('Oops, wrong input, try again !!!')
    # --------------------------------- CATEGORIZE/ENCODE SPECIFIC COLUMNS END -----------------------------------------

    return df_variables



# dataset_balanced --> a dataset which wants too be balanced
# BALANCED --> same count for each category
def describe_balance(dataset_balance):

    # this is our Y column, our last column in our dataframe
    Y = list(dataset_balance.columns)[-1]

    # a dictionary of counts of Y column, each category has it's count
    dict_counts = dict(dataset_balance[Y].value_counts())


    # -------------------------------------- PRINT THE DESCRIPTION OF DF -----------------------------------------------
    # ask for description (mean, std, min, max etc...)
    print('')
    ask_describe = input('Wanna see the description of the variables you have chosen? Yes/No: ').upper()

    if ask_describe == 'YES':
        print('')
        print('THE DESCRIPTION OF YOUR DATASET')
        print(dataset_balance.describe())


    elif ask_describe == 'NO':
        pass

    else:
        print('')
        print('Oops, wrong input, try again (rerun the whole program) !!!')
        describe_balance(dataset_balance)
    # ---------------------------------- PRINT THE DESCRIPTION OF DF END -----------------------------------------------



    # --------------------------------------- PRINT VALUE COUNTS OF LABEL (Y) ------------------------------------------
    # ask for printing value counts
    print('')
    ask_value_counts = input('Do you also have your Y categorized? If yes then you will see the amount for each category. Yes/No: ').upper()

    if ask_value_counts == 'YES':
        print('')
        print('AMOUNT FOR EACH CATEGORY IN Y')
        print(dataset_balance[Y].value_counts())

    elif ask_value_counts == 'NO':
        pass

    else:
        print('')
        print('Oops, wrong input, try all over again (rerun the whole program) !!!')
        describe_balance(dataset_balance)
    # ----------------------------------- PRINT VALUE COUNTS OF LABEL (Y) END ------------------------------------------


    # ------------------------------------ BALANCE THE DATASET ---------------------------------------------------------
    # ask for balancing the dataset
    print('')
    ask_balance = input('''Do you wanna balance your data? 
Meaning when you wanna have the same amount of rows for each category.
Some of the data will be permanently deleted from the dataset, but it will be better and more effective for classification purposes.
Yes/No: ''').upper()

    if ask_balance == 'YES':
        # the min value a unique category has in Y column
        min_y_count = min(np.array(dataset_balance[Y].value_counts()))
        # the sum of counts of unique categories in Y column
        sum_y_count = np.sum(np.array(dataset_balance[Y].value_counts()))

        # for each category (key) and it's count (value)
        for category, max_size in dict_counts.items():

            # create a mask where there will be only those rows which has this specific category
            mask = (dataset_balance[Y] == category)
            # create a second dataframe where there will be only those rows which has the specific category, and then reset the index of that df
            df = dataset_balance.loc[mask]
            df = df.reset_index(drop=True)

            # if that category has the same amount of rows as the min, thne let it be
            if max_size == min_y_count:
                pass

            else:
                # if not drop values from the range min and its count, this will make a df with the same amount of rows like the category with min has
                # range(0, 2) --> removes rows with index 0 and 1
                df.drop(range(min_y_count, max_size), inplace=True)

            # add to the original dataset this modified/or_not dataframe with the same number of rows which has the category with min counts
            dataset_balance = dataset_balance.append(df, ignore_index=True)

        # then when all dataframes are added, delete all those rows which has been before this function started, before balancing, then reset the index
        dataset_balance.drop(range(sum_y_count), inplace=True)
        dataset_balance.reset_index(inplace=True, drop=True)

        # print the changed/or_not dataframe with the same counts for each category
        print('')
        print('AMOUNT FOR EACH CATEGORY IN Y AFTER BALANCING, EACH CATEGORY SHOULD HAVE THE SAME AMOUNT')
        print(dataset_balance[Y].value_counts())

    elif ask_balance == 'NO':
        print('OK, no balancing categorized.')

    else:
        print('')
        print('Oops, wrong input, try all over again (rerun the whole program) !!!')
        describe_balance(dataset_balance)
    # ------------------------------------ BALANCE THE DATASET END -----------------------------------------------------


    return dataset_balance



def make_dataset():

    print('')
    print('''
                            !!! IMPORTANT ANNOUNCEMENT !!!
IF YOU TYPE SOMETHING WRONG, BY TYPING A WRONG INPUT ETC., THE PROGRAM WILL TELL YOU.
IN THAT CASE PLEASE RERUN THE PROGRAM BY CLICKING SHIFT + F10 (if in PyCharm) OR F5 (when in shell) JUST RERUN THE WHOLE PROGRAM PLEASE !!! ''')


    # ask if user wants to just read the dataset, or to modify first
    print('')
    ask_customize_read = input('Do you want to first make changes to the dataset, make some modification, cleaning, balancing, or want to just read your dataset? Modify/Read: ').upper()

    if ask_customize_read == 'MODIFY':

        print('')

        # ----------------------------------- FUNCTION read_change_columns FOOL-PROOF --------------------------------------
        ask_dataset = input('Type the exact name of the dataset you wanna modify, must be in this directory!!!: ')
        ask_sep = input('What is the separator of that dataset? (","/ ";" / if tab --> backslash + t): ')
        ask_change_columns = input('Do you want change your columns names? Yes/No: ').upper()

        df = read_change_columns(ask_dataset, ask_sep, ask_change_columns)
        # ------------------------------------------------------------------------------------------------------------------


        # ----------------------------------- FUNCTION clean_drop_sort FOOL-PROOF ------------------------------------------
        df = clean_drop_sort(df)
        # ------------------------------------------------------------------------------------------------------------------

        print('')
        print('THIS IS HOW YOUR DATASET LOOKS LIKE RIGHT NOW !!!')
        print(df)

        # ------------------------------------ FUNCTION set_categorize FOOL-PROOF -------------------------------------------
        print('')
        print(' !!! HERE ARE YOUR COLUMN NAMES:\n', list(df.columns))
        print('')

        ask_X = input('Type all column names you want for feature(s) (for X variable, Independent Variable) (split with comma + space): ').split(', ')
        ask_Y = input('Type column names you want for label (for Y, Dependent Variable) (split with comma + space): ').split(', ')

        df = set_convert_categorize(df, ask_X, ask_Y)
        # ------------------------------------------------------------------------------------------------------------------

        print('')
        print('THIS IS HOW YOUR DATASET LOOKS LIKE RIGHT NOW !!!')
        print(df)

        # ---------------------------------- FUNCTION describe_balance FOOL-PROOF ------------------------------------------
        df = describe_balance(df)
        # ------------------------------------------------------------------------------------------------------------------

        print('')
        print('THIS IS HOW YOUR DATASET LOOKS LIKE RIGHT NOW !!!')
        print(df)

        # --------------------------------------------- SAVE DATASET --------------------------------------------------------
        print('')
        ask_save = input('Do you wanna save that dataframe for later use? Yes/No: ').upper()

        if ask_save == 'YES':

            print('')
            ask_name = input('''OK, so how do you wanna call that new file you wanna save?
Do not type .csv at the end !!!
It will saved in this current directory you are using, and it will be saved as csv file !!!
type name: ''')
            ask_sep = input('What separator you wanna set for that dataset?: ')

            try:
                # index=False, it will not make and index column when saving it
                df.to_csv(ask_name + '.csv', sep=ask_sep, index=False)

            except Exception:
                print('')
                print('Oops, something was input wrong, try not to type .csv at the end of the name or any other file format, try all over again (rerun the whole program) !!!')
                make_dataset()

        elif ask_save == 'NO':
            print('')
            print('OK, I will not save that dataset')

        else:
            print('')
            print('Oops, wrong input Yes/No, try all over again (rerun the whole program) !!!')
            make_dataset()
        # --------------------------------------------------------------------------------------------------------------------

        # now return a whole modified/cleaned/categorized dataframe with only those variables he/she want to use for feature(s) and label
        return df


    # if just read
    elif ask_customize_read == 'READ':
        # ask for the name of file and the separator
        print('')
        ask_dataset = input('Type the exact name of the dataset you wanna read, must be in this directory!!!: ')
        ask_sep = input('What is the separator of that dataset? (","/ ";" / " "): ')

        # check for exceptions
        try:
            # read that file, print it how it looks, and return it
            df = pd.read_csv(ask_dataset, sep=ask_sep, engine='python')

            print('')
            print('THIS IS YOUR DATASET YOU HAVE READ !!!')
            print(df)

            return df

        except Exception:
            print('')
            print('Something went wrong, file does not exist or the separator has been input wrong, try again (rerun the whole program) !!!')
            make_dataset()

    else:
        print('')
        print('Modify/Read was input wrong, try again (rerun the whole program) !!!')
        make_dataset()
