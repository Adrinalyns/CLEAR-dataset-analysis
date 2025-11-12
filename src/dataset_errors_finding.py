#!/usr/bin/env python3

import pandas as pd
import numpy as np

from constants import TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100, EVENT_TYPES
from constants import EASTERN, WESTERN, TIME_FLARE, TIME_CME, TIME_PEAK, TIME_MAX, TIME_SEP
from constants import FLARE_TO_PEAK, CME_TO_PEAK, SEP_TO_PEAK, FLARE_TO_MAX, CME_TO_MAX, SEP_TO_MAX



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


def test_positive_SEP_to_peak_delay(df):
    '''
    Test the SEP to peak delay for all events, looking at all event types if they exist.
    The SEP to peak delay is defined as the time between the SEP Start Time and the Onset peak time.
    The function verify that all SEP to peak delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    SEP start time, the Onset peak time and the calculated delay.
    '''
    allways_positive=True
    for index,row in df.iterrows():
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + SEP_TO_PEAK]) & (row[event_type + SEP_TO_PEAK]<0):
                print(f"Event index {index}, starting at {row['Time Period Start']}")
                print(f"has a negative SEP to peak delay for event type {event_type}:")
                print(f"\t SEP start time: {row[event_type + TIME_SEP]}")
                print(f"\t Onset peak time: {row[event_type + TIME_PEAK]}")
                print(f"\t Calculated delay: {row[event_type + SEP_TO_PEAK]}")
                allways_positive=False
    assert allways_positive, "Some SEP to peak delays are negative!"
    print("All SEP to peak delays are positive!")
    

def test_positive_CME_to_peak_delay(df):
    '''
    Test the CME to peak delay for all events, looking at all event types if they exist.
    The CME to peak delay is defined as the time between the CME CDAW First Look Time and the Onset peak time.
    The function verify that all CME to peak delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    CME CDAW First Look Time, the Onset peak time and the calculated delay.
    '''
    allways_positive=True
    for index,row in df.iterrows():
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + CME_TO_PEAK]) & (row[event_type + CME_TO_PEAK]<0):
                print(f"Event index {index}, starting at {row['Time Period Start']}")
                print(f"has a negative CME to peak delay for event type {event_type}:")
                print(f"\t CME CDAW First Look Time: {row[TIME_CME]}")
                print(f"\t Onset peak time: {row[event_type + TIME_PEAK]}")
                print(f"\t Calculated delay: {row[event_type + CME_TO_PEAK]}")
                allways_positive=False
    assert allways_positive, "Some CME to peak delays are negative!"
    print("All CME to peak delays are positive!")


def test_positive_Flare_to_peak_delay(df):
    '''
    Test the Flare to peak delay for all events, looking at all event types if they exist.
    The Flare to peak delay is defined as the time between the Flare Xray Peak Time and the Onset peak time.
    The function verify that all Flare to peak delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    Flare Xray Peak Time, the Onset peak time and the calculated delay.
    '''
    allways_positive=True
    for index,row in df.iterrows():
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + FLARE_TO_PEAK]) & (row[event_type + FLARE_TO_PEAK]<0):
                print(f"Event index {index}, starting at {row['Time Period Start']}")
                print(f"has a negative Flare to peak delay for event type {event_type}:")
                print(f"\t Flare Xray Peak Time: {row[TIME_FLARE]}")
                print(f"\t Onset peak time: {row[event_type + TIME_PEAK]}")
                print(f"\t Calculated delay: {row[event_type + FLARE_TO_PEAK]}")
                allways_positive=False
    assert allways_positive, "Some Flare to peak delays are negative!"
    print("All Flare to peak delays are positive!")

def test_positive_SEP_to_max_delay(df):
    '''
    Test the SEP to max delay for all events, looking at all event types if they exist.
    The SEP to max delay is defined as the time between the SEP Start Time and the Max Flux Time time.
    The function verify that all SEP to max delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    SEP start time, the Max Flux Time and the calculated delay.
    '''
    allways_positive=True
    for index,row in df.iterrows():
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + SEP_TO_MAX]) & (row[event_type + SEP_TO_MAX]<0):
                print(f"Event index {index}, starting at {row['Time Period Start']}")
                print(f"has a negative SEP to max delay for event type {event_type}:")
                print(f"\t SEP start time: {row[event_type + TIME_SEP]}")
                print(f"\t Max Flux Time: {row[event_type + TIME_MAX]}")
                print(f"\t Calculated delay: {row[event_type + SEP_TO_MAX]}")
                allways_positive=False
    assert allways_positive, "Some SEP to max delays are negative!"
    print("All SEP to max delays are positive!")
    

def test_positive_CME_to_max_delay(df):
    '''
    Test the CME to max delay for all events, looking at all event types if they exist.
    The CME to max delay is defined as the time between the CME CDAW First Look Time and the Max Flux Time time.
    The function verify that all CME to max delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    CME CDAW First Look Time, the Max Flux Time and the calculated delay.
    '''
    allways_positive=True
    for index,row in df.iterrows():
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + CME_TO_MAX]) & (row[event_type + CME_TO_MAX]<0):
                print(f"Event index {index}, starting at {row['Time Period Start']}")
                print(f"has a negative CME to max delay for event type {event_type}:")
                print(f"\t CME CDAW First Look Time: {row[TIME_CME]}")
                print(f"\t Max Flux Time: {row[event_type + TIME_MAX]}")
                print(f"\t Calculated delay: {row[event_type + CME_TO_MAX]}")
                allways_positive=False
    assert allways_positive, "Some CME to max delays are negative!"
    print("All CME to max delays are positive!")


def test_positive_Flare_to_max_delay(df):
    '''
    Test the Flare to max delay for all events, looking at all event types if they exist.
    The Flare to max delay is defined as the time between the Flare Xray Peak Time and the Max Flux Time time.
    The function verify that all Flare to max delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    Flare Xray Peak Time, the Max Flux Time and the calculated delay.
    '''
    allways_positive=True
    for index,row in df.iterrows():
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + FLARE_TO_MAX]) & (row[event_type + FLARE_TO_MAX]<0):
                print(f"Event index {index}, starting at {row['Time Period Start']}")
                print(f"has a negative Flare to max delay for event type {event_type}:")
                print(f"\t Flare Xray Peak Time: {row[TIME_FLARE]}")
                print(f"\t Max Flux Time: {row[event_type + TIME_MAX]}")
                print(f"\t Calculated delay: {row[event_type + FLARE_TO_MAX]}")
                allways_positive=False
    assert allways_positive, "Some Flare to max delays are negative!"
    print("All Flare to max delays are positive!")


