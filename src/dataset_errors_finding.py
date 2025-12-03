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


def test_positive_SEP_to_peak_delay(df,print_terminal=False):
    '''
    Test the SEP to peak delay for all events, looking at all event types if they exist.
    The SEP to peak delay is defined as the time between the SEP Start Time and the Onset peak time.
    The function verify that all SEP to peak delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    SEP start time, the Onset peak time and the calculated delay.
    '''
    #Opening the debug file to write the anomalies
    debug_file = open("debug_reports/negative_sep_to_peak_delays.txt", "w", encoding="utf-8")
    debug_file.write("Debug report of negative SEP to peak delays\n")

    always_positive=True

    for index,row in df.iterrows():
        first_error=True
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + SEP_TO_PEAK]) & (row[event_type + SEP_TO_PEAK]<0):
                
                if first_error: #Only write the event header once
                    debug_file.write(f"\nEvent index {index}, starting at {row['Time Period Start']}:\n")
                    if print_terminal:
                        print(f"\nEvent index {index}, starting at {row['Time Period Start']}:")
                    first_error = False

                #Writing the anomaly in the debug file
                debug_file.write(f"\t Event type {event_type}:\n")
                debug_file.write(f"\t \t SEP start time: {row[event_type + TIME_SEP]}\n")
                debug_file.write(f"\t \t Onset peak time: {row[event_type + TIME_PEAK]}\n")
                debug_file.write(f"\t \t Calculated delay: {row[event_type + SEP_TO_PEAK]}\n \n")

                if print_terminal: #Also print the anomaly in the terminal
                    print(f"\t negative SEP to peak delay for event type {event_type}:")
                    print(f"\t\t SEP start time: {row[event_type + TIME_SEP]}")
                    print(f"\t\t Onset peak time: {row[event_type + TIME_PEAK]}")
                    print(f"\t\t Calculated delay: {row[event_type + SEP_TO_PEAK]}\n")

                always_positive=False
        
    if always_positive:
        debug_file.write("\n \tAll CME to peak delays are positive!\n")

    debug_file.close()

    assert always_positive, "Some SEP to peak delays are negative!"
    print("All SEP to peak delays are positive!")
    

def test_positive_CME_to_peak_delay(df,print_terminal=False):
    '''
    Test the CME to peak delay for all events, looking at all event types if they exist.
    The CME to peak delay is defined as the time between the CME CDAW First Look Time and the Onset peak time.
    The function verify that all CME to peak delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    CME CDAW First Look Time, the Onset peak time and the calculated delay.
    '''
    #Opening the debug file to write the anomalies
    debug_file = open("debug_reports/negative_cme_to_peak_delays.txt", "w", encoding="utf-8")
    debug_file.write("Debug report of negative CME to peak delays\n")

    always_positive=True
    for index,row in df.iterrows():
        first_error=True

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:

            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + CME_TO_PEAK]) & (row[event_type + CME_TO_PEAK]<0):

                if first_error: #Only write the event header once
                    debug_file.write(f"\nEvent index {index}, starting at {row['Time Period Start']}:\n")
                    if print_terminal:
                        print(f"\nEvent index {index}, starting at {row['Time Period Start']}:")
                    first_error = False
                
                #Writing the anomaly in the debug file
                debug_file.write(f"\t Event type {event_type}:\n")
                debug_file.write(f"\t \t CME CDAW First Look Time: {row[TIME_CME]}\n")
                debug_file.write(f"\t \t Onset peak time: {row[event_type + TIME_PEAK]}\n")
                debug_file.write(f"\t \t Calculated delay: {row[event_type + CME_TO_PEAK]}\n \n")
                
                if print_terminal: #Also print the anomaly in the terminal
                    print(f"\t negative SEP to peak delay for event type {event_type}:")
                    print(f"\t\t SEP start time: {row[event_type + TIME_SEP]}")
                    print(f"\t\t Onset peak time: {row[event_type + TIME_PEAK]}")
                    print(f"\t\t Calculated delay: {row[event_type + SEP_TO_PEAK]}\n")
                
                always_positive=False
    
    if always_positive:
        debug_file.write("\n \tAll CME to peak delays are positive!\n")
    
    debug_file.close()

    assert always_positive, "Some CME to peak delays are negative!"
    print("All CME to peak delays are positive!")


def test_positive_Flare_to_peak_delay(df,print_terminal=False):
    '''
    Test the Flare to peak delay for all events, looking at all event types if they exist.
    The Flare to peak delay is defined as the time between the Flare Xray Peak Time and the Onset peak time.
    The function verify that all Flare to peak delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    Flare Xray Peak Time, the Onset peak time and the calculated delay.
    '''
    #Opening the debug file to write the anomalies
    debug_file = open("debug_reports/negative_flare_to_peak_delays.txt", "w", encoding="utf-8")
    debug_file.write("Debug report of negative Flare to peak delays\n")

    always_positive=True

    for index,row in df.iterrows():
        first_error=True
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + FLARE_TO_PEAK]) & (row[event_type + FLARE_TO_PEAK]<0):
                if first_error: #Only write the event header once
                    debug_file.write(f"\nEvent index {index}, starting at {row['Time Period Start']}:\n")
                    if print_terminal:
                        print(f"\nEvent index {index}, starting at {row['Time Period Start']}:")
                    first_error = False
                #Writing the anomaly in the debug file
                debug_file.write(f"\t Event type {event_type}:\n")
                debug_file.write(f"\t \t Flare Xray Peak Time: {row[TIME_FLARE]}\n")
                debug_file.write(f"\t \t Onset peak time: {row[event_type + TIME_PEAK]}\n")
                debug_file.write(f"\t \t Calculated delay: {row[event_type + FLARE_TO_PEAK]}\n \n")
                
                if print_terminal: #Also print the anomaly in the terminal
                    print(f"\t negative Flare to peak delay for event type {event_type}:")
                    print(f"\t\t Flare Xray Peak Time: {row[TIME_FLARE]}")
                    print(f"\t\t Onset peak time: {row[event_type + TIME_PEAK]}")
                    print(f"\t\t Calculated delay: {row[event_type + FLARE_TO_PEAK]}\n")
                
                always_positive=False
    
    if always_positive:
        debug_file.write("\n \tAll Flare to peak delays are positive!\n")

    debug_file.close()

    assert always_positive, "Some Flare to peak delays are negative!"
    print("All Flare to peak delays are positive!")


def test_positive_SEP_to_max_delay(df,print_terminal=False):
    '''
    Test the SEP to max delay for all events, looking at all event types if they exist.
    The SEP to max delay is defined as the time between the SEP Start Time and the Max Flux Time time.
    The function verify that all SEP to max delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    SEP start time, the Max Flux Time and the calculated delay.
    '''
    #Opening the debug file to write the anomalies
    debug_file = open("debug_reports/negative_sep_to_max_delays.txt", "w", encoding="utf-8")
    debug_file.write("Debug report of negative SEP to max delays\n")

    always_positive=True

    for index,row in df.iterrows():
        first_error=True
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + SEP_TO_MAX]) & (row[event_type + SEP_TO_MAX]<0):

                if first_error: #Only write the event header once
                    debug_file.write(f"\nEvent index {index}, starting at {row['Time Period Start']}:\n")
                    if print_terminal:
                        print(f"\nEvent index {index}, starting at {row['Time Period Start']}:")
                    first_error = False

                #Writing the anomaly in the debug file
                debug_file.write(f"\t Event type {event_type}:\n")
                debug_file.write(f"\t \t SEP start time: {row[event_type + TIME_SEP]}\n")
                debug_file.write(f"\t \t Max Flux Time: {   row[event_type + TIME_MAX]}\n")
                debug_file.write(f"\t \t Calculated delay: {row[event_type + SEP_TO_MAX]}\n \n")
                
                if print_terminal: #Also print the anomaly in the terminal
                    print(f"\thas a negative SEP to max delay for event type {event_type}:")
                    print(f"\t\tSEP start time: {row[event_type + TIME_SEP]}")
                    print(f"\t\tMax Flux Time: {row[event_type + TIME_MAX]}")
                    print(f"\t\tCalculated delay: {row[event_type + SEP_TO_MAX]}\n")
                    
                    always_positive=False

    if always_positive:
        debug_file.write("\n \tAll SEP to max delays are positive!\n")
    
    debug_file.close()

    assert always_positive, "Some SEP to max delays are negative!"
    print("All SEP to max delays are positive!")
    

