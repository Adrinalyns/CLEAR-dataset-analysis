#!/usr/bin/env python3

import pandas as pd
import numpy as np

from src.constants import TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100, EVENT_TYPES
from src.constants import TIME_FLARE, TIME_CME, TIME_PEAK, TIME_MAX, TIME_SEP
from src.constants import FLARE_TO_PEAK, CME_TO_PEAK, SEP_TO_PEAK, FLARE_TO_MAX, CME_TO_MAX, SEP_TO_MAX

from src.calculate_delays import calculate_flare_to_peak_delay, calculate_CME_to_peak_delay, calculate_CME_to_max_delay, calculate_flare_to_max_delay


def test_flare_to_peak_delay(df):
    '''
    Test the flare to peak delay for all events, looking at all event types if they exist.
    The flare to peak delay is defined as the time between the Flare time and the Onset peak time.
    The function checks if the calculated flare to peak delay matches the value in the dataframe.
    
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''
    k=0 #variable to count the number of values not null in all the columns '*** Flare Time to Onset (minutes)'

    #looking at all known event
    for index,row in df.iterrows():
        print(f"Testing index {index}...")

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Onset peak time exists for this event type
            if pd.notnull(row[event_type + TIME_PEAK] ) & pd.notnull(row[TIME_FLARE]):
                print(f"\t Testing event type {event_type}...")
                #Calculating the flare to peak delay (subtracting the Flare Time to the Onset peak time)
                flare_to_peak_delay_calculated=(pd.to_datetime(row[event_type + TIME_PEAK]) - pd.to_datetime(row[TIME_FLARE])).total_seconds() / 60.0
                #Checking if the calculated flare to peak delay matches the value in the dataframe
                assert np.isclose(flare_to_peak_delay_calculated, row[event_type + 'Flare Time to Onset (minutes)']), f"Flare to Onset delay test failed for index {index} and event type {event_type}"
                
                k+=1 # +1 existing and is accurate value in '*** Flare Time to Onset (minutes)'
            
            else:
                #If the Onset peak time or the Flare peak time is not defined, the delay should be NaN
                assert pd.isnull(row[event_type + FLARE_TO_PEAK]), f"Flare to Peak delay test failed for index {index} and event type {event_type}"
    print("All tests passed!")

    print(f"Number of non-null values in '*** Flare Time to Onset (minutes)': {k}")


def test_CME_to_peak_delay(df):
    '''
    Test the CME to peak delay for all events, looking at all event types if they exist.
    The CME to peak delay is defined as the time between the CME time and the Onset peak time.
    The function checks if the calculated CME to peak delay matches the value in the dataframe.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''
    
    k=0 #variable to count the number of values not null in all the columns '***CME Time to Onset (minutes)'

    #looking at all known event
    for index,row in df.iterrows():
        print(f"Testing index {index}...")

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Onset peak time exists for this event type
            if pd.notnull(row[event_type + TIME_PEAK] ) & pd.notnull(row[TIME_CME]):
                print(f"\t Testing event type {event_type}...")
                #Calculating the CME to peak delay (subtracting the CME Time to the Onset peak time)
                CME_to_peak_delay_calculated=(pd.to_datetime(row[event_type + TIME_PEAK]) - pd.to_datetime(row[TIME_CME])).total_seconds() / 60.0
                
                #Checking if the calculated CME to peak delay matches the value in the dataframe
                assert np.isclose(CME_to_peak_delay_calculated, row[event_type + 'CME Time to Onset (minutes)']), f"CME to Onset delay test failed for index {index} and event type {event_type}"
                
                k+=1 # +1 existing and is accurate value in '***CME Time to Onset (minutes)'

            else:
                #If the Onset peak time or the CME time is not defined, the delay should be NaN
                assert pd.isnull(row[event_type + CME_TO_PEAK]), f"CME to Peak delay test failed for index {index} and event type {event_type}"
    
    print("All tests passed!")
    print(f"Number of non-null values in '***CME Time to Onset (minutes)': {k}")


def test_CME_to_max_delay(df):
    '''
    Test the CME to max delay for all events, looking at all event types if they exist.
    The CME to max delay is defined as the time between the CME time and the Max flux time.
    The function checks if the calculated CME to max delay matches the value in the dataframe.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''
    
    k=0 #variable to count the number of values not null in all the columns '***CME Time to Max (minutes)'

    #looking at all known event
    for index,row in df.iterrows():
        print(f"Testing index {index}...")

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Max flux time exists for this event type
            if pd.notnull(row[event_type + TIME_MAX] ) & pd.notnull(row[TIME_CME]):
                print(f"\t Testing event type {event_type}...")
                #Calculating the CME to max delay (subtracting the CME Time to the Max flux time)
                CME_to_max_delay_calculated=(pd.to_datetime(row[event_type + TIME_MAX]) - pd.to_datetime(row[TIME_CME])).total_seconds() / 60.0
                
                #Checking if the calculated CME to max delay matches the value in the dataframe
                assert np.isclose(CME_to_max_delay_calculated, row[event_type + 'CME Time to Max (minutes)']), f"CME to Max delay test failed for index {index} and event type {event_type}"
                
                k+=1 # +1 existing and is accurate value in '***CME Time to Max (minutes)'

            else:
                #If the Max flux time or the CME time is not defined, the delay should be NaN
                assert pd.isnull(row[event_type + CME_TO_MAX]), f"CME to Max delay test failed for index {index} and event type {event_type}"
    
    print("All tests passed!")
    print(f"Number of non-null values in '***CME Time to Max (minutes)': {k}")


def test_flare_to_max_delay(df):
    '''
    Test the flare to max delay for all events, looking at all event types if they exist.
    The flare to max delay is defined as the time between the Flare time and the Max flux time.
    The function checks if the calculated flare to max delay matches the value in the dataframe.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''
    
    k=0 #variable to count the number of values not null in all the columns '*** Flare Time to Max (minutes)'

    #looking at all known event
    for index,row in df.iterrows():
        print(f"Testing index {index}...")

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Max flux time exists for this event type
            if pd.notnull(row[event_type + TIME_MAX] ) & pd.notnull(row[TIME_FLARE]):
                print(f"\t Testing event type {event_type}...")
                #Calculating the flare to max delay (subtracting the Flare Time to the Max flux time)
                flare_to_max_delay_calculated=(pd.to_datetime(row[event_type + TIME_MAX]) - pd.to_datetime(row[TIME_FLARE])).total_seconds() / 60.0
                
                #Checking if the calculated flare to max delay matches the value in the dataframe
                assert np.isclose(flare_to_max_delay_calculated, row[event_type + 'Flare Time to Max (minutes)']), f"Flare to Max delay test failed for index {index} and event type {event_type}"
                
                k+=1 # +1 existing and is accurate value in '*** Flare Time to Max (minutes)'

            else:
                #If the Max flux time or the Flare time is not defined, the delay should be NaN
                assert pd.isnull(row[event_type + FLARE_TO_MAX]), f"Flare to Max delay test failed for index {index} and event type {event_type}"
    
    print("All tests passed!")
    print(f"Number of non-null values in '*** Flare Time to Max (minutes)': {k}")


#Define the directory used
file_name='GOES_integral_PRIMARY.1986-02-03.2025-09-10_sep_events.csv'
#'GOES-06_integral_enhance_idsep.1986-01-01.1994-11-30_sep_events.csv'
file_path='Datasets/'
#'../output/opsep/GOES-06_integral_enhance_idsep/'

#Read the main SEP event file into a pandas DataFrame
df = pd.read_csv(file_path + file_name)

#Calculate all aditional columns (delays)
df=calculate_CME_to_max_delay(df)
df=calculate_flare_to_peak_delay(df)
df=calculate_CME_to_peak_delay(df)
df=calculate_flare_to_max_delay(df)

#Run all tests
test_flare_to_peak_delay(df)
test_CME_to_peak_delay(df)
test_CME_to_max_delay(df)
test_flare_to_max_delay(df)