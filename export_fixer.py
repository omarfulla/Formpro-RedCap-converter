#! /usr/bin/env python3
"""UKE Export Fixer

Call function with an csv export from formPro:
    $ ./export_fixer.py export.csv

Todo:
    * more comments

***This was a Google style docstring***
"""

import sys
import math
import re
import numpy as np
import pandas as pd

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def main():
    """main function

    Main executes fixer if used on its own

    """

    print("\n\nWelcome to the FormPro Export Fixer\n")
    data = load_file()
    show_header(data)
    data = show_columnwise(data)
    write_to_csv(data, sys.argv[1])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def load_file():
    """load_file function

    - checks if a file is given, otherwise asks for a file
    - reads the csv file into a pandas dataframe

    Returns:
        data: DataFrame of the loaded csv

    """
    if len(sys.argv) == 1:
        print("Please enter path to file: ")
        file_path = input()
    else:
        file_path = sys.argv[1]

    data = pd.read_csv(file_path, decimal=',')
    data = data.fillna(-99)
    return data

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def show_header(data):
    """show_header function

    - prints the header of the dataframe

    Args:
        data (pandas.DataFrame): dataframe which head will be printed

    """
    print("The data you are going to edit is: ")
    print(data.head())

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def show_columnwise(data, keys=None):
    """show_columnwise function

    - prints columns of the given dataframe
    - allows to choose an action which will be performed on the current column
    - writes the edited dataframe to csv after every column

    Args:
        data (pandas.DataFrame): dataframe which head will be printed
        keys (list, optional): If a list of keys is given, only those will be
            printed

    """
    if keys is None:
        keys = data.keys()
    for key in keys:
        write_to_csv(data)
        sucessful = False
        while not sucessful:
            print(key)
            print(data[key], "\n")
            print("Which operation shall be executed?")
            print("0) Do nothing")
            print("1) add One (y=x+1)")
            print("2) decrease by one and to the power of 2 (y=2^(x-1))")
            print("3) inverse values and decrease by one (y=(x-(xMax+1)*-1))")
            print("4) inverse values (y=(x-xMax)*-1")
            print("5) format date (YYY-MM-DD)")
            print("6) fix multiple choice (generate new columns)")
            print("7) substract one (y=x-1)")
            print("8) Replace 0 with -99")
            #except value error if an non int is typed in
            try:
                method = int(input())
            except ValueError:
                sucessful = False
            else:
                if method == 0:
                    sucessful = True
                elif method < 6  or method == 7 or method == 8:
                    data[key] = apply_fix(method, data[key])
                    if query_yes_no("Fix something else on those columns?"):
                        sucessful = False
                    else:
                        sucessful = True
                elif method == 6:
                    old_cols = data.shape[1]
                    data = apply_fix(method, data[key], data)
                    data = data.drop(key, axis=1)
                    nof_new_cols = data.shape[1] - old_cols
                    list_of_new_cols = list(
                        data.columns.values[
                            old_cols - 1: old_cols + nof_new_cols])
                    if query_yes_no("Fix something else on those columns?"):
                        show_columnwise(data, list_of_new_cols)
                    sucessful = True
                else:
                    sucessful = False
    return data

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def apply_fix(method, column, data=None):
    """apply_fix function

    """
    column_cpy = column.copy()

    if method == 1:
        column = add_one(column, column_cpy)
    elif method == 2:
        column = decrease_and_pow_two(column, column_cpy)
    elif method == 3:
        column = invert_decrease_one(column, column_cpy)
    elif method == 4:
        column = invert(column, column_cpy)
    elif method == 5:
        column = format_date(column, column_cpy)
    elif method == 6:
        data = pd.concat([data, multiple_choice(column)], axis=1)
        return data
    elif method == 7:
        column = substract_one(column, column_cpy)
    elif method == 8:
        column = replace_zero(column, column_cpy)
    return column

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def add_one(column, column_cpy):
    """function
    """
    #for i in range(0, len(column)):
    for counter, value in enumerate(column):
        if check_value(value):
            column_cpy[counter] = value + 1
        else:
            column_cpy[counter] = value
    return column_compare(column, column_cpy)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def replace_zero(column, column_cpy):
    """function
    """
    #for i in range(0, len(column)):
    for counter, value in enumerate(column):
        if check_value(value):
            if value == 0 or value == '0' or value == '0.0':
                column_cpy[counter] = -99
            else:
                column_cpy[counter] = value
        else:
            column_cpy[counter] = value
    return column_compare(column, column_cpy)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def substract_one(column, column_cpy):
    """function
    """
    for counter, value in enumerate(column):
        if check_value(value):
            column_cpy[counter] = int(value) - 1
        else:
            column_cpy[counter] = value
    return column_compare(column, column_cpy)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def check_value(val):
    """function
    """
    try:
        val = int(val)
    except ValueError:
        print("not an int")
        print(val.isdigit())
        return False
    else:
        if (val == -99 or val == -88 or math.isnan(val)):
            return False
    return True

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def column_compare(column, column_cpy, errors=[]):
    """function
    """
    for counter, value in enumerate(column):
        if counter in errors:
            print("\033[31m", value, "\t", column_cpy[counter], "\033[0m")
        else:
            print(value, "\t", column_cpy[counter])
    if query_yes_no("Apply those changes?"):
        for counter, value in enumerate(column):
            column[counter] = column_cpy[counter]
    print(column[0])
    return column

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def invert_decrease_one(column, column_cpy):
    """function
    """
    print("What is the maximum possible value?")
    x_max = int(input())
    for counter, value in enumerate(column):
        if check_value(value):
            column_cpy[counter] = (value - (x_max + 1)) * -1
        else:
            column_cpy[counter] = value
    return column_compare(column, column_cpy)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def decrease_and_pow_two(column, column_cpy):
    """function
    """
    for counter, value in enumerate(column):
        if check_value(value) and value != 0:
            column_cpy[counter] = math.pow(2, value - 1)
        else:
            column_cpy[counter] = value
    return column_compare(column, column_cpy)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def invert(column, column_cpy):
    """function
    """
    print("What is the maximum possible value?")
    x_max = int(input())
    for counter, value in enumerate(column):
        if check_value(value):
            column_cpy[counter] = (value - x_max) * -1
        else:
            column_cpy[counter] = value
    return column_compare(column, column_cpy)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def format_date(column, column_cpy):
    """function
    """
    errors = []
    column = column.fillna(value=0)
    for counter, value in enumerate(column):
        if check_value(value):
            value = int(value)
            if len(str(value)) == 7:
                column_cpy[counter] = (str(value)[-4:] + "-"
                                       + str(value)[1:-4] + "-" + str(0)
                                       + str(value)[:1])
            elif len(str(value)) == 8:
                column_cpy[counter] = (str(value)[-4:] + "-"
                                       + str(value)[2:-4] + "-"
                                       + str(value)[:2])
            elif len(str(value)) == 6:
                #if year is less then 25 it must be 2025 or less
                if int(str(value)[-2:]) <= 25:
                    year = "20"
                #if year is more then 25 it must be 1925 or higher
                else:#(int(str(value)[-2:]) <= 25):
                    year = "19"
                column_cpy[counter] = year + str(value)[-2:] + "-" \
                    + str(value)[2:4] + "-" + str(value)[:2]
            else:
                print("\033[31m" + "Something went wrong" + '\033[0m')
                #collect rows which have an error, to highlight them later
                errors.append(counter)
    return column_compare(column, column_cpy, errors)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def write_to_csv(data, file_name='WIP'):
    """function
    """
    file_name = file_name.split('.')[0]
    file_name = file_name + "_fixed" + ".csv"
    data.to_csv(file_name, index=False)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def multiple_choice(column):
    """function
    """
    unique = [] # stores each given aswer once
    col_vals = dict() # saves patients to each answer
    extradata = pd.DataFrame() # for the new columns

    for counter, value in enumerate(column):
        matches = re.findall('([0-9]+)', str(value))
        for numbers in matches:
            if check_value(numbers) and value != "-99":
                numbers = int(numbers)
                if numbers not in unique:
                    unique.append(numbers)
                    col_vals[numbers] = [counter]
                else:
                    col_vals[numbers].append(counter)
    unique.sort()
    for num in unique:
        data = np.zeros(column.size, dtype=int)
        new_col = pd.Series(data, dtype=int)
        name = column.name + "___" + str(num)
        new_col = new_col.rename(name)
        for patient in col_vals[num]:
            new_col[patient] = 1
        extradata = extradata.append(new_col)
    print(extradata)
    return extradata.transpose()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == "__main__":
    main()
