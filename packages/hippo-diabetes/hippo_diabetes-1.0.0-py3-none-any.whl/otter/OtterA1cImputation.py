# imports from general
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#class
class OtterA1cImputation(BaseEstimator, TransformerMixin):
    """For all the members in cohort without a1c values, impute the a1c values with stratified imputation

    Parameters
    :param mappingCol: columns on which to map stratified imputation
    :type mappingCol: list
    :param imputeCol: column on which to perform stratified imputation
    :type imputeCol: string
    :param newImputeCol:column with missing values replaced with imputation
    :tyoe newImputeCol:string
    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """
    # Class Constructor
    def __init__(self,mappingCol=[],imputeCol='',newImputeCol=''):
        """ constructor method
        """
        self.mappingCol = mappingCol
        self.imputeCol = imputeCol
        self.newImputeCol = newImputeCol
    
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
    
    def transform(self,X,y=None):
        """impute the columns with missing values

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: data frame with the columns of interest
        :rtype: pd.DataFrame
        """
        #check whether the imputed column is in the mapping columns
        if self.imputeCol in self.mappingCol:
            raise ValueError("{} must not include {}".format(self.mappingCol, self.imputeCol))
        
        # group by mapping columns and have the mean
        imputed_vals = X.groupby(self.mappingCol).agg(
            imputed_val = pd.NamedAgg(column=self.imputeCol,aggfunc='mean')
        )
        
        # fill nan with mean of the overall mean
        imputed_vals.fillna(X[self.imputeCol].mean(),inplace=True)
                
        # add the impute_val to original table (imputed_val)
        X = X.merge(imputed_vals, how='left', left_on=self.mappingCol, right_on = self.mappingCol)

        # for lab_a1c that are missing values, replace with imputed values
        X[self.newImputeCol] = X[self.imputeCol].fillna(round(X['imputed_val'],1))
        
        X = X.drop('imputed_val',axis=1)
        
        return X
        
