#!/usr/bin/env python3

import pandas as pd
import numpy as np

from constants import TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100, EVENT_TYPES
from constants import EASTERN, WESTERN, TIME_FLARE, TIME_CME, TIME_PEAK, TIME_MAX, TIME_SEP



def test_rise_time_to_onset(df):
    '''
    Test the rise time to onset for all events, looking at all event types if they exist.
    The rise time to onset is defined as the time between the SEP start time and the Onset peak time.
    The function checks if the calculated rise time to onset matches the value in the dataframe.
    
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''

    #looking at all known event
    for index,row in df.iterrows():
        print(f"Testing index {index}...")

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Onset peak time exists for this event type

            if pd.notnull(row[event_type + TIME_PEAK]) & pd.notnull(row[event_type + TIME_SEP]):
                print(f"\t Testing event type {event_type}...")

                #Calculating the rise time to onset (substracting the SEP start time to the Onset peak time)
                rise_time_to_onset_calculated = (pd.to_datetime(row[event_type + TIME_PEAK]) - pd.to_datetime(row[event_type + TIME_SEP])).total_seconds() / 60.0
                
                #Checking if the calculated rise time to onset matches the value in the dataframe
                assert np.isclose(rise_time_to_onset_calculated, row[event_type + 'Rise Time to Onset (minutes)']), f"Rise time to onset test failed for index {index} and event type {event_type}"
                
    print("All tests passed!")


def print_errors_in_rise_time_to_onset(df):
    '''
    Print the errors in the rise time to onset for all events, looking at all event types if they exist.
    The rise time to onset is defined as the time between the SEP start time and the Onset peak time.
    The function checks if the calculated rise time to onset matches the value in the dataframe.
    
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''

    #looking at all known event
    for index,row in df.iterrows():
        #print(f"Testing index {index}...")

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Onset peak time exists for this event type
            if pd.notnull(row[event_type + TIME_PEAK]):
                #print(f"\t Testing event type {event_type}...")

                #Calculating the rise time to onset (subtracting the SEP start time to the Onset peak time)
                rise_time_to_onset_calculated=(pd.to_datetime(row[event_type + TIME_PEAK]) - pd.to_datetime(row[event_type + TIME_SEP])).total_seconds() / 60.0
                #Checking if the calculated rise time to onset matches the value in the dataframe
                if not np.isclose(rise_time_to_onset_calculated, row[event_type + 'Rise Time to Onset (minutes)']):
                    print(f"{row['Time Period Start']} (index={index}) : Rise time to onset test failed for event type {event_type}")
                    print(f"\t Calculated: {rise_time_to_onset_calculated} min , Expected: {row[event_type + 'Rise Time to Onset (minutes)']} min")
                    print(f"\t Rise Time :       {row[event_type + TIME_SEP]}")
                    print(f"\t Onset Peak Time : {row[event_type + TIME_PEAK]}\n")
    print("Error search completed!")


def test_rise_time_to_max(df):
    '''
    Test the rise time to max for all events, looking at all event types if they exist.
    The rise time to max is defined as the time between the SEP start time and the Max peak time.
    The function checks if the calculated rise time to max matches the value in the dataframe.
    
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''

    #looking at all known event
    for index,row in df.iterrows():
        print(f"Testing index {index}...")

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Max peak time and the SEP start time exist for this event type
            if (pd.notnull(row[event_type + TIME_MAX])) & (pd.notnull(row[event_type + TIME_SEP])):
                print(f"\t Testing event type {event_type}...")

                #Calculating the rise time to max (subtracting the SEP start time to the Max peak time)
                rise_time_to_max_calculated=(pd.to_datetime(row[event_type + TIME_MAX]) - pd.to_datetime(row[event_type + TIME_SEP])).total_seconds() / 60.0
                #Checking if the calculated rise time to max matches the value in the dataframe
                assert np.isclose(rise_time_to_max_calculated, row[event_type + 'Rise Time to Max (minutes)']), f"Rise time to max test failed for index {index} and event type {event_type}"

    print("All tests passed!")


def print_errors_in_rise_time_to_max(df):
    '''
    Print the errors in the rise time to onset for all events, looking at all event types if they exist.
    The rise time to onset is defined as the time between the SEP start time and the Onset peak time.
    The function checks if the calculated rise time to onset matches the value in the dataframe.
    
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''
    #looking at all known event
    for index,row in df.iterrows():

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the Max peak time and SEP start time exist for this event type
            if (pd.notnull(row[event_type + TIME_MAX])) & (pd.notnull(row[event_type + TIME_SEP])):

                #Calculating the rise time to max (subtracting the SEP start time to the Max peak time)
                rise_time_to_max_calculated=(pd.to_datetime(row[event_type + TIME_MAX]) - pd.to_datetime(row[event_type + TIME_SEP])).total_seconds() / 60.0
                
                #Checking if the calculated rise time to onset matches the value in the dataframe
                if not np.isclose(rise_time_to_max_calculated, row[event_type + 'Rise Time to Max (minutes)']):
                    print(f"Rise time to max test failed for index {index} and event type {event_type}")
                    print(f"\t Calculated: {rise_time_to_max_calculated}, Expected: {row[event_type + 'Rise Time to Max (minutes)']}")
    
    print("Error search completed!")


def test_longitude_range(df):
    '''
    Test the longitude range selection for all events.
    The function checks if all events in the dataframe have a longitude within [-180, 180].

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    '''
    longitude_out_of_range=False
    longitude_out_of_range_count=0

    for index,row in df.iterrows():
        print(f"Testing index {index}...")
        longitude=row['Event Longitude']
        if (longitude < -180) | (longitude > 180):
            longitude_out_of_range=True
            longitude_out_of_range_count+=1
            print(f"For index {index} the longitude is {longitude} out of range [-180; 180] ")

    assert not longitude_out_of_range, f"Longitude range test failed. Number of out of range longitudes: {longitude_out_of_range_count}"

    print("All longitudes are within the range [-180; 180]!")
