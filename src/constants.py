#Define the Constants: 
#different event types
TC_10='>10.0 MeV 10.0 pfu '
TC_30='>30.0 MeV 1.0 pfu '
TC_50='>50.0 MeV 1.0 pfu '
TC_100='>100.0 MeV 1.0 pfu '
AB_10='>10.0 MeV 1e-06 pfu '
AB_30='>30.0 MeV 1e-06 pfu '
AB_50='>50.0 MeV 1e-06 pfu '
AB_100='>100.0 MeV 1e-06 pfu '

EVENT_TYPES=[TC_10, TC_30, TC_50, TC_100, AB_10, AB_30, AB_50, AB_100]

#Event longitude selection
#In this configuration, if the longitude is 0°, the event is considered to be Eastern and Western, It is counted twice
EASTERN=(-180,0)
WESTERN=(0,180)

#Time constant for Flare and CME, that doesn't depends on the flux type
TIME_FLARE='Flare Xray Peak Time'
TIME_CME='CME CDAW First Look Time'

#Time key word for Onset peak, and max flux that depends on the flux type
TIME_PEAK='Onset Peak Time'
TIME_MAX='Max Flux Time'
TIME_SEP='SEP Start Time'