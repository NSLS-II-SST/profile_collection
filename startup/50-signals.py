print(f'Loading {__file__}...')

from ophyd import EpicsSignalRO

# These might need/make more sense to be split up into separate files later on.
# But while we have so few, I'm just putting them in this single file.

bpm13_sum = EpicsSignalRO('XF:07ID-BI{BPM:13}Stats5:Total_RBV', name='bpm13_sum')

dm3_c1 = EpicsSignalRO('XF:07ID-BI{DM3:I400-1}:IC1_MON', name='dm3_c1')

# Not sure how best to do this image yet... 

#BPM13 Image:
#XF:07ID-BI{BPM:13}image1:ArrayData
