#!/usr/bin/env python3
'''
This code allow to read the SEP_event files of the CLEAR dataset

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
import os
import matplotlib.pyplot as plt
import numpy as np

from conversion import convert_column_to_numeric, convert_column_to_date

from constants import TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100, EVENT_TYPES
from constants import EASTERN, WESTERN, TIME_FLARE, TIME_CME, TIME_PEAK, TIME_MAX, TIME_SEP
from constants import FLARE_TO_PEAK, CME_TO_PEAK, SEP_TO_PEAK, FLARE_TO_MAX, CME_TO_MAX, SEP_TO_MAX

from dataset_errors_finding import test_rise_time_to_onset, print_errors_in_rise_time_to_onset
from dataset_errors_finding import test_rise_time_to_max, print_errors_in_rise_time_to_max
from dataset_errors_finding import test_longitude_range

from calculate_delays import calculate_flare_to_peak_delay, calculate_CME_to_peak_delay, corrects_sep_to_peak_delay
from calculate_delays import calculate_CME_to_max_delay, calculate_flare_to_max_delay, corrects_sep_to_max_delay
plt.style.use('seaborn-v0_8-darkgrid')


def plot_flux_time_series(file_path,event,event_type):
    '''
    Plot the flux time series from a given file path.
    The file is expected to have two columns: Time and Value, separated by whitespace. 
    It will be imported into a pandas DataFrame.
    The Time column is converted to datetime format, and the Value column is plotted on a logarithmic scale.

    Parameters:
    -----------
    file_path : string
        the path to the directory containing the flux time series file
    event : panda Series
        a row from the dataframe containing all event information
    event_type : string
        the type of differential flux to plot for this event (eg '>10.0 MeV 10.0 pfu')

    Returns:
    --------
    fig,ax : the figure and axis object of the plot
    '''

    #Define which file to open to get the flux time series of the event
    name_flux_time_series=file_path + event[event_type + 'Flux Time Series']

    #Read the file into a pandas DataFrame
    df_plot = pd.read_csv(name_flux_time_series, delim_whitespace=True, names=["Time", "Flux"])
    
    #Convert the Time column to datetime format
    df_plot["Time"] = pd.to_datetime(df_plot["Time"])

    #Plot the flux versus time on a logarithmic scale for the flux
    fig,ax=plt.subplots(1,1,figsize=(10,6))
    ax.plot(df_plot["Time"], df_plot["Flux"], marker='o', linestyle='-')
    ax.set_yscale('log')
    ax.set_xlabel('Time (Date)')
    ax.set_ylabel('Flux (pfu)')
    ax.set_title(f'Event nb {event.name} \nDifferential Flux:\n{event_type}')
    ax.grid(True, which="both", ls="--")

    #Plot the max peak and onset peak

    if pd.notnull(event[event_type + 'Max Flux Time']):
        Max_flux_time=pd.to_datetime(event[event_type + 'Max Flux Time'])
        Max_flux=(event[event_type + 'Max Flux (pfu)'])
        ax.axvline(Max_flux_time, color='red', linestyle='--', label='Max Flux Time')
        ax.plot(Max_flux_time, Max_flux, 'ro',markersize=10)  # Mark the max flux point

    if pd.notnull(event[event_type + 'Onset Peak Time']):
        Onset_peak_time=pd.to_datetime(event[event_type + 'Onset Peak Time'])
        Onset_peak_flux=(event[event_type + 'Onset Peak (pfu)'])
        ax.axvline(Onset_peak_time, color='orange', linestyle='--', label='Onset Peak Time')
        ax.plot(Onset_peak_time, Onset_peak_flux, 'o', color='orange', markersize=10)  # Mark the onset peak point
        
    if pd.notnull(event[event_type + 'SEP Start Time']):
        SEP_start_time=pd.to_datetime(event[event_type + 'SEP Start Time'])
        ax.axvline(SEP_start_time, color='green', linestyle='--', label='SEP Start Time')

    if pd.notnull(event[TIME_FLARE]):
        Flare_time=pd.to_datetime(event[TIME_FLARE])
        ax.axvline(Flare_time, color='yellow', linestyle='--', label='Flare Xray Peak Time')
    
    if pd.notnull(event[TIME_CME]):
        CME_time=pd.to_datetime(event[TIME_CME])
        ax.axvline(CME_time, color='purple', linestyle='--', label='CME CDAW First Look Time')
    
    ax.legend()
    plt.show()

    return fig,ax


def subset_selection(df,event_type=None,Event_longitude=None,Flare_magnitude=None,CDAW_speed=None,DONKI_speed=None):
    '''
    This function return a subset of SEP event data frame according to the selection criteria.
    All the criteria are default to None, meaning no selection on that criteria.
    The function will filter the dataframe for all criteria specified.

    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information

    event_type : string, default to None
        The type of event (Threshold Crossing, Above Background, and the differential flux studied)
        Use the constants defined above (eg TC_10, AB_10...)

    Event_longitude : (float,float), default to None
        The minimum and maximum longitude of the events to consider (in degrees)

    Flare_magnitude : string, default to None
        The minimum flare magnitude of the SEP. M-class : flare magnitude >= 1e-5 (W/m^2)

    CDAW_speed : float, default to None
        The minimum speed of the CME from the CDAW catalog (km/s)

    DONKI_speed : float, default to None
        The minimum speed of the CME from the DONKI catalog (km/s)

    Returns:
    --------
    df : pandas DataFrame
        The filtered dataframe according to the selection criteria
    '''

    if event_type is not None:
        df = df.loc[df[event_type + 'SEP Start Time'].notnull()]
    
    #I considered only the events with a known longitude that respect the criteria
    if Event_longitude is not None:
        df = df.loc[(df['Event Longitude'] >= Event_longitude[0]) & (df['Event Longitude'] <= Event_longitude[1])]

    #I considered only the events with a known magnitude that respect the criteria
    #there is no need to add the '.notnull()' condition, as NaN values are not >= Flare_magnitude
    #I added it for clarity, and I may remove it to speed up the code
    if Flare_magnitude is not None:
        df = df.loc[df['Flare Magnitude'].notnull() & (df['Flare Magnitude'] >= Flare_magnitude)]

    #I considered only the events with a known CDAW speed that respect the criteria
    #there is no need to add the '.notnull()' condition, as NaN values are not >= CDAW_speed
    #I added it for clarity, and I may remove it to speed up the code
    if CDAW_speed is not None:
        df = df.loc[df['CDAW CME Speed'].notnull() & (df['CDAW CME Speed'] >= CDAW_speed)]
    
    #I considered only the events with a known DONKI speed that respect the criteria
    #there is no need to add the '.notnull()' condition, as NaN values are not >= DONKI_speed
    #I added it for clarity, and I may remove it to speed up the code
    if DONKI_speed is not None:
        df = df.loc[df['DONKI CME Speed'].notnull() & (df['DONKI CME Speed'] >= DONKI_speed)]

    return df


def test_subset_selection(df,all=0):
    '''
    Test the function subset_selection to ensure it works as expected.
    Parameters:
    -----------
    df : panda DataFrame
        the initial dataframe containing all event information
    all : boolean, default to 0
        If all=1, run all the tests, otherwise only run a subset of the tests
    '''
    df_TC_10 = df.loc[df[TC_10 + 'SEP Start Time'].notnull()]
    df_AB_10 = df.loc[df[AB_10 + 'SEP Start Time'].notnull()]
    df_TC_30 = df.loc[df[TC_30 + 'SEP Start Time'].notnull()]
    df_AB_30 = df.loc[df[AB_30 + 'SEP Start Time'].notnull()]
    df_TC_50 = df.loc[df[TC_50 + 'SEP Start Time'].notnull()]
    df_AB_50 = df.loc[df[AB_50 + 'SEP Start Time'].notnull()]
    df_TC_100 = df.loc[df[TC_100 + 'SEP Start Time'].notnull()]
    df_AB_100 = df.loc[df[AB_100 + 'SEP Start Time'].notnull()]

    if all:
        print("Running all tests...\n")
        print(f'\t Running test for event type selection...\n')
        #Test 1: No selection criteria, should return the original dataframe
        df_test = subset_selection(df)
        assert df_test.equals(df), "The DataFrame should be unchanged when no criteria are provided"

        #Test 2: Select events with TC_10 event type
        df_test = subset_selection(df, event_type=TC_10)
        assert df_test.equals(df_TC_10), "The DataFrame was not filtered correctly for TC_10 event type"

        #Test 3: Select events with TC_30 event type
        df_test = subset_selection(df, event_type=TC_30)
        assert df_test.equals(df_TC_30), "The DataFrame was not filtered correctly for TC_30 event type"

        #Test 4: Select events with TC_50 event type
        df_test = subset_selection(df, event_type=TC_50)
        assert df_test.equals(df_TC_50), "The DataFrame was not filtered correctly for TC_50 event type"

        #Test 5: Select events with TC_100 event type
        df_test = subset_selection(df, event_type=TC_100)
        assert df_test.equals(df_TC_100), "The DataFrame was not filtered correctly for TC_100 event type"

        #Test 6: Select events with AB_10 event type
        df_test = subset_selection(df, event_type=AB_10)
        assert df_test.equals(df_AB_10), "The DataFrame was not filtered correctly for AB_10 event type"

        #Test 7: Select events with AB_30 event type
        df_test = subset_selection(df, event_type=AB_30)
        assert df_test.equals(df_AB_30), "The DataFrame was not filtered correctly for AB_30 event type"

        #Test 8: Select events with AB_50 event type
        df_test = subset_selection(df, event_type=AB_50)
        assert df_test.equals(df_AB_50), "The DataFrame was not filtered correctly for AB_50 event type"

        #Test 9: Select events with AB_100 event type
        df_test = subset_selection(df, event_type=AB_100)
        assert df_test.equals(df_AB_100), "The DataFrame was not filtered correctly for AB_100 event type"

        print(f'\t Running test for longitude selection...\n')
        #Test 10: Select Event with a longitude >=0
        df_test = subset_selection(df, Event_longitude=WESTERN)
        df_expected = df.loc[df['Event Longitude'] >= 0]
        assert df_test.equals(df_expected), "The Dataframe was not filtered correctly Event_longitude >= 0"

        #Test 11: Select Event with a longitude <=0
        df_test = subset_selection(df, Event_longitude=EASTERN)
        df_expected = df.loc[df['Event Longitude'] <= 0]
        assert df_test.equals(df_expected), "The Dataframe was not filtered correctly Event_longitude <= 0"

        print(f'\t Running test for Flare Magnitude selection...\n')
        #Test 12: Select Flare_magnitude >= 1e-5
        df_test = subset_selection(df, Flare_magnitude=1e-5)
        df_expected = df.loc[df['Flare Magnitude'] >= 1e-5]
        assert df_test.equals(df_expected), "The Dataframe was not sorted correctly for Flare_magnitude >= 1e-5"

        print(f'\t Running test for CME CDAW Speed selection...\n')
        #Test 13: Select events with CDAW_speed >= 500
        df_test = subset_selection(df,CDAW_speed=500)
        df_expected = df.loc[(df['CDAW CME Speed'] >= 500)]
        assert df_test.equals(df_expected), "The Dataframe was not filtered correctly for CDAW_speed >= 500"
        
        print(f'\t Running test for CME DONKI Speed selection...\n')
        #Test 14: Select events with DONKI_speed >= 800
        df_test = subset_selection(df,DONKI_speed=800)
        df_expected = df.loc[(df['DONKI CME Speed'] >= 800)]
        assert df_test.equals(df_expected), "The Dataframe was not filtered correctly for DONKI_speed >= 800"

        print("All tests passed!")
    else:
        print("Running test for a combination of selections...\n")
        #Test: Select events with AB_50 event type, Event_longitude >= 10, Flare_magnitude >= 1e-5, CDAW_speed >= 800
        df_test = subset_selection(df, event_type=AB_50, Event_longitude=EASTERN, Flare_magnitude=1e-5, CDAW_speed=500, DONKI_speed=800)
        df_expected = df_AB_50.loc[(df_AB_50['Event Longitude'] <= 0) & (df_AB_50['Flare Magnitude'] >= 1e-5) & (df_AB_50['CDAW CME Speed'] >= 500) & (df_AB_50['DONKI CME Speed'] >= 800)]
        assert df_test.equals(df_expected), "Test Failed"
        print("Test passed!")


def prepare_dataframe():
    '''
    This function prepare the dataframe by reading the SEP event file,
    converting relevant columns to the correct data type,
    and calculating all additional columns (delays).

    Returns:
    --------
    df : pandas DataFrame
        The prepared dataframe containing all event information
    '''
    #Define the directory used
    file_name='GOES_integral_PRIMARY.1986-02-03.2025-09-10_sep_events.csv'
    #'GOES-06_integral_enhance_idsep.1986-01-01.1994-11-30_sep_events.csv'
    file_path='Datasets/'
    #'../output/opsep/GOES-06_integral_enhance_idsep/'

    #Read the main SEP event file into a pandas DataFrame
    df = pd.read_csv(file_path + file_name)
    df=df.iloc[:-1] #removing the last row because its longitude is out of range [-180;180]

    #Convert relevant columns to the correct data type
    df=convert_column_to_date(df,'Time Period Start',notify_changes=True)

    df=convert_column_to_numeric(df,'Flare Magnitude',notify_changes=True)
    df=convert_column_to_numeric(df,'CDAW CME Speed',notify_changes=True)
    df=convert_column_to_numeric(df,'DONKI CME Speed',notify_changes=True)
    df=convert_column_to_numeric(df,'Event Longitude',notify_changes=True)

    df=convert_column_to_date(df,TIME_FLARE,notify_changes=True)
    df=convert_column_to_date(df,TIME_CME,notify_changes=True)

    for event_type in EVENT_TYPES:
        df=convert_column_to_date(df,event_type + TIME_SEP,notify_changes=True)
        df=convert_column_to_date(df,event_type + TIME_PEAK,notify_changes=True)
        df=convert_column_to_date(df,event_type + TIME_MAX,notify_changes=True)

    #Calculate all aditional columns (delays)
    df=calculate_CME_to_max_delay(df)
    df=calculate_flare_to_max_delay(df)
    df=calculate_flare_to_peak_delay(df)
    df=calculate_CME_to_peak_delay(df)
    
    #Correcting the SEP to peak and SEP to max delay columns if they exist
    df=corrects_sep_to_max_delay(df)
    df=corrects_sep_to_peak_delay(df)
    
    return df
 

def load_generate_dataset(force=False):
    """
    This function either loads an existing dataset from a pickle file
    or generates a new dataset by calling the prepare_dataframe function.
    If the dataset is generated, it is saved to a pickle file for future use, 
    so that it doesn't need to be regenerated each time.
    """
    DATA_PATH = "Datasets/my_dataset.pkl" 
    if not force and os.path.exists(DATA_PATH):
        print("Loading the existing dataset...")
        return pd.read_pickle(DATA_PATH)
    else:
        print("Generating the dataset...")
        df = prepare_dataframe()
        df.to_pickle(DATA_PATH)
        print("Dataset saved in", DATA_PATH)
        return df


def histogram_of_delays_max(df,event_type,Event_longitude=None,Flare_magnitude=None,CDAW_speed=None,DONKI_speed=None,debug=False):
    '''
    This function plot the histogram of the delays (CME to Max, Flare to Max, SEP to Max)
    for a subset of events selected according to the selection criteria.
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    event_type : string
        The type of event (Threshold Crossing, Above Background, and the differential flux studied).
        Use the constants defined above (eg TC_10, AB_10...)
    Event_longitude : (float,float), default to None
        The minimum and maximum longitude of the events to consider (in degrees)
    Flare_magnitude : string, default to None
        The minimum flare magnitude of the SEP. M-class : flare magnitude >= 1e-5 (W/m^2)
    CDAW_speed : float, default to None
        The minimum speed of the CME from the CDAW catalog (km/s)
    DONKI_speed : float, default to None
        The minimum speed of the CME from the DONKI catalog (km/s)
    '''
    #Selecting the subset of events according to the selection criteria
    df_subset=subset_selection(df, event_type=event_type, Event_longitude=Event_longitude, Flare_magnitude=Flare_magnitude, CDAW_speed=CDAW_speed, DONKI_speed=DONKI_speed)
    print(df_subset.shape) #to see how many events are in the subset, if there is enough data
    #Get the delays for the selected subset of events and convert them to hours
    CME_to_max_delays=df_subset[event_type + CME_TO_MAX].dropna().values/60.0 #in hours
    Flare_to_max_delays=df_subset[event_type + FLARE_TO_MAX].dropna().values/60.0 #in hours
    SEP_to_max_delays=df_subset[event_type + SEP_TO_MAX].dropna().values/60.0 #in hours

    #Plot the histogram of the CME to Max delays for the selected subset of events
    fig,ax=plt.subplots(1,1,figsize=(10,6))

    counts, bins = np.histogram(CME_to_max_delays, bins=30)
    ax.stairs(counts, bins, label=' CME to Max Delay')
    counts, bins = np.histogram(Flare_to_max_delays, bins=30)
    ax.stairs(counts, bins, label=' Flare to Max Delay')
    counts, bins = np.histogram(SEP_to_max_delays, bins=30)
    ax.stairs(counts, bins, label=' SEP to Max Delay')

    #Create the title based on the selection criteria
    title=f'Histogram of Delays for {event_type}, '
    if Event_longitude is not None:
        title+=f'longitude {Event_longitude}, '
    if Flare_magnitude is not None:
        title+=f'Flare magnitude >= {Flare_magnitude}, '
    if CDAW_speed is not None:
        title+=f'CDAW speed >= {CDAW_speed} km/s, '
    if DONKI_speed is not None:
        title+=f'DONKI speed >= {DONKI_speed} km/s, '
    
    ax.set_xlabel('CME to Max Delay (hours)')
    ax.set_ylabel('Number of Events')
    ax.set_title(title)
    plt.show()
    plt.legend()

    if debug:
        print("CME to peak delays < 0:")
        print(CME_to_max_delays[CME_to_max_delays<0])
        print("Flare to peak delays < 0:")
        print(Flare_to_max_delays[Flare_to_max_delays<0])
        print("SEP to peak delays < 0:")
        print(SEP_to_max_delays[SEP_to_max_delays<0])
    


def histogram_of_delays_peak(df,event_type,Event_longitude=None,Flare_magnitude=None,CDAW_speed=None,DONKI_speed=None,debug=False):
    '''
    This function plot the histogram of the delays (CME to Peak, Flare to Peak, SEP to Peak)
    for a subset of events selected according to the selection criteria.
    Parameters:
    -----------
    df : panda DataFrame
        the dataframe containing all event information
    event_type : string
        The type of event (Threshold Crossing, Above Background, and the differential flux studied).
        Use the constants defined above (eg TC_10, AB_10...)
    Event_longitude : (float,float), default to None
        The minimum and maximum longitude of the events to consider (in degrees)
    Flare_magnitude : string, default to None
        The minimum flare magnitude of the SEP. M-class : flare magnitude >= 1e-5 (W/m^2)
    CDAW_speed : float, default to None
        The minimum speed of the CME from the CDAW catalog (km/s)
    DONKI_speed : float, default to None
        The minimum speed of the CME from the DONKI catalog (km/s)
    '''
    #Selecting the subset of events according to the selection criteria
    df_subset=subset_selection(df, event_type=event_type, Event_longitude=Event_longitude, Flare_magnitude=Flare_magnitude, CDAW_speed=CDAW_speed, DONKI_speed=DONKI_speed)
    print(df_subset.shape) #to see how many events are in the subset, if there is enough data

    #Get the delays for the selected subset of events and convert them to hours
    CME_to_peak_delays=df_subset[event_type + CME_TO_PEAK].dropna().values/60.0 #in hours
    Flare_to_peak_delays=df_subset[event_type + FLARE_TO_PEAK].dropna().values/60.0 #in hours
    SEP_to_peak_delays=df_subset[event_type + SEP_TO_PEAK].dropna().values/60.0 #in hours

    #Plot the histogram of the CME to Peak delays for the selected subset of events
    fig,ax=plt.subplots(1,1,figsize=(10,6))

    counts, bins = np.histogram(CME_to_peak_delays, bins=30)
    ax.stairs(counts, bins, label=' CME to Peak Delay')
    counts, bins = np.histogram(Flare_to_peak_delays, bins=30)
    ax.stairs(counts, bins, label=' Flare to Peak Delay')
    counts, bins = np.histogram(SEP_to_peak_delays, bins=30)
    ax.stairs(counts, bins, label=' SEP to Peak Delay')

    #Create the title based on the selection criteria
    title=f'Histogram of Delays for {event_type}, '
    if Event_longitude is not None:
        title+=f'longitude {Event_longitude}, '
    if Flare_magnitude is not None:
        title+=f'Flare magnitude >= {Flare_magnitude}, '
    if CDAW_speed is not None:
        title+=f'CDAW speed >= {CDAW_speed} km/s, '
    if DONKI_speed is not None:
        title+=f'DONKI speed >= {DONKI_speed} km/s, '
    
    ax.set_xlabel('CME to Max Delay (hours)')
    ax.set_ylabel('Number of Events')
    ax.set_title(title)
    plt.show()
    plt.legend()

    if debug:
        print("CME to peak delays < 0:")
        print(CME_to_peak_delays[CME_to_peak_delays<0])
        print("Flare to peak delays < 0:")
        print(Flare_to_peak_delays[Flare_to_peak_delays<0])
        print("SEP to peak delays < 0:")
        print(SEP_to_peak_delays[SEP_to_peak_delays<0])



df=load_generate_dataset()

def main():
    histogram_of_delays_max(df,TC_10,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)
    histogram_of_delays_max(df,TC_30,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)
    histogram_of_delays_max(df,TC_50,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)
    histogram_of_delays_max(df,TC_100,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)

    histogram_of_delays_peak(df,TC_10,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)
    histogram_of_delays_peak(df,TC_30,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)
    histogram_of_delays_peak(df,TC_50,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)
    histogram_of_delays_peak(df,TC_100,Event_longitude=WESTERN,Flare_magnitude=1e-5,debug=True)



'''
#Example to verify that the max flux is defined for all event types, even when the threshold is not reached
for index,row in df.iterrows():
    for event in EVENT_TYPES:
        print(index,row[event+'Flux Time Series'],row[event + 'Max Flux Time'], row[event + 'Max Flux (pfu)'])


