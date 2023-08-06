#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterRealRequiredThresholdSelector import OtterRealRequiredThresholdSelector
from OtterDenseMatrixMasker import OtterDenseMatrixMasker
class OtterDensePipeline:
    """Pipeline for making dense matrix

    Parameters:
    :param realRequiredThreshold: for a column to be retained, this number (expressing a percentage between 0 and 100) most have none null values
    :type realRequiredThreshold:float

    Returns:
    :return: dense data frame
    :rtype: pd.DataFrame
    """

    def __init__(self, realRequiredThreshold=90.0):
        """constructor method
        """
        self.realRequiredThreshold = np.float(realRequiredThreshold)


    # apply pipe function
    def add_pipe(self):
        OtterDensePipeline = Pipeline(steps=[
            ('OtterRealRequiredThresholdSelector', OtterRealRequiredThresholdSelector(realRequiredThreshold=self.realRequiredThreshold)),
            ('OtterDenseMatrixMasker',OtterDenseMatrixMasker())
        ])

        # return pipeline
        return OtterDensePipeline