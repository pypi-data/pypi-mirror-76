#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

#get custom packages
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

class RavenTableCheckOutput(BaseEstimator, TransformerMixin):
    """ check every single table for who edited it, when they edited it and the row count

    :return: ROI Report of the member gap information
    :rtype: string
    """

    def __init__(self):
        """constructor class
        """
        pass

    def report(self):

        # get the db name
        dbName = '''dev_cvsdia_enc'''

        # get the prefix
        dbPrefix = ''

        #get the list of tables