#Example used to understand when TIME_PEAK, TIME_MAX, TIME_SEP are defined:
for index,row in df.iterrows():
    for event in EVENT_TYPES:
        print(index,row[event+TIME_SEP],row[event + TIME_PEAK])

#Example used to see what info is defined for a particular event, and a particular event type
#I used it to debug the rise time to max calculation
name=['Flux Time Series',
		'SEP Start Time',
		'SEP End Time',
		'SEP Duration (hours)',
		'Onset Peak (pfu)',
		'Onset Peak Time',
		'Rise Time to Onset (minutes)',
		'Max Flux (pfu)',
		'Max Flux Time',
		'Rise Time to Max (minutes)',
		'Fluence (cm^-2)',
		'Fluence Spectrum (cm^-2)',
		'Fluence Spectrum Energy Bins (MeV)',
		'Fluence Spectrum Energy Bin Centers (MeV)']
df0=df.iloc[1]
for k in name:
    print(df0[TC_30 +k])

#Example to see why does the calculation of the rise time to max doesn't work 
event_type=TC_30
row=df.iloc[0]
print(row[TC_10 + TIME_MAX],row[TC_10 + TIME_SEP],row[TC_10 + 'Rise Time to Max (minutes)'])
print((pd.to_datetime(row[TC_10 + TIME_MAX]) - pd.to_datetime(row[TC_10 + TIME_SEP])).total_seconds() / 60.0)


#Examples to debug the function plot_flux_time_series
plot_flux_time_series(file_path, df_TC_10.iloc[0], TC_10)
plot_flux_time_series(file_path, df_AB_100.iloc[0], AB_100)
'''