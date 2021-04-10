#! /usr/bin/env python3
import sys
import math
import re
import numpy as np
import pandas as pd

def check_value(val):
    """function"""
    try:
        val = int(float(val))
    except ValueError:
        #print('{} should be a number in your file'.format(val))
        return False
    else:
        if (val == -99):
            return True
        elif(val == -88 or math.isnan(val)):
            return False
    return True

def format_date(column, column_cpy):
    """function"""
    errors = []
    column = column.fillna(value=-99)
    for counter, value in enumerate(column):
        # The line number is the index in Column + 2
        # The index starts with 0 and the first line is the header
        line = counter + 2
        if check_value(value):
            value = int(value)
            if len(str(value)) == 7:
                column_cpy[counter] = (str(value)[-4:] + "-"
                                       + str(value)[1:-4] + "-" + str(0)
                                       + str(value)[:1])
            elif len(str(value)) == 8:
                if value == 99999999 :
                    column_cpy[counter] = '1900-01-01'
                else :
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
            elif value == -99:
                column_cpy[counter] = '1900-01-01'
            else:
                print(f"Please correct the date ( {value} ) in line {line}")
                # print("\033[31m" + "Something went wrong" + '\033[0m')
                #collect rows which have an error, to highlight them later
                # will not be used
                errors.append(counter)
        else:
            print(f"The date ( {value} ) in line {line} should be a number to be converted to a date")
    return column_cpy, errors

def multiple_choice(column):
    unique = [] # stores each given aswer once
    col_vals = dict() # saves patients to each answer
    extradata = pd.DataFrame() # for the new columns
    for counter, value in enumerate(column):
        matches = re.findall('([0-9]+)', str(value))
        for numbers in matches:
            if check_value(numbers):
                numbers = int(float(numbers))
                if numbers not in unique:
                    unique.append(numbers)
                    col_vals[numbers] = [counter]
                else:
                    col_vals[numbers].append(counter)
    unique.sort()
    for num in unique:
        data = np.zeros(column.size, dtype=int)
        new_col = pd.Series(data, dtype=int)
        if num == 99:
            name = column.name + "____" + str(num)
            new_col = new_col.rename(name)
        else:
            name = column.name + "___" + str(num)
            new_col = new_col.rename(name)
        for patient in col_vals[num]:
            new_col[patient] = 1
        extradata = extradata.append(new_col)
    extradata = extradata.astype(int)
    return extradata.transpose()
def write_to_csv(data, file_name='WIP'):
    file_name = file_name.split('.')[0]
    file_name = file_name + "_fixed" + ".csv"
    data.to_csv(file_name, index=False)

if __name__ == '__main__':
    dictionary = pd.read_csv(r"C:\Users\Omar\Downloads\DataDictionary.csv", index_col =0, skiprows=0)
    # dtype=str has been used to replace the -99.0 with -99
    data = pd.read_csv(r"C:\Users\Omar\Documents\New Exports\test.csv", dtype=str, sep=';')
    data = data.fillna(int(-99))
    #data.replace(r'\d+\.0', 'new', regex=True)
    data.insert(1, 'redcap_event_name', 'z10_arm_2')
    only_date = dictionary[dictionary['Text Validation Type OR Show Slider Number'] == 'date_dmy']
    checkbox = dictionary[dictionary['Field Type'] == 'checkbox']
    keys = data.keys()
    i = 1
    for key in keys:
        column =data[key]
        column_cpy = column.copy()
        if(key in checkbox.index):
            old_cols = data.shape[1]
            data = data.drop(key, axis=1)
            nof_new_cols = data.shape[1] - old_cols
            list_of_new_cols = list(data.columns.values[old_cols - 1: old_cols + nof_new_cols])
            data = pd.concat([data, multiple_choice(column)], axis=1)
        elif(key in only_date.index):
            data[key], errors = format_date(column, column_cpy)
            #print(errors)
    write_to_csv(data, r"C:\Users\Omar\Documents\New Exports\test.csv")