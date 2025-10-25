#!/usr/bin/env python3
'''
This code allow to compare multiple Dataset files to see if they have the same data.

Experiment,
Flux Type,
Options,
Background Subtraction,
Time Period Start,
Time Period End,
All Fluxes Time Series,

>10.0 MeV 10.0 pfu		>30.0 MeV 1.0 pfu			>50.0 MeV 1.0 pfu       >100.0 MeV 1.0 pfu
>10.0 MeV 1e-06 pfu		>30.0 MeV 1e-06 pfu		    >50.0 MeV 1e-06 pfu		>100.0 MeV 1e-06 pfu	

		Flux Time Series,
		SEP Start Time,
		pfu SEP End Time,
		SEP Duration (hours),
		Onset Peak (pfu),
		Onset Peak Time,
		Rise Time to Onset (minutes),
		Max Flux (pfu),
		Max Flux Time,
		Rise Time to Max (minutes),
		Fluence (cm^-2),
		Fluence Spectrum (cm^-2),
		Fluence Spectrum Energy Bins (MeV),
		Fluence Spectrum Energy Bin Centers (MeV),
Other parameters:
    Cycle,
    EventType,
    Case,
    Flare Xray Start Time,
    Flare Xray Peak Time,
    Flare X-ray End Time,
    Flare Class,
    Flare Opt,
    Flare Magnitude,
    Flare Integrated Flux,
    Flare Duration,
    Flare Xray Time To Peak,
    Active Region,
    AR Area,
    AR Spot Class,
    AR Mag Class,
    AR Carrington,
    Event Location From Center,
    Event Latitude,
    Event Longitude,
    Event Location Source,
    Event Location from Center 2,
    Event Latitude 2,
    Event Longitude 2,
    Event Location Source 2,
    Radio Rbr245Max,
    Radio Rbr2695Max,
    Radio Rbr8800,
    Radio TyIII_Imp,
    Radio m_TyII Start Time,
    Radio m_TyII End Time,
    Radio TyII Imp,
    Radio TyII Speed,
    Radio m_TyII Start Frequency,
    Radio m_TyII End Frequency,
    Radio Station,
    Radio DH Start Time,
    Radio DH End Time,
    Radio DH Start Frequency,
    Radio DH End Frequency,
    Radio DH Note,
    Radio TyIV Start Time,
    Radio TyIV End Time,
    Radio TyIV Imp,
    Radio TyIV Duration,
    CME CDAW First Look Time,
    CDAW CME Speed,
    DONKI CME Speed,
    CME Width,
    CME Mean Position Angle,
    ESP_CME,
    GLE Event Number,
    PRF,Comments
'''


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from constants import TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100, EVENT_TYPES
from constants import EASTERN, WESTERN, TIME_FLARE, TIME_CME, TIME_PEAK, TIME_MAX, TIME_SEP

plt.style.use('seaborn-darkgrid')


#First dataset
file_name1='GOES-06_integral_enhance_idsep.1986-01-01.1994-11-30_sep_events_CA.csv'
file_path1='../dataset_comparison/'
df_CA = pd.read_csv(file_path1+file_name1)


#Second dataset
file_name2='GOES-06_integral_enhance_idsep.1986-01-01.1994-11-30_sep_events_CC.csv'
file_path2='../dataset_comparison/'
df_CC = pd.read_csv(file_path2+file_name2)


#Second dataset
file_name3='GOES-06_integral_enhance_idsep.1986-01-01.1994-11-30_sep_events_KW.csv'
file_path3='../dataset_comparison/'
df_KW = pd.read_csv(file_path3+file_name3)

def test_dataframe_format(df1,name1,df2,name2):

    print(f'\nTesting if the dataset {name1} format match the dataset from {name2}...')
    (N1,M1)=df1.shape
    df1_1st_line=list(df1.columns)
    
    (N2,M2)=df2.shape
    df2_1st_line=list(df2.columns)

    assert M1==M2,f'The two Dataset are different: \nThe dataset {name1} has {M1} columns why the dataset {name2} has {M2} columns.'
    assert N1==N2, f'The two Dataset are different: \nThe dataset {name1} has {N1} lines why the dataset {name2} has {N2} lines.'
    print(f'\tThe two datasets have the same number of lines')
    for k in range(M1):
        
        assert df1_1st_line[k]==df2_1st_line[k], f'The column {df1_1st_line[k]} of the dataset {name1} does not match the column {df2_1st_line[k]} of the dataset {name2}, one column may be missing, or the columns may be in a different order'
    print(f'\tThe columns name of the dataset {name1} and the dataset {name2} match perfectly (same name and same order)')

