#!/usr/bin/env python3

import pandas as pd
import numpy as np

from constants import TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100, EVENT_TYPES
from constants import TIME_FLARE, TIME_CME, TIME_PEAK, TIME_MAX, TIME_SEP
from constants import FLARE_TO_PEAK, CME_TO_PEAK, SEP_TO_PEAK, FLARE_TO_MAX, CME_TO_MAX, SEP_TO_MAX


def calculate_flare_to_max_delay(df):
    '''
    This function compute the delay between the Flare time and the Max Flux time for each event in the dataframe.
    It calculates the delay only if the Max Flux time and the Flare time are defined.
    It only calculate the delay for real events ie event whose TIME_SEP is defined.

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
        df[event_type + FLARE_TO_MAX] = np.nan  # Initialize the column with NaN values
        df.loc[ df[event_type + TIME_SEP].notnull(), event_type + FLARE_TO_MAX] = \
            (pd.to_datetime(df[event_type + TIME_MAX]) - pd.to_datetime(df[TIME_FLARE])).dt.total_seconds() / 60.0

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
        df[event_type + CME_TO_MAX] = np.nan  # Initialize the column with NaN values
        df.loc[ df[event_type + TIME_SEP].notnull(), event_type + CME_TO_MAX] = \
            (pd.to_datetime(df[event_type + TIME_MAX]) - pd.to_datetime(df[TIME_CME])).dt.total_seconds() / 60.0
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
        df[event_type + CME_TO_PEAK] = np.nan  # Initialize the column with NaN values
        df.loc[ df[event_type + TIME_SEP].notnull(), event_type + CME_TO_PEAK] = \
            (pd.to_datetime(df[event_type + TIME_PEAK]) - pd.to_datetime(df[TIME_CME])).dt.total_seconds() / 60.0
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
        df[event_type + FLARE_TO_PEAK] = np.nan  # Initialize the column with NaN values
        df.loc[ df[event_type + TIME_SEP].notnull(), event_type + FLARE_TO_PEAK] = \
            (pd.to_datetime(df[event_type + TIME_PEAK]) - pd.to_datetime(df[TIME_FLARE])).dt.total_seconds() / 60.0
    return df


def corrects_sep_to_max_delay(df):
    '''
    This function compute the rise time to onset for each event in the dataframe. 
    The rise time column already exists but contains errors.
    The rise time to max is defined as the time between the SEP start time and the Max flux time.
    It calculates the rise time to max only if the Max flux time and the SEP start time are defined.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with the corrected column 'Rise Time to Max (minutes)' containing the rise time to max in minutes
    '''
    for event_type in EVENT_TYPES:
        df[event_type + SEP_TO_MAX] = (pd.to_datetime(df[event_type + TIME_MAX]) - pd.to_datetime(df[event_type + TIME_SEP])).dt.total_seconds() / 60.0
    return df


def corrects_sep_to_peak_delay(df):
    '''
    This function compute the rise time to onset for each event in the dataframe. 
    The rise time column already exists but contains errors.
    The rise time to onset is defined as the time between the SEP start time and the Onset peak time.
    It calculates the rise time to onset only if the Onset peak time and the SEP start time are defined.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    Returns:
    --------
    df : pandas DataFrame
        The dataframe with the corrected column 'Rise Time to Onset (minutes)' containing the rise time to onset in minutes
    '''
    for event_type in EVENT_TYPES:
        df[event_type + SEP_TO_PEAK] = (pd.to_datetime(df[event_type + TIME_PEAK]) - pd.to_datetime(df[event_type + TIME_SEP])).dt.total_seconds() / 60.0

    return df