def test_positive_CME_to_max_delay(df,print_terminal=False):
    '''
    Test the CME to max delay for all events, looking at all event types if they exist.
    The CME to max delay is defined as the time between the CME CDAW First Look Time and the Max Flux Time time.
    The function verify that all CME to max delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    CME CDAW First Look Time, the Max Flux Time and the calculated delay.
    '''
    debug_file = open("debug_reports/negative_cme_to_max_delays.txt", "w", encoding="utf-8")
    debug_file.write("Debug report of negative CME to max delays\n")

    always_positive=True

    for index,row in df.iterrows():
        first_error=True
        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + CME_TO_MAX]) & (row[event_type + CME_TO_MAX]<0):

                if first_error: #Only write the event header once
                    debug_file.write(f"\nEvent index {index}, starting at {row['Time Period Start']}:\n")
                    if print_terminal:
                        print(f"\nEvent index {index}, starting at {row['Time Period Start']}:")
                    first_error = False

                #Writing the anomaly in the debug file
                debug_file.write(f"\t Event type {event_type}:\n")         
                debug_file.write(f"\t \t CME CDAW First Look Time: {row[TIME_CME]}\n")
                debug_file.write(f"\t \t Max Flux Time: {row[event_type + TIME_MAX]}\n")
                debug_file.write(f"\t \t Calculated delay: {row[event_type + CME_TO_MAX]}\n \n")
                
                if print_terminal: #Also print the anomaly in the terminal
                    print(f"\thas a negative CME to max delay for event type {event_type}:")
                    print(f"\t\tCME CDAW First Look Time: {row[TIME_CME]}")
                    print(f"\t\tMax Flux Time: {row[event_type + TIME_MAX]}")
                    print(f"\t\tCalculated delay: {row[event_type + CME_TO_MAX]}\n")

                always_positive=False

    if always_positive:
        debug_file.write("\n \tAll CME to max delays are positive!\n")
    
    debug_file.close()

    assert always_positive, "Some CME to max delays are negative!"
    print("All CME to max delays are positive!")


def test_positive_Flare_to_max_delay(df,print_terminal=False):
    '''
    Test the Flare to max delay for all events, looking at all event types if they exist.
    The Flare to max delay is defined as the time between the Flare Xray Peak Time and the Max Flux Time time.
    The function verify that all Flare to max delays are positive.
    If not it prints a message with the index and event type of the negative delays, as well as the 
    Flare Xray Peak Time, the Max Flux Time and the calculated delay.
    '''
    debug_file = open("debug_reports/negative_flare_to_max_delays.txt", "w", encoding="utf-8")
    debug_file.write("Debug report of negative Flare to max delays\n")

    always_positive=True

    for index,row in df.iterrows():
        first_error=True

        #looking at all integral flux/event types
        for event_type in EVENT_TYPES:
            #Verifying that the delay exists for this event type
            if pd.notnull(row[event_type + FLARE_TO_MAX]) & (row[event_type + FLARE_TO_MAX]<0):

                if first_error: #Only write the event header once
                    debug_file.write(f"\nEvent index {index}, starting at {row['Time Period Start']}:\n")
                    if print_terminal:
                        print(f"\nEvent index {index}, starting at {row['Time Period Start']}:")
                    first_error = False
                
                #Writing the anomaly in the debug file
                debug_file.write(f"\t Event type {event_type}:\n")
                debug_file.write(f"\t \t Flare Xray Peak Time: {row[TIME_FLARE]}\n")
                debug_file.write(f"\t \t Max Flux Time: {row[event_type + TIME_MAX]}\n")
                debug_file.write(f"\t \t Calculated delay: {row[event_type + FLARE_TO_MAX]}\n \n")
                
                if print_terminal: #Also print the anomaly in the terminal
                    print(f"\thas a negative Flare to max delay for event type {event_type}:")
                    print(f"\t\tFlare Xray Peak Time: {row[TIME_FLARE]}")
                    print(f"\t\tMax Flux Time: {row[event_type + TIME_MAX]}")
                    print(f"\t\tCalculated delay: {row[event_type + FLARE_TO_MAX]}\n")

                always_positive=False
    
    if always_positive:
        debug_file.write("\n \tAll Flare to max delays are positive!\n")

    debug_file.close()

    assert always_positive, "Some Flare to max delays are negative!"
    print("All Flare to max delays are positive!")


