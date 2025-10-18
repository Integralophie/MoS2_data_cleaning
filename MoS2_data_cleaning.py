import pandas as pd
import matplotlib.pyplot as plt


def read_csv_direction(filename):
    '''
    Reads the csv file, converts `ID` unit to uA, and adds a line representing
    forward and backward loop

    Arg:
        filename: a string containing the file name of csv files
    '''
    df  = pd.read_csv(filename, skiprows=259)
    df.drop(df.columns[0], axis=1, inplace=True)
    
    df[' ID'] = df[' ID'] * 1E6    # converts unit

    df[' forward'] = True    

    df.loc[(df.index >= 101) & (df.index <= 201), ' forward'] = False
    df.loc[(df.index >= 303) & (df.index <= 403), ' forward'] = False
    df.loc[(df.index >= 505) & (df.index <= 605), ' forward'] = False
    df.loc[(df.index >= 707) & (df.index <= 807), ' forward'] = False
    df.loc[(df.index >= 909) & (df.index <= 1009), ' forward'] = False
    df.loc[(df.index >= 1111) & (df.index <= 1211), ' forward'] = False
    df.loc[(df.index >= 1313) & (df.index <= 1413), ' forward'] = False

    return df


def reshape_table_by_VG(df):
    df_new = pd.pivot_table(df,columns=' VG',values=[' ID'],index=[' VD',' forward'])

    df_sorted = df_new.sort_values(by=[' forward',' VD'])

    return df_sorted


def reorder_by_VD(df_sorted):
    '''
    Separates the dataframe into two. The first half is sorted in ascending
    order based on Vd, and the second is descending. Also changes column name
    by V_G = {VG}
    '''
    midpoint = len(df_sorted) // 2

    # Split the DataFrame into two halves
    first_half = df_sorted.iloc[:midpoint]
    second_half = df_sorted.iloc[midpoint:]

    # Sort the first half in ascending order based on 'col1'
    first_half_sorted = first_half.sort_values(by=' VD', ascending=True)
    # Sort the second half in descending order based on 'col1'
    second_half_sorted = second_half.sort_values(by=' VD', ascending=False)
    # Concatenate the sorted halves back together
    sorted_df = pd.concat([first_half_sorted, second_half_sorted])


    column_names_list = sorted_df.columns.tolist()
    new_list = []

    for tup in column_names_list:
        new_list.append(f'V_G = {tup[1]}')


    sorted_df.columns = new_list

    return sorted_df



# sorted_df.to_csv('output.csv', index=True)


def read_csv_IdVtg(filename):
    df  = pd.read_csv(filename, skiprows=256)
    df.drop(df.columns[0], axis=1, inplace=True)
    Vbg = df.iloc[1, 2]
    df.drop(columns=[' Vbg', ' IS'], inplace=True)

    df[' forward'] = True

    df.loc[(df.index >= 201) & (df.index <= 401), ' forward'] = False
    df.loc[(df.index >= 603) & (df.index <= 803), ' forward'] = False
    df.loc[(df.index >= 1005) & (df.index <= 1205), ' forward'] = False
    df.loc[(df.index >= 1407) & (df.index <= 1607), ' forward'] = False
    return Vbg, df



def reshape_table_by_VG(df):
    df_new = pd.pivot_table(df,columns=' VD',values=[' ID',' ITG',' Ibg'],index=[' VTG',' forward'])
    df_sorted = df_new.sort_values(by=[' forward',' VTG'])
    return df_sorted


def reorder_by_VG(df_sorted, Vbg):
    midpoint = len(df_sorted) // 2

    # Split the DataFrame into two halves
    first_half = df_sorted.iloc[:midpoint]
    second_half = df_sorted.iloc[midpoint:]

    # Sort the first half in ascending order based on 'col1'
    first_half_sorted = first_half.sort_values(by=' VTG', ascending=True)

    # Sort the second half in descending order based on 'col1'
    second_half_sorted = second_half.sort_values(by=' VTG', ascending=False)

    # Concatenate the sorted halves back together
    sorted_df = pd.concat([first_half_sorted, second_half_sorted])

    column_names_list = sorted_df.columns.tolist()

    new_list = []
    for tup in column_names_list[0:4]:
        new_list.append(f'Id, V_D = {tup[1]}')
    for tup in column_names_list[4:8]:
        new_list.append(f'Itg, V_D = {tup[1]}')
    for tup in column_names_list[8:]:
        new_list.append(f'Ibg, V_D = {tup[1]}')

    sorted_df.columns = new_list

    df_new = sorted_df.reset_index().set_index(' VTG')
    df_new['Itg, V_D = 0.1'] = abs(df_new['Itg, V_D = 0.1'])
    df_new['Id, V_D = 0.1'] = abs(df_new['Id, V_D = 0.1'])
    df_new.drop(columns=[' forward', 'Itg, V_D = 0.4', 'Itg, V_D = 0.7', 'Itg, V_D = 1.0','Ibg, V_D = 0.4', 'Ibg, V_D = 0.7', 'Ibg, V_D = 1.0'],inplace=True)
    df_new[' Vbg'] = Vbg

    return df_new