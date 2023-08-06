# imports from general
import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error,mean_squared_error
from scipy import stats
from datetime import datetime
from sklearn.model_selection import train_test_split, KFold

#custom functions from this module
from HippoRowRandomizerMasker import HippoRowRandomizerMasker
from HippoOutcomePredictionTranche import HippoOutcomePredictionTranche
from HippoXgboostModel import HippoXgboostModel
from HippoShapTransformer import HippoShapTransformer

#custom functions from other modules
#import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

# package for modeling
class HippoAPI:

    # init
    def __init__(self,**kwargs):
        """constructor class
        """
        self.modelParam = UtilAPI().modelParam

    def _fit(self,X,model,y,**kwargs):
        """generic fit function

        :param X: two dimensional training data set
        :type X: pd.DataFrame
        :param model: generic model that will be fit
        :type model: model
        :param y: one dimensional outcome vector
        :type y: pd.Series
        :param cv: Kfold object holding the number of splits to conduct
        :type cv: Kfold
        :return: model, fitted
        :rtype: model
        """

        #timer
        startTime = datetime.now()

        #create the fitted model as an attribute
        self.model = model.fit(X.values,y.values)

        #complete time
        self.timeFit = datetime.now()-startTime

        #return model as needed
        return self.model


    def _predict(self,X, y=None,model=None,cv=KFold(n_splits=3, shuffle=True), seen=False,**kwargs):
        """ generic predict function
        :param X: two dimensional training data set
        :type X: pd.DataFrame
        :param model: generic model that will be fit
        :type model: model
        :param y: one dimensional outcome vector
        :type y: pd.Series
        :param cv: Kfold object holding the number of splits to conduct
        :type cv: Kfold
        :return:
        """
        #timer
        startTime = datetime.now()

        #holders for test information
        testPredictionIndexHolder = []
        testPredictionHolder = []

        #grab model
        if model is None:
            model = self.model

        #if we are operation on seen data
        if seen == True:
            for counter, (train_index, test_index) in enumerate(cv.split(X)):
                # split into sets
                X_test = X.values[test_index]

                # predict on fitted model
                y_pred = model.predict(X_test)

                #get the predicted value on unseen data
                testPredictionIndexHolder.append(test_index)
                testPredictionHolder.append(y_pred)

        #it we are operating on unseen data (training and then testing on the holdout that was not used
        elif seen == False:
            for counter, (train_index, test_index) in enumerate(cv.split(X)):

                # split into sets
                X_train, X_test = X.values[train_index], X.values[test_index]
                y_train, y_test = y.values[train_index], y.values[test_index]

                #fit the model on the seen
                # predict on fitted model
                model = self.model
                model_fitted = model.fit(X_train, y_train)

                # predict for the unseen
                y_pred = model_fitted.predict(X_test)

                #get the predicted value on unseen data
                testPredictionIndexHolder.append(test_index)
                testPredictionHolder.append(y_pred)

        #organize test prediction results (clean up in the future)
        testPrediction = np.stack([np.concatenate(testPredictionIndexHolder),np.concatenate(testPredictionHolder)],axis=1)
        testPrediction = testPrediction[testPrediction[:,0].argsort()][:,1]

        #complete time
        self.timePredict = datetime.now()-startTime

        #return seen prediction
        return testPrediction


    def _score(self,y,yPred,model,**kwargs):
        """ score metrics
        :param y: one dimensional outcome vector
        :type y: pd.Series
        :param yPred: one dimensional outcome vector - predicted
        :type yPred: pd.Series
        :param model: generic model that will be fit
        :type model: model
        :param kwargs:
        :return:
        """

        #dictionary of results
        scoreDict = {}

        #model and statistics
        scoreDict['model'] = model
        scoreDict['MAE'] = mean_absolute_error(y, yPred)
        scoreDict['MSE'] = mean_squared_error(y, yPred)
        scoreDict['Pearson R2'] =stats.pearsonr(y, yPred)[0] ** 2

        #timing informatin
        scoreDict['time_run'] = datetime.now()

        #if exists
        if self.timeFit is not None:
            scoreDict['time_fit'] = self.timeFit
        if self.timePredict is not None:
            scoreDict['time_predict'] = self.timePredict

        #create information
        self.scoreDict = scoreDict

        #return if requested
        return scoreDict

    #causal ml
    def causalml(self,X,y):

        for treatment in modelParam['moose_impact_feature_list']:
            xl = BaseXRegressor(learner=XGBRegressor(random_state=42))
            te, lb, ub = xl.estimate_ate(X, e, treatment, y)
            print('Average Treatment Effect (BaseXRegressor using XGBoost): {:.2f} ({:.2f}, {:.2f})'.format(te[0], lb[0], ub[0]))

#main (fits and predicts)(break out these functions and then include inside the hippo command
    def hippo(self,X):

        #randomize rows
        X = HippoRowRandomizerMasker().transform(X)

        # split out the data and the columns
        #data is correct at this step but removes columns that we do not want
        X, y, XMisc = HippoOutcomePredictionTranche(outcomeColName=self.modelParam['hippo_model_outcomeColName'],
                                                    memberShare=self.modelParam['hippo_model_memberShare'] ).transform(X)
        ####
        ####xgboost
        ####

        #get model
        self.model = HippoXgboostModel().get_model(X,y)

        #fit model
        self._fit(X,self.model,y)

        #predict with model
        yPred = self._predict(X,y,self.model)

        #score with model
        self._score(y,yPred,self.model)

        ####
        ####shap
        ####

        #apply shap
        shap = HippoShapTransformer().transform(X,self.model)

        #output
        #clean up results and put back in features removed from shap
        XOutput = pd.concat([y,X,XMisc,shap],axis=1).reset_index(drop=True)

        #add prediction column to data set with clear label as the first value
        XOutput.insert(loc=0, column=self.modelParam['hippo_model_outcomeColName']+"_prediction", value=yPred)

        #save as memory object
        self.X = XOutput