def print_value_for_each_event_type(df,column_name):
    '''
    Print the values of a given column for each event type in all events.
    
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    column_name : str
        the name of the column to test
    '''
    for index,row in df.iterrows():
        print(f"Testing index {index}...")
        values=[]
        for event_type in EVENT_TYPES:
            #if pd.notnull(row[event_type + column_name]):
            values.append(row[event_type + column_name])
        print(f'{values[0]}, {values[4]}, \n{values[1]}, {values[5]}, \n{values[2]}, {values[6]}, \n{values[3]}, {values[7]}')
        #assert len(values)<=1, f"Column {column_name} has different values for event index {index}: {values}"


def print_differences_btwn_TC_AB(df,column_name):
    '''
    Print when a given "column"/value has different values for TC and AB event types in all events.
    
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    column_name : str
        the name of the column to test
    '''
    for index,row in df.iterrows():
        print(f"Testing index {index}...")
        values=[]
        if (row[TC_10 + column_name] != row[AB_10 + column_name]) & (pd.notnull(row[TC_10 + column_name]) | pd.notnull(row[AB_10 + column_name])):
            print(f"\t10 MeV : {row[TC_10 + column_name]} vs {row[AB_10 + column_name]}")
        if (row[TC_30 + column_name] != row[AB_30 + column_name]) & (pd.notnull(row[TC_30 + column_name]) | pd.notnull(row[AB_30 + column_name])):
            print(f"\t30 MeV : {row[TC_30 + column_name]} vs {row[AB_30 + column_name]}")
        if (row[TC_50 + column_name] != row[AB_50 + column_name]) & (pd.notnull(row[TC_50 + column_name]) | pd.notnull(row[AB_50 + column_name])):
            print(f"\t50 MeV : {row[TC_50 + column_name]} vs {row[AB_50 + column_name]}")
        if (row[TC_100 + column_name] != row[AB_100 + column_name]) & (pd.notnull(row[TC_100 + column_name]) | pd.notnull(row[AB_100 + column_name])):
            print(f"\t100 MeV : {row[TC_100 + column_name]} vs {row[AB_100 + column_name]}")
        #assert len(values)<=1, f"Column {column_name} has different values for event index {index}: {values}"


def test_in_progress(df):

    from work import plot_flux_time_series
    
    #investigation on the falre_to_max and cme_to_max negative delays
    #Why sep_to_max > 0
    #2,6,14,27,27,27,38,81,122,129,164,
    indexes=[172,193,197,197,236,237,248,250,253,266,275,275,277,280,284,292,292]
    event_type = [TC_50,TC_10,TC_10,TC_30,TC_100,TC_30,TC_50,TC_100,TC_10,TC_10,TC_10,TC_30,TC_30,TC_10,TC_10,TC_10,TC_30]
    #1-11 : GOES-6
    #12-170 : GOES-7
    #171-308 : GOES-8
    #309-357 : GOES-11
    

    for nb, index in enumerate(indexes):
        print(f"Testing index {index}...")
        row=df.iloc[index]
        flux_type = event_type[nb]
        print(f"\tflux : {flux_type}")
        print(f"\t file {row[flux_type + 'Flux Time Series']}:")
        print(f"\t \t SEP start time: {row[flux_type + TIME_SEP]}")
        print(f"\t \t Onset peak time: {row[flux_type + TIME_PEAK]}")
        plot_flux_time_series('../output/opsep/GOES-08_integral_enhance_idsep/',row,flux_type)
        #print(f"\t \t Max Flux Time: {   row[TC_100 + TIME_MAX]}")
        #print(f"\t \t Flare Xray Peak Time: {row[TIME_FLARE]}")
        #print(f"\t \t CME CDAW First Look Time: {row[TIME_CME]}")