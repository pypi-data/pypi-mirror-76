#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#get required transformers
from WhaleRhinoTestCallToActionTransformer import *
from WhaleRhinoTestRankAndWeightTransformer import *
from WhaleRhinoTestROIThresholdTransformer import *
from WhaleRhinoTestCampaignSelectionTransformer import *
from WhaleRhinoTestChannelPermissionTransformer import *
from WhaleRhinoTestChannelSuppressionTransformer import *
from WhaleRhinoTestProactiveChannelSelectorTransformer import *
from WhaleRhinoTestHMLClassTransformer import *


#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#menagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)


#class
class WhaleRhinoPipeline(BaseEstimator, TransformerMixin):
    """runs the checks needed to authenticate that rhino is performing to the quality control standards

    Parameters

    Returns
    :returns: if there are no errors, returns outcome of rhino.X without removing or changing any data; if there are any errors asserts an error
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        self.modelParam = UtilAPI().modelParam

    # apply pipe function
    def add_pipe(self):

        #init dict
        modelParam = UtilAPI().modelParam

        #create all the preCPL components
        whaleRhinoPipeline = Pipeline(steps =[
            ('WhaleRhinoTestCallToActionTransformer',WhaleRhinoTestCallToActionTransformer()),
            ('WhaleRhinoTestRankAndWeightTransformer',WhaleRhinoTestRankAndWeightTransformer()),
            ('WhaleRhinoTestCampaignSelectionTransformer', WhaleRhinoTestCampaignSelectionTransformer()),
            ('WhaleRhinoTestROIThresholdTransformer',WhaleRhinoTestROIThresholdTransformer(channel_dict       = self.modelParam['rhino_channel_dict'], 
                                                                                           direct_comms       = self.modelParam['rhino_direct_comms'],
                                                                                           proactive_channels = self.modelParam['rhino_proactive_channels'])),
            ('WhaleRhinoTestChannelPermissionTransformer',WhaleRhinoTestChannelPermissionTransformer(direct_comms       = self.modelParam['rhino_direct_comms'],
                                                                                                     proactive_channels = self.modelParam['rhino_proactive_channels'])),
            ('WhaleRhinoTestChannelSuppressionTransformer',WhaleRhinoTestChannelSuppressionTransformer(no_IVR_CC_prgms = self.modelParam['rhino_no_IVR_CC_prgms'], 
                                                                                                       no_CC_prgms     = modelParam['rhino_no_CC_prgms'])),
            ('WhaleRhinoTestProactiveChannelSelectorTransformer',WhaleRhinoTestProactiveChannelSelectorTransformer()),
            ('WhaleRhinoTestHMLClassTransformer',WhaleRhinoTestHMLClassTransformer())
            
        ])

        # return pipeline
        return whaleRhinoPipeline

