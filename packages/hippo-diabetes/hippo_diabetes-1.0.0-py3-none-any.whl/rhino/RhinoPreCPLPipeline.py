#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#get files
from RhinoAttachCallToAction import RhinoAttachCallToAction
from RhinoRankAndWeight import RhinoRankAndWeight
from RhinoSelectCallToActionAndCampaign import RhinoSelectCallToActionAndCampaign
from RhinoDispositionSuppression import RhinoDispositionSuppression
from RhinoChannelSelectionPipeline import RhinoChannelSelectionPipeline

#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)

#class
class RhinoPreCPLPipeline(BaseEstimator, TransformerMixin):
    """aggregate the preCPL pipeline for CTA, weight and rank, and campaign selection

    Parameters

    Returns
    :returns: dataframe reorganized to get information reqested for the above specifications
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        pass

    # apply pipe function
    def add_pipe(self):
        #init dict
        modelParam = UtilAPI().modelParam
        
        #create all the preCPL components
        preCPLPipeline = Pipeline(steps =[
            ('RhinoAttachCallToAction',RhinoAttachCallToAction()),
            ('RhinoDispositionSuppression',RhinoDispositionSuppression()),
            ('RhinoRankAndWeight',RhinoRankAndWeight()),
            ('RhinoSelectCallToActionAndCampaign',RhinoSelectCallToActionAndCampaign()), 
            ('RhinoChannelSelection',RhinoChannelSelectionPipeline().add_pipe())
        ])

        # return pipeline
        return preCPLPipeline
    