def test_columns_print_all(df1,name1,df2,name2):
    '''
    This function test if the two dataframe have the same data in each column
    It is assumed that the two dataframe have the same format (verified with the function test_dataframe_format).
    Then it tests for each column if the data for each line match. 
    If a difference is found, it is printed in the terminal.
    At the end, an assertion is raised if the two dataframe are not the same.

    Parameters:
    -----------
    df1: pandas dataframe
        First dataframe to compare
    name1: str
        Name of the first dataframe (for printing purposes)
    df2: pandas dataframe
        Second dataframe to compare
    name2: str
        Name of the second dataframe (for printing purposes)
    -----------
    Returns:
    None
    '''

    (M,N)=df1.shape
    column_name=list(df1.columns)
    period_start='Time Period Start'

    are_datasets_equals=True #Flag to check if the two datasets are the same

    print(f'\nTesting if the dataset {name1} is the same as the dataset {name2}...')

    for column in column_name:

        print(f'Testing if the columns "{column}" match...')
        are_columns_equals=True #Reset the flag for each column

        for line_nb in range(M):
            elmnt1=df1[column].iloc[line_nb]
            elmnt2=df2[column].iloc[line_nb]
            if(pd.notnull(elmnt1) or pd.notnull(elmnt2)): #It allows to skip the comparison if both values are NaN

                if(elmnt1!=elmnt2):

                    are_datasets_equals=False #Set the flag to False since a difference was found
                    are_columns_equals=False #Set the flag to False since a difference was found

                    print(f'\t{df1[period_start].iloc[line_nb]} (line={line_nb}):')
                    print(f'\t\t The value for the dataset {name1} is {elmnt1} while the value for the dataset {name2} is {elmnt2}')
        
        if(are_columns_equals):
            print(f'\t The columns "{column}" match perfectly for both datasets\n')
    
    #If there was any difference found it raise an assertion
    assert (are_datasets_equals),f'The datasets {name1} and {name2} are not the same. All the differences are listed above'
    print(f'\nThe datasets {name1} and {name2} are the same! (except for the columns "**** Fluence Spectrum (cm^-2)")')

def test_columns_print_errors(df1,name1,df2,name2):
    '''
    This function test if the two dataframe have the same data in each column
    It is assumed that the two dataframe have the same format (verified with the function test_dataframe_format).
    Then it tests for each column if the data for each line match. 
    If a difference is found, it is printed in the terminal.
    At the end, an assertion is raised if the two dataframe are not the same.

    Parameters:
    -----------
    df1: pandas dataframe
        First dataframe to compare
    name1: str
        Name of the first dataframe (for printing purposes)
    df2: pandas dataframe
        Second dataframe to compare
    name2: str
        Name of the second dataframe (for printing purposes)
    -----------
    Returns:
    None
    '''

    (M,N)=df1.shape
    column_name=list(df1.columns)
    period_start='Time Period Start'

    are_datasets_equals=True #Flag to check if the two datasets are the same

    print(f'\nTesting if the dataset {name1} is the same as the dataset {name2}...')

    for column in column_name:
        nb_differences=0 #Counter of differences found in the column
        nb_non_both_null=0 #Counter of non simultaneously null values in the column

        for line_nb in range(M):

            elmnt1=df1[column].iloc[line_nb]
            elmnt2=df2[column].iloc[line_nb]

            if(pd.notnull(elmnt1) or pd.notnull(elmnt2)): #It allows to skip the comparison if both values are NaN
                nb_non_both_null+=1
                if(elmnt1!=elmnt2):

                    if(nb_differences==0): #Print the column name only once
                        print(f'\nThe columns "{column}" don\'t match...\n')

                    are_datasets_equals=False #Set the flag to False since a difference was found
                    nb_differences+=1

                    if not("Fluence Spectrum (cm^-2)" in column):
                        print(f'\t{df1[period_start].iloc[line_nb]} (line={line_nb}):')
                        print(f'\t\t The value for the dataset {name1} is {elmnt1} while the value for the dataset {name2} is {elmnt2}')
        
        if(nb_differences>0):
            print(f'\t {nb_differences} differences found in the column "{column}" over {nb_non_both_null} non-simultaneously null values')

    #If there was any difference found it raise an assertion
    assert (are_datasets_equals),f'The datasets {name1} and {name2} are not the same. All the differences are listed above'
    print(f'\nThe datasets {name1} and {name2} are the same!')

#Test Campaign:

test_dataframe_format(df_CC,'CC',df_CA,'CA')
test_columns_print_errors(df_CC,'CC',df_CA,'CA')

test_dataframe_format(df_CC,'CC',df_KW,'KW')
test_columns_print_errors(df_CC,'CC',df_KW,'KW')

test_dataframe_format(df_KW,'KW',df_CA,'CA')
test_columns_print_errors(df_KW,'KW',df_CA,'CA')