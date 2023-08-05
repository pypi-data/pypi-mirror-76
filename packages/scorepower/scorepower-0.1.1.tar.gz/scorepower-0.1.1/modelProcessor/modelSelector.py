#coding=utf-8
import  pandas as pd
import os,time
from datetime import datetime,timedelta
from sklearn.preprocessing import LabelEncoder
import numpy as np
from feature_selector import FeatureSelector
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
#from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
import xgboost as xgb
import lightgbm as lgb
from xgboost import plot_importance
from multiprocessing import cpu_count
import datetime
from sklearn.metrics import roc_auc_score,roc_curve,auc
import catboost as cb
from sklearn.model_selection import cross_val_score
#混淆矩阵计算
from sklearn import metrics
from sklearn.metrics import roc_curve, auc,roc_auc_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import statsmodels.api as sm
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
class model:
    @staticmethod
    def logistic(x_train,y_train,x_test,y_test):
        # penalty:正则化 l2/l1
        # C ：正则化强度
        # multi_class:多分类时使用 ovr: one vs rest
        # model = LogisticRegression(penalty='l2', C=100, multi_class='multinomial', solver="newton-cg", n_jobs=-1)
        #
        # lr = model.fit(x_train, y_train)
        # print(lgr.coef_[0])  # 输出逻辑回归系数
        # # # 对测试集进行预测
        # # y_pred = lgr.predict(X_test)

        lr = sm.Logit(y_train, x_train).fit()

        return lr
    @staticmethod
    def xgboost(x_train,y_train,x_test,y_test):
        model = xgb.XGBClassifier(max_depth=10, learning_rate=0.1, n_estimators=200, silent=True,
                                  objective='multi:softmax')

        xgb_model = model.fit(x_train, y_train)

        return xgb_model


    @staticmethod
    def catboost(x_train,y_train,x_test,y_test):
        # cab = cb.CatBoostClassifier(iterations=5000,early_stopping_rounds=500)
        cab = cb.CatBoostClassifier()

        cab.fit(x_train, y_train)
        return cab
    # @staticmethod
    def mlp(x_train,y_train,x_test,y_test):
        import keras
        from keras.models import Sequential
        from keras.layers import Dense, Dropout
        from keras.utils.np_utils import to_categorical
        seq = Sequential()
        seq.add(Dense(64, activation='relu', input_dim=x.shape[1]))
        seq.add(Dense(32, activation='relu'))
        seq.add(Dropout(0.2))
        seq.add(Dense(5, activation='softmax'))
        seq.compile(loss=keras.losses.categorical_crossentropy, optimizer='adam', metrics=['accuracy'])
        y_train = to_categorical(y_train, 5)
        y_test = to_categorical(y_test, 5)
        seq.fit(x=x_train, y=y_train, validation_data=(x_test, y_test), epochs=50, batch_size=10)
    @staticmethod
    def ligthGBM(x_train, y_train, x_test, y_test):

        clf = lgb.LGBMClassifier(
            boosting_type='gbdt', objective='binary', metric="auc",
            max_depth=10, num_leaves=560, n_estimators=1500, reg_alpha=0.0, reg_lambda=1,
            subsample=0.8, colsample_bytree=0.8, subsample_freq=1,
            learning_rate=0.01, min_child_weight=50,
            feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=5,
            lambda_l1=0.4, lambda_l2=0.5, min_gain_to_split=0.2,  # verbose=5,
            random_state=None, n_jobs=cpu_count() - 1, num_iterations=5000
        )

        clf.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)],
                early_stopping_rounds=1000)
        return clf