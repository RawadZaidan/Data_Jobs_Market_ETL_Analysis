from lookup import ErrorHandling, CSV_FOLDER_PATH
from logging_handler import show_error_message
import pandas as pd
import os
       
def remove_duplicates(df, column=None):
    try:
        df_no_duplicates = None
        if column is None:
            df = df.drop_duplicates()
        else:
            df_no_duplicates = df.drop_duplicates(subset=[column])
        return df_no_duplicates
    except Exception as e:
        error_string_prefix = ErrorHandling.DB_RETURN_QUERY_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return df_no_duplicates

#This function automatically drops any row with a None value
def drop_nulls(df, all=False, column=None):
    try:
        return_df = df
        if all:
            return_df = df.dropna(how='all')
        elif column is not None:
            return_df = df.dropna(subset=column)
        elif column is not None and all:
            print('Please pick only 1 type. Leave empty for any, all for rows ')
        else:
            return_df = df.dropna()
        return return_df
    except Exception as e:
        error_string_prefix = ErrorHandling.PANDAS_NULLS_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return return_df

def fill_nulls(df, all=False, column=None):
    try:
        return_df = df.copy()
        if all:
            return_df = df.fillna(0)
        elif column is not None:
            return_df[column] =df[column].fillna(0)
        elif column is not None and all:
            print('Please pick only 1 type. Leave empty for any, all for rows ')
        else:
            return_df = df.fillna(0)
        return return_df
    except Exception as e:
        error_string_prefix = ErrorHandling.PANDAS_FILL_NULLS_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return return_df

def fill_nulls_with_mean(df, all=False, column=None):
    try:
        return_df = df.copy()
        if all:
            return_df.fillna(return_df.mean(), inplace=True)
        elif column is not None:
            return_df[column].fillna(return_df[column].mean(), inplace=True)
        elif column is not None and all:
            print('Please pick only 1 type. Leave empty for any, all for rows ')
        return return_df
    except Exception as e:
        error_string_prefix = ErrorHandling.PANDAS_FILL_NULLS_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return return_df

def get_csv_file_names_into_list(folder_path = CSV_FOLDER_PATH.NAME.value):
    try:
        csv_files_names = []
        for filename in os.listdir(folder_path):
            if filename[-4:] == ".csv":
                csv_files_names.append(filename)
    except Exception as e:
        error_string_prefix = ErrorHandling.CSV_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return csv_files_names


def get_csv_file_names_into_dict(folder_path=CSV_FOLDER_PATH.NAME.value):
    try:
        csv_files_dict = {}
        for filename in os.listdir(folder_path):
            if filename[-4:] == ".csv":
                csv_files_dict[filename] = None
    except Exception as e:
        error_string_prefix = ErrorHandling.CSV_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return csv_files_dict


def return_paths_dict(list_of_paths, subfolder_name = CSV_FOLDER_PATH.NAME.value):
    return_path_dict = {}
    current_directory = os.getcwd()
    subfolder_path = os.path.join(current_directory, subfolder_name)
    for file in list_of_paths:
        cssss = file
        item_relative_path = os.path.join(subfolder_path, cssss)
        name_of_table = remove_spaces_from_string(file)
        return_path_dict[name_of_table[:-4]] = item_relative_path
    return return_path_dict

def get_blanks(df):
    blank_df = None
    try:
        blank_df = df.isnull().any(axis=1)
    except Exception as e:
        error_string_prefix = ErrorHandling.PANDAS_BLANKS_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return blank_df

def get_shape(df):
    Shape = None
    try:
        blank_df = df.shape
    except Exception as e:
        error_string_prefix = ErrorHandling.PANDAS_SHAPE_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return Shape
    
def get_length(df):
    Length = None
    try:
        blank_df = len(df)
    except Exception as e:
        error_string_prefix = ErrorHandling.PANDAS_LEN_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return Length
    
def remove_spaces_from_columns_df(df):
    for column in df.columns:
        new_column_name = column.replace(' ', '_')
        df.rename(columns={column: new_column_name}, inplace=True)
    return df

def remove_spaces_from_string(name):
    name = name.replace(' ', '_')
    return name

def return_paths(list_of_paths, subfolder_name): 
    return_path_list = []
    current_directory = os.getcwd()
    subfolder_path = os.path.join(current_directory, subfolder_name)
    for file in list_of_paths:
        cssss= file
        item_relative_path = os.path.join(subfolder_path, cssss)
        name_of_table = remove_spaces_from_string(file[:-4])
        return_path_list.append([name_of_table,item_relative_path])
    return return_path_list

def return_paths_as_dict(list_of_paths, subfolder_name):
    return_path_dict = {}
    current_directory = os.getcwd()
    subfolder_path = os.path.join(current_directory, subfolder_name)
    for file in list_of_paths:
        cssss = file
        item_relative_path = os.path.join(subfolder_path, cssss)
        name_of_table = remove_spaces_from_string(file[:-4])
        return_path_dict[name_of_table] = item_relative_path
    return return_path_dict
