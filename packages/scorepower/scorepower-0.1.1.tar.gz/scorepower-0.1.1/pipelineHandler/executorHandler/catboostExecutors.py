from ..pipelineExecutor import pipelineExecutor
import  pandas as pd
from dataProcessor.dataReports import statistics
from dataProcessor.binCut import ChiMerge
from modelProcessor.performance import performance
import os,gc,pickle
import statsmodels.api as sm
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
import time
import lightgbm as lgb
import warnings,joblib
from sklearn import metrics
from sklearn.model_selection import train_test_split
import catboost as cb

from sklearn.datasets import load_breast_cancer

###catboost模型训练
class executor_catboostModelTrainHandle(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_catboostModelTrainHandle,self).__init__()
        self.__ctx = ctx
        self._model=None

    def _cbTrainGridSearch(self, x_train, x_test, y_train, y_test,cvn):
        start_time=time.time()
        # params = {'depth': [4, 7, 10],
        #           'learning_rate': [0.03, 0.1, 0.15],
        #           'l2_leaf_reg': [1, 4, 9],
        #           'iterations': [100,300,500]}
        params = {
            'depth': [3, 1, 2, 6, 4, 5, 7, 8, 9, 10],
            'iterations': [250, 100, 500, 1000,1500,2000],
            'learning_rate': [0.01, 0.1, 0.2, 0.3],
            'l2_leaf_reg': [3, 1, 5, 10, 30, 50, 70, 100],
            'border_count': [32, 5, 10, 20, 50, 100, 200],
        }
        cb_model = cb.CatBoostClassifier(loss_function="Logloss",
                                 eval_metric="Accuracy",
                                 learning_rate=0.01,
                                 iterations=1000,
                                 random_seed=626,
                                 # od_type="Iter",
                                 depth=8,
                                 early_stopping_rounds=500,
                                 thread_count=self.__ctx.task.cpu_core
                                 )

        cb_model_gsearch = GridSearchCV(cb_model, param_grid=params, scoring="roc_auc", cv = cvn,n_jobs=self.__ctx.task.cpu_core)
        cb_model_gsearch.fit(x_train,y_train)
        print("     [cb_model_gsearch]: 耗时:",time.time()-start_time)
        print('         参数的最佳取值:{0}'.format(cb_model_gsearch.best_params_))
        print('         最佳模型得分:{0}'.format(cb_model_gsearch.best_score_))
        best_depth = cb_model_gsearch.best_params_["depth"]
        best_learning_rate = cb_model_gsearch.best_params_["learning_rate"]
        best_l2_leaf_reg = cb_model_gsearch.best_params_["l2_leaf_reg"]
        best_l2_leaf_iterations = cb_model_gsearch.best_params_["iterations"]

        cb_model = cb.CatBoostClassifier(depth=best_depth,learning_rate=best_learning_rate,l2_leaf_reg=best_l2_leaf_reg,
                                         iterations=best_l2_leaf_iterations)
        cb_model.fit(x_train, y_train)
        aauc = cross_val_score(cb_model, x_train, y_train, scoring='roc_auc', cv=cvn)

        y_pred = cb_model.predict_proba(x_test)
        lgb_scores = performance.Prob2Score(y_pred[:, 1], self.__ctx.task.basePoint, self.__ctx.task.odds)
        report_ks = os.path.join(self.__ctx.task_train_catboost.reports_baseDir, self.__ctx.task_train_catboost.reports_ks)
        pic_ks = os.path.join(self.__ctx.task_train_catboost.reports_baseDir, self.__ctx.task_train_catboost.reports_ks_png)

        ks = performance.KS(lgb_scores, y_test,report_ks,pic_ks)
        auc = roc_auc_score(y_test, y_pred[:, 1])
        print("     训练集auc.mean():", aauc.mean())
        print("     测试集KS：", ks)
        print("     测试集AUC：", auc)
        print("     ----------------------")


    def _cbTrainDefault(self, x_train, x_test, y_train, y_test):
        self._model = cb.CatBoostClassifier(
            depth=10, learning_rate=0.1, l2_leaf_reg=9,
            iterations=1500,early_stopping_rounds=500
        )

        # self._model = cb.CatBoostClassifier()
        # auc = cross_val_score(self._model, x_train, y_train, scoring='roc_auc', cv=5)
        # self._model.fit(x_train, y_train, )
        self._model.fit(x_train, y_train,eval_set=(x_test, y_test), plot=True)
        cb_y_pred = self._model.predict_proba(x_test)
        cb_scores = performance.Prob2Score(cb_y_pred[:, 1], self.__ctx.task.basePoint, self.__ctx.task.odds)

        report_ks = os.path.join(self.__ctx.task_train_catboost.reports_baseDir, self.__ctx.task_train_catboost.reports_ks)
        pic_ks = os.path.join(self.__ctx.task_train_catboost.reports_baseDir, self.__ctx.task_train_catboost.reports_ks_png)
        cb_auc = roc_auc_score(y_test, cb_y_pred[:, 1])
        cb_ks = performance.KS(cb_scores, cb_auc,y_test, report_ks, pic_ks,self.__ctx.task_train_catboost.reports_ks_scores_bin)

        # print("     训练集auc.mean():", auc.mean())
        print("     测试集KS：", cb_ks)
        print("     测试集AUC：", cb_auc)
        print("     ----------------------")

    def __modelExport(self):
        coefFile = os.path.join(self.__ctx.task_train_catboost.model_baseDir, self.__ctx.task_train_catboost.model_coef)
        joblibFile = os.path.join(self.__ctx.task_train_catboost.model_baseDir, self.__ctx.task_train_catboost.model_joblib_pkl)

        self._model.save_model(coefFile)
        print("     [生成权重文件]:", coefFile)
        joblib.dump(self._model, joblibFile)
        print("     [生成模型文件]:", joblibFile)

    def __psiTrianTest(self,model,x_train, x_test):
        psiReport = os.path.join(self.__ctx.task_train_catboost.reports_baseDir,self.__ctx.task_train_catboost.reports_psi)
        psiReportPng = os.path.join(self.__ctx.task_train_catboost.reports_baseDir,self.__ctx.task_train_catboost.reports_psi_png)
        performance.psi_calculation2Set(model,
                                        psiReport,
                                        psiReportPng,
                                        x_train,
                                        x_test,
                                        "train",
                                        "test",
                                        self.__ctx.task.basePoint,
                                        self.__ctx.task.odds,
                                        self.__ctx.task_train_catboost.reports_psi_bin)

    def executor(self,df):
        warnings.filterwarnings('ignore')
        print("[catboost模型训练] 训练方式:",self.__ctx.task_train_catboost.model_trian_type)
        obj_cols = [self.__ctx.train.data_label]
        for col in df.columns:
            if str(df[col].dtype) == 'object':
                obj_cols.append(col)
        print("     删除字符型(日期)变量:", obj_cols)
        numerical_cols = df.columns.drop(obj_cols)

        x = df[numerical_cols]
        y = df[self.__ctx.train.data_label]
        df=df[numerical_cols.tolist()+[self.__ctx.train.data_label]]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=22)

        if self.__ctx.task_train_catboost.model_trian_type == self.__ctx.trainMode_gridSearch:
            self._cbTrainGridSearch(x_train, x_test, y_train, y_test,5)
        elif self.__ctx.task_train_catboost.model_trian_type == self.__ctx.trainMode_default:
            self._cbTrainDefault(x_train, x_test, y_train, y_test)

        self.__modelExport()
        self.__psiTrianTest(self._model,x_train, x_test)

        return df

class executor_catboostPredictHandle(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_catboostPredictHandle,self).__init__()
        self.__ctx = ctx
        # if self.__ctx
        # self.__model=joblib.load(self.modeInfo.modelfile_pkl)