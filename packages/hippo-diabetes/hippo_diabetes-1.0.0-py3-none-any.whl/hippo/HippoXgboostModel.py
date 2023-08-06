#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import mean_absolute_error,make_scorer
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from hyperopt import hp, fmin, tpe, space_eval, STATUS_OK, Trials
from catboost import CatBoostRegressor
from scipy import stats
import pickle


#modeling packages
import pickle
import xgboost as xgb

#import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

#class
class HippoXgboostModel(BaseEstimator, TransformerMixin):
    """ xgboost model Fitter
    :parameter:
    :param X: trainning dataset
    :type X: pd.DataFrame
    :param y: outcome colunns
    :type y: pd.Series
    :param pickleName: name of pickled model object if using historic model or saving the name of a new model
    :type pickleName: string or None
    :param pickleSave: True if we should save this copy of the model, else False if we are not going to save it
    :type pickleSave: bool
    :param kfold: number of folds
    :type kfold: interger
    :param hyperoptGo: True if we are going to hyperparamter tune this model, else false
    :type hyperoptGo: bool
    :param space: dictionary that holds the range of spaces permitted for model tunning
    :type space: dict
    :param maxEvals: cap of the number of times that hyper opt does optimization
    :type maxEvals: int
    :param seenUnseen: unseen if you want the prediction recalculated on unseen people, seen if you want it calculated on seen people (artifically high)
    :type seenUnseen: string
    :param newPickleName: if creating a new model, use this name
    :type newPickleName: string
    :return: model
    :type: model

    """

    # Class Constructor
    def __init__(self,model=None,pickleName=None, pickleSave= False, kfold=None,hyperoptGo=None,space=None,maxEvals=None,seenUnseen = None,newPickleName=None):
        """ constructor method
        """
        #retrieve model params
        modelParam = UtilAPI().modelParam

        #model
        #initalize model
        if model is None:
            self.model = None
        else:
            self.model = model

        #pickle information
        if pickleName is None:
            self.pickleName = modelParam['hippo_model_pickleName']
        else:
            self.pickleName = pickleName

        if pickleSave is None:
            self.pickleSave = modelParam['hippo_model_pickleSave']
        else:
            self.pickleSave = pickleSave

        #kfold parameters set from the modelParam
        if kfold is None:
            self.kfold = modelParam['hippo_model_kfold']
        else:
            self.kfold = kfold

        #hyperopt do or not do: set in modelParam
        if hyperoptGo is None:
            self.hyperoptGo = modelParam['hippo_model_hyperoptGo']
        else:
            self.hyperoptGo = hyperoptGo

        #space that the model can train
        if space is None:
            self.space = modelParam['hippo_model_space']
        else:
            self.space = space

        #number of evaluations
        if maxEvals is None:
            self.maxEvals = modelParam['hippo_model_maxEval']
        else:
            self.maxEvals = maxEvals

        #unseen or seen data in the prediction
        if seenUnseen is None:
            self.seenUnseen = modelParam['hippo_model_seenUnseen']
        else:
            self.seenUnseen = seenUnseen

        #new file name to save
        if newPickleName is None:
            self.newPickleName = modelParam['hippo_model_newPickleName']
        else:
            self.newPickleName = newPickleName

    @classmethod
    def gini(cls, truth, predictions):
        """
        :param truth:
        :param predictions:
        :return:
        """
        g = np.asarray(np.c_[truth, predictions, np.arange(len(truth))], dtype=np.float)
        g = g[np.lexsort((g[:, 2], -1 * g[:, 1]))]
        gs = g[:, 0].cumsum().sum() / g[:, 0].sum()
        gs -= (len(truth) + 1) / 2.
        return gs / len(truth)

    @classmethod
    def gini_sklearn(cls, truth, predictions):
        """
        :param truth:
        :param predictions:
        :return:
        """
        return cls.gini(truth, predictions) / cls.gini(truth, truth)

    def optimize(self, clf, X, y, max_evals):

        """
        This is the optimization function that given a space (space here) of
        hyperparameters and a scoring function (score here), finds the best hyperparameters.
        """
        clf = self.model


        def objective(params):
            """

            :param params: paramters based on the space and the hyperopt choice that we are trying to score
            :type params: dictionr
            :return: score based on cross validation
            :rtype: float

            """

            clf.set_params(**params)

            gini_scorer = make_scorer(self.gini_sklearn,
                                      greater_is_better=True,
                                      needs_proba=False)

            score = cross_val_score(clf, X, y,
                                    scoring=gini_scorer,
                                    cv=KFold(n_splits=3,
                                             shuffle=True)).mean()

            #print("Gini {:.3f} params {}".format(score, params))

            return score

        #hyperopt going its optimized grid search 
        best = fmin(fn=objective,
                    space=self.space,
                    algo=tpe.suggest,
                    max_evals=max_evals)

        return best

    def get_model(self,X,y):
        """return model and also do the hyper optimization as needed
        Parameters
        :param X: array of features of interest for training
        :type X: pd.DataFrame
        :param y: one dimensional array of features of interest for testing
        :type Y: pd.Series

        :return: model that has been fitted
        :rtype: in memory model
        """

        #figure retrieve model as needed if we are using a historic model
        if self.pickleName is not None:

            #load saved model with previously optimized parameters
            self.model = pickle.load(open(self.pickleName,'rb'))

        #create new model otherwise with the hyperparamter space
        if self.newPickleName is not None:
            self.model = CatBoostRegressor(logging_level='Silent')

            #problems with hyperoptimization ,revisit later
            return self.model
            #self.model = xgb.XGBRegressor(self.space)

        #optimize model
        if self.hyperoptGo == True:

            #fit the best params and reset the moel reset model
            self.model.set_params = self.optimize(self.model,
                                                  X.values,
                                                  y.values,
                                                  max_evals=self.maxEvals)

        #save model as requested
        if self.pickleSave == True:
            pickle.dump(self.model, open(self.pickleName, 'wb'))

        #return None (fit function sets the paramteres of the model
        return self.model


