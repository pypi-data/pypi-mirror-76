#imports
import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from RhinoROIChannelSelector import RhinoROIChannelSelector
from RhinoChannelSuppression import RhinoChannelSuppression
from RhinoChannelPermission import RhinoChannelPermission
from RhinoProactiveChannelSelector import RhinoProactiveChannelSelector
from RhinoHighMediumLowClassfier import RhinoHighMediumLowClassfier
from RhinoJourneyCost import RhinoJourneyCost

# import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead + '/hippo/src2/util')
from util import UtilAPI

class RhinoChannelSelectionPipeline:
    """Pipeline for Channel Selection bucket in Pre-CPL module
    It determines the High/Medium/Low Member journey

    Parameters:
    :param modelParam: dict of util model param
    :type modelParam: dict

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """


    def __init__(self):
        """constructor method
        """
        self.modelParam = UtilAPI().modelParam

    # apply pipe function
    def add_pipe(self):
        ChannelSelectionPipeline = Pipeline(steps=[
            # turn on channel for a member if ROI>=1
            ('ROIChannelSelector', RhinoROIChannelSelector(channel_dict = self.modelParam['rhino_channel_dict'], 
                                                           direct_comms = self.modelParam['rhino_direct_comms'],
                                                           proactive_channels = self.modelParam['rhino_proactive_channels'])),
            # suppress IVR and Care Coordinator to avoid program overlap
            ('ChannelSuppression', RhinoChannelSuppression(no_IVR_CC_prgms = self.modelParam['rhino_no_IVR_CC_prgms'], 
                                                           no_CC_prgms     = self.modelParam['rhino_no_CC_prgms'])),
            # apply channel permissions 
            ('ChannelPermission', RhinoChannelPermission(direct_comms       = self.modelParam['rhino_direct_comms'] , 
                                                         proactive_channels = self.modelParam['rhino_proactive_channels'])),
            # select the preferred proactive call channel
            ('ProactiveChannelSelector', RhinoProactiveChannelSelector(proactive_channels = self.modelParam['rhino_proactive_channels'])),
            # classify member journey into High/Medium/Low
            ('HighMediumLowJourney', RhinoHighMediumLowClassfier(direct_comms       = self.modelParam['rhino_direct_comms'] , 
                                                                 proactive_channels = self.modelParam['rhino_proactive_channels'])),
            ('JourneyCost', RhinoJourneyCost(channel_dict = self.modelParam['rhino_channel_dict'], 
                                             direct_comms = self.modelParam['rhino_direct_comms']))
        ])
        # return pipeline
        return ChannelSelectionPipeline
   