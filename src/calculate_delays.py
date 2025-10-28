#!/usr/bin/env python3

import pandas as pd

from constants import TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100, EVENT_TYPES
from constants import TIME_FLARE, TIME_CME, TIME_PEAK, TIME_MAX, TIME_SEP
from constants import FLARE_TO_PEAK, CME_TO_PEAK, SEP_TO_PEAK, FLARE_TO_MAX, CME_TO_MAX, SEP_TO_MAX


def calculate_flare_to_max_delay(df):
    '''
    This function compute the delay between the Flare time and the Max Flux time for each event in the dataframe.
    It calculates the delay only if the Max Flux time and the Flare time are defined.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with an additional column 'Flare Time to Max (minutes)' containing the delay in minutes
    '''
    for event_type in EVENT_TYPES:
        df[event_type + FLARE_TO_MAX] = (pd.to_datetime(df[event_type + TIME_MAX]) - pd.to_datetime(df[TIME_FLARE])).dt.total_seconds() / 60.0

    return df

def calculate_CME_to_max_delay(df):
    '''
    This function compute the delay between the CME time and the Max Flux time for each event in the dataframe.
    It calculates the delay only if the Max Flux time and the CME time are defined.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with an additional column 'CME Time to Max (minutes)' containing the delay in minutes
    '''
    for event_type in EVENT_TYPES:
        df[event_type + CME_TO_MAX] = (pd.to_datetime(df[event_type + TIME_MAX]) - pd.to_datetime(df[TIME_CME])).dt.total_seconds() / 60.0

    return df

def calculate_CME_to_peak_delay(df):
    '''
    This function compute the delay between the CME time and the Onset Peak time for each event in the dataframe.
    It calculates the delay only if the Onset Peak time and the CME time are defined.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with an additional column 'CME Time to Onset (minutes)' containing the delay in minutes
    '''
    for event_type in EVENT_TYPES:
        df[event_type + CME_TO_PEAK] = (pd.to_datetime(df[event_type + TIME_PEAK]) - pd.to_datetime(df[TIME_CME])).dt.total_seconds() / 60.0

    return df

def calculate_flare_to_peak_delay(df):
    '''
    This function compute the delay between the Flare time and the Onset Peak time for each event in the dataframe.
    It calculates the delay only if the Onset Peak time and the Flare time are defined.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with an additional column 'Flare Time to Onset (minutes)' containing the delay in minutes
    '''
    for event_type in EVENT_TYPES:
        df[event_type + FLARE_TO_PEAK] = (pd.to_datetime(df[event_type + TIME_PEAK]) - pd.to_datetime(df[TIME_FLARE])).dt.total_seconds() / 60.0

    return df