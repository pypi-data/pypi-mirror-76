# coding=utf-8
import abc
#混淆矩阵计算
from sklearn import metrics
from sklearn.metrics import roc_curve, auc,roc_auc_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from modelProcessor.performance import performance
import  pandas as pd
import os,time
from modelProcessor.modelSelector import model
from sklearn.preprocessing import LabelEncoder
import numpy as np
import datetime

class modelTrain(metaclass=abc.ABCMeta):
    def __init__(self,model):
        self._model=model

    @abc.abstractmethod
    def dataLoad(self):
        pass

    def fit(self,x_train, y_train, x_test, y_test):
        starttime = datetime.datetime.now()
        pred_model = self._model(x_train, y_train,x_test,y_test)
        endtime = datetime.datetime.now()
        print("耗时：%d" % (endtime - starttime).seconds + "s")
        y_pred = pred_model.predict(x_test,num_iteration=pred_model.best_iteration_)
        # 计算P、R、F1
        performance.confusionMatrixcal(y_test, y_pred)



        return pred_model

        # pd.DataFrame({
        #     'column': x_train.columns,
        #     'importance': pred_model.feature_importances_,
        # }).sort_values(by='importance')  # .to_excel("./feature_importances_lightGbm_1000.xlsx")
        # self.pre_model = pred_model
        # 保存模型
        # from sklearn.externals import joblib
        # joblib.dump(pred_model, 'gbm.pkl')

