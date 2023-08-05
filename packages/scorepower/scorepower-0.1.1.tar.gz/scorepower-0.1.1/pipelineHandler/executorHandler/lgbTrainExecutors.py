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
import numpy as np
import lightgbm as lgb
import warnings,joblib
import time
from multiprocessing import cpu_count
###std标准化
class executor_stdScaleHandle(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_stdScaleHandle,self).__init__()
        self.__ctx = ctx

    def executor(self,df):
        #数据填充
        print("[标准化处理] ")

        # self.reports.gen_outlierReport_quantile(df.drop(["label","today_overdue_days"],axis=1),5,"./dataReports/outlierReport.csv")
        # self.reports.gen_outlierReport_std(df.drop(["label", "today_overdue_days"], axis=1),"./dataReports/outlierStdReport.csv")

        return df
###lgb模型训练
class executor_lgbModelTrainHandle(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_lgbModelTrainHandle,self).__init__()
        self.__ctx = ctx
        self._model=None

    def _lgbTrainGridSearch(self, x_train, x_test, y_train, y_test,cvn):

        starttime=time.time()
        gbm = lgb.LGBMClassifier(objective='binary',
                                 is_unbalance=True,
                                 metric='binary_logloss,auc',
                                 max_depth=6,
                                 num_leaves=40,
                                 learning_rate=0.1,
                                 feature_fraction=0.7,
                                 min_child_samples=21,
                                 min_child_weight=0.001,
                                 bagging_fraction=1,
                                 bagging_freq=2,
                                 reg_alpha=0.001,
                                 reg_lambda=8,
                                 cat_smooth=0,
                                 num_iterations=200,
                                 n_estimators=100
                                 )
        para1 = {
            'max_depth': [4, 6, 8, 12],
            'num_leaves': [20, 30, 40, 50],
        }
        ############## stpe1 ##############
        gsearch1 = GridSearchCV(gbm, param_grid=para1, scoring='roc_auc', cv=cvn,n_jobs=self.__ctx.task.cpu_core )
        gsearch1.fit(x_train, y_train)
        print("     [gsearch1]: search max_depth and num_leaves")
        print('         参数的最佳取值:{0}'.format(gsearch1.best_params_))
        print('         最佳模型得分:{0}'.format(gsearch1.best_score_))
        # print(gsearch.cv_results_['mean_test_score'])
        # print(gsearch.cv_results_['params'])
        best_max_depth=gsearch1.best_params_["max_depth"]
        best_num_leaves = gsearch1.best_params_["num_leaves"]

        ############## stpe2 ##############
        para2 = {"min_child_samples": [18, 19, 20, 21, 22],"min_child_weight":[0.001, 0.002, 0.003]}

        gsearch2 = GridSearchCV(gbm, param_grid=para2, scoring='roc_auc', cv=cvn,n_jobs=self.__ctx.task.cpu_core )
        gsearch2.fit(x_train, y_train)
        print("     [gsearch2]: search min_child_samples and min_child_weight")
        print('         参数的最佳取值:{0}'.format(gsearch2.best_params_))
        print('         最佳模型得分:{0}'.format(gsearch2.best_score_))
        best_min_child_samples = gsearch2.best_params_["min_child_samples"]
        best_min_child_weight = gsearch2.best_params_["min_child_weight"]

        ############## stpe3 ##############
        para3 = {
            'feature_fraction': [0.6, 0.8, 1],
        }
        gsearch3 = GridSearchCV(gbm, param_grid=para3, scoring='roc_auc', cv=cvn,n_jobs=self.__ctx.task.cpu_core)
        gsearch3.fit(x_train, y_train)
        print("     [gsearch3]: search feature_fraction")
        print('         参数的最佳取值:{0}'.format(gsearch3.best_params_))
        print('         最佳模型得分:{0}'.format(gsearch3.best_score_))
        best_feature_fraction = gsearch3.best_params_["feature_fraction"]

        ############## stpe4 ##############
        para4 = {
            'bagging_fraction': [0.8,0.9,1],
            'bagging_freq': [2,3,4],
        }
        gsearch4 = GridSearchCV(gbm, param_grid=para4, scoring='roc_auc', cv=cvn, n_jobs=self.__ctx.task.cpu_core)
        gsearch4.fit(x_train, y_train)
        print("     [gsearch4]: search bagging_fraction and bagging_freq")
        print('         参数的最佳取值:{0}'.format(gsearch4.best_params_))
        print('         最佳模型得分:{0}'.format(gsearch4.best_score_))
        best_bagging_fraction = gsearch4.best_params_["bagging_fraction"]
        best_bagging_freq = gsearch4.best_params_["bagging_freq"]

        ############## stpe5 ##############
        para5= {
            'reg_alpha': [0.001,0.01, 0.1, 1, 10, 50, 100, 200, 500]
        }
        gsearch5 = GridSearchCV(gbm, param_grid=para5, scoring='roc_auc', cv=cvn, n_jobs=self.__ctx.task.cpu_core)
        gsearch5.fit(x_train, y_train)
        print("     [gsearch5]: search reg_alpha")
        print('         参数的最佳取值:{0}'.format(gsearch5.best_params_))
        print('         最佳模型得分:{0}'.format(gsearch5.best_score_))
        best_reg_alpha = gsearch5.best_params_["reg_alpha"]

        ############## stpe6 ##############
        para6 = {'n_estimators': [100, 400, 250, 80, 500]}
        gsearch6 = GridSearchCV(gbm, param_grid=para6, scoring='roc_auc', cv=cvn, n_jobs=self.__ctx.task.cpu_core)
        gsearch6.fit(x_train, y_train)
        print("     [gsearch6]: search n_estimators")
        print('         参数的最佳取值:{0}'.format(gsearch6.best_params_))
        print('         最佳模型得分:{0}'.format(gsearch6.best_score_))
        best_n_estimators = gsearch6.best_params_["n_estimators"]

        ############## stpe7 ##############
        para7 = {'cat_smooth': [0,10,20]}
        gsearch7 = GridSearchCV(gbm, param_grid=para7, scoring='roc_auc', cv=cvn, n_jobs=self.__ctx.task.cpu_core)
        gsearch7.fit(x_train, y_train)
        print("     [gsearch7]: search cat_smooth")
        print('         参数的最佳取值:{0}'.format(gsearch7.best_params_))
        print('         最佳模型得分:{0}'.format(gsearch7.best_score_))
        best_cat_smooth = gsearch7.best_params_["cat_smooth"]

        ############## 用获取得到的最优参数再次训练模型 ##############
        self._model=lgb.LGBMClassifier(objective='binary',
                                 is_unbalance=True,
                                 metric='binary_logloss,auc',
                                 max_depth=best_max_depth,
                                 num_leaves=best_num_leaves,
                                 learning_rate=0.1,
                                 feature_fraction=best_feature_fraction,
                                 min_child_samples=best_min_child_samples,
                                 min_child_weight=best_min_child_weight,
                                 bagging_fraction=best_bagging_fraction,
                                 bagging_freq=best_bagging_freq,
                                 reg_alpha=best_reg_alpha,
                                 reg_lambda=1,
                                 cat_smooth=best_cat_smooth,
                                 num_iterations=200,
                                 n_estimators=best_n_estimators,
                                 n_jobs=self.__ctx.task.cpu_core)
        print("     [best parameters]: spentTime:{} best_max_depth:{},best_num_leaves:{},best_feature_fraction:{},best_min_child_samples:{},"
              "best_min_child_weight:{},best_bagging_fraction:{},best_bagging_freq:{},best_reg_alpha:{},best_cat_smooth:{},"
              "best_n_estimators:{}".format(time.time()-starttime,best_max_depth,best_num_leaves,best_feature_fraction,best_min_child_samples,
                                                                 best_min_child_weight,best_bagging_fraction,best_bagging_freq,best_reg_alpha,best_cat_smooth,
                                                                 best_n_estimators))
        self._model.fit(x_train, y_train)

        ###tiran  reports
        auc = cross_val_score(self._model, x_train, y_train, scoring='roc_auc', cv=cvn)
        print("     训练集auc.mean():", auc.mean())
        print("     ----------------------")

        lgb_y_pred = self._model.predict_proba(x_test)
        lgb_scores = performance.Prob2Score(lgb_y_pred[:, 1], self.__ctx.task.basePoint, self.__ctx.task.odds)
        report_ks = os.path.join(self.__ctx.task_train_lgb.reports_baseDir, self.__ctx.task_train_lgb.reports_ks)
        pic_ks = os.path.join(self.__ctx.task_train_lgb.reports_baseDir, self.__ctx.task_train_lgb.reports_ks_png)

        lgb_ks = performance.KS(lgb_scores, y_test,report_ks,pic_ks)
        lgb_auc = roc_auc_score(y_test, lgb_y_pred[:, 1])
        print("     测试集KS：", lgb_ks)
        print("     测试集AUC：", lgb_auc)
        print("     ----------------------")

    def _lgbTrainDefault(self, x_train, x_test, y_train, y_test):
        self._model = lgb.LGBMClassifier(
            boosting_type='gbdt', objective='binary', metric="auc",
            max_depth=10, num_leaves=560, n_estimators=1500, reg_alpha=0.0, reg_lambda=1,
            subsample=0.8, colsample_bytree=0.8, subsample_freq=1,
            learning_rate=0.01, min_child_weight=50,
            feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=5,
            lambda_l1=0.4, lambda_l2=0.5, min_gain_to_split=0.2,  # verbose=5,
            random_state=None, n_jobs=self.__ctx.task.cpu_core, num_iterations=5000,
        )  # lgb

        auc = cross_val_score(self._model, x_train, y_train, scoring='roc_auc', cv=5)
        self._model.fit(x_train, y_train)
        lgb_y_pred = self._model.predict_proba(x_test)
        lgb_scores = performance.Prob2Score(lgb_y_pred[:, 1], self.__ctx.task.basePoint, self.__ctx.task.odds)

        report_ks = os.path.join(self.__ctx.task_train_lgb.reports_baseDir, self.__ctx.task_train_lgb.reports_ks)
        pic_ks = os.path.join(self.__ctx.task_train_lgb.reports_baseDir, self.__ctx.task_train_lgb.reports_ks_png)

        lgb_auc = roc_auc_score(y_test, lgb_y_pred[:, 1])
        lgb_ks = performance.KS(lgb_scores,lgb_auc, y_test, report_ks, pic_ks,self.__ctx.task_train_lgb.reports_ks_scores_bin)

        print("     训练集auc.mean():", auc.mean())
        print("     测试集KS：", lgb_ks)
        print("     测试集AUC：", lgb_auc)
        print("     ----------------------")
    def __modelExport(self):
        coefFile = os.path.join(self.__ctx.task_train_lgb.model_baseDir, self.__ctx.task_train_lgb.model_coef)
        joblibFile = os.path.join(self.__ctx.task_train_lgb.model_baseDir, self.__ctx.task_train_lgb.model_joblib_pkl)

        self._model.booster_.save_model(coefFile)
        print("     [生成权重文件]:", coefFile)
        joblib.dump(self._model, joblibFile)
        print("     [生成模型文件]:", joblibFile)

    def executor(self,df):
        warnings.filterwarnings('ignore')
        print("[lgb模型训练] 训练方式:",self.__ctx.task_train_lgb.model_trian_type)
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
        if self.__ctx.task_train_lgb.model_trian_type == self.__ctx.trainMode_gridSearch:
            self._lgbTrainGridSearch(x_train, x_test, y_train, y_test,5)
        elif self.__ctx.task_train_lgb.model_trian_type == self.__ctx.trainMode_default:
            self._lgbTrainDefault(x_train, x_test, y_train, y_test)

        self.__modelExport()
        return df