import pandas as pd


def convert_column_to_numeric(df,col,notify_changes=True):
    '''
    Convert a column to numeric, setting errors to NaN, and notifying the user of the changes made.
    This function is used to clean the column in the dataframe.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with the column converted to numeric
    '''

    # Keep a copy of the original column for comparison
    original = df[col].copy()

    # Conversion
    converted = pd.to_numeric(df[col], errors='coerce')

    # Update the DataFrame
    df[col] = converted
    # Notify the user of changes
    if notify_changes:
        for k in range(len(original)):
            if converted.isna()[k] and original.notna()[k]:
                print(f"{df['Time Period Start'].iloc[k]} / Row {k}: Converted {col} from '{original.iloc[k]}' to '{df[col].iloc[k]}'")

    return df


def convert_column_to_date(df,col,notify_changes=True):
    '''
    Convert a column to a date, setting errors to NaN, and notifying the user of the changes made.
    This function is used to clean the column in the dataframe.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with the column converted to date
    '''

    # Keep a copy of the original column for comparison
    original = df[col].copy()

    # Conversion
    converted = pd.to_datetime(df[col], errors='coerce')

    # Update the DataFrame
    df[col] = converted
    
    # Notify the user of changes
    if notify_changes:
        for k in range(len(original)):
            if converted.isna()[k] and original.notna()[k]:
                print(f"{df['Time Period Start'].iloc[k]} / Row {k}: Converted {col} from '{original.iloc[k]}' to '{df[col].iloc[k]}'")

    return df
