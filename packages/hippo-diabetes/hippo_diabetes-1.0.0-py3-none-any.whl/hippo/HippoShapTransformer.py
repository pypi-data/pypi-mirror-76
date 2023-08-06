#imports
import pandas as pd
import numpy as np
import shap
import os
from sklearn.base import BaseEstimator, TransformerMixin

#import model params
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

#class
class HippoShapTransformer(BaseEstimator, TransformerMixin):
    """Get shap values and return

    Parameters

    Returns
    :returns: dataframe with shap values appended to the original data frame
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self):
        """ constructor method
        """
        pass

    def fit(self, X, y=None):
        """fit method for collaborating with pipeline

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: fited data frame
        :rtype: sklearn.base.BaseEstimator
        """
        return self

    # Method that describes what we need this transformer to do
    def transform(self, X, model, y=None):
        """Select the columns of interest

        Parameters
        :param X: np.array of features of interest
        :type X: np.array
        :param model: model used to predict the outcome
        :type model:sklearn.base.model
        :param y: np.array of features of interest (none in this case)
        :type Y: np.array

        Returns
        :returns: data frame with shap values
        :rtype: pd.DataFrame
        """
        #retrieve model params
        modelParam = UtilAPI().modelParam

        #develop expaliner
        explainer = shap.TreeExplainer(model)

        #get shap values
        shap_values = explainer.shap_values(X)

        #label the shap_values
        shapOutput = pd.DataFrame(shap_values,columns=[x+modelParam['hippo_model_impact_label'] for x in X.columns])

        #return
        return shapOutput