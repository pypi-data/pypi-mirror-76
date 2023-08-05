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

###分箱
class executor_binCutHandle(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_binCutHandle,self).__init__()
        self.__ctx = ctx

    def _loadPara(self,df,special_attribute=[]):
        with open(os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_woeParaPickle), "rb") as f:
            var_WOE = pickle.load(f)
        with open(os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivParaPickle), "rb") as f:
            var_IV = pickle.load(f)
        with open(os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_cutoffParaPickle), "rb") as f:
            var_cutoff = pickle.load(f)
        woe_cols=var_WOE.keys()

        del_cols=df.columns.drop(woe_cols)
        for i,col in enumerate(woe_cols):
            print("      正在导入{}/{},字段: {}".format(i+1,len(var_WOE.keys()),col))
            col1 = str(col) + "_WOE"
            if col in var_cutoff.keys():
                cutOffPoints = var_cutoff[col]
                binValue = df[col].map(lambda x: ChiMerge.AssignBin(x, cutOffPoints, special_attribute=special_attribute))
                df[col] = binValue.map(lambda x: var_WOE[col][x])
            else:
                df[col] = df[col].map(lambda x: var_WOE[col][x])
        df.drop(del_cols,axis=1,inplace=True)
        print("     [complted load woe/cutoff parameters]!!!")

    def executor(self,df):

        print("[分箱]:生成方式:{}\n   生成分箱占比报告:{},和超过阈值{}的特征占比报告:{},以及ivWoeCutoff报告:{}".format(self.__ctx.task_train_lr.model_ivWoeCutoff_genType,
                                                                             os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_singBinPcn),
                                                                             self.__ctx.task_train_lr.para_singBin_maxPercentThreshHold,
                                                                             os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_singBinPcnOverThreshold),
                                                                             os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivWoeCutoff)))

        df_label=df[self.__ctx.train.data_label]
        #报告未生成
        if not os.path.exists(os.path.join(self.__ctx.task_train_lr.model_baseDir, self.__ctx.task_train_lr.model_ivWoeCutoff)):
            if self.__ctx.task_train_lr.model_ivWoeCutoff_genType != self.__ctx.reportSaveModel_never:
                # a.numerical(obj变量)和catigorey变量区分，并删除常数型变量
                obj_cols = [self.__ctx.train.data_label]
                for col in df.columns:
                    if str(df[col].dtype) == 'object':
                        obj_cols.append(col)
                print("     删除字符型(日期)变量:", obj_cols)
                numerical_cols = df.columns.drop(obj_cols)

                ChiMerge.numericalBinCut(df, numerical_cols, self.__ctx.train.data_label, [],
                                         self.__ctx.task_train_lr.para_singBin_maxPercentThreshHold,
                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivWoeCutoff),
                                         os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.model_singBinPcnOverThreshold),
                                         os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.model_singBinPcn),

                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_woeParaPickle),
                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivParaPickle),
                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_cutoffParaPickle))
        else:#报告已生成
            if self.__ctx.task_train_lr.model_ivWoeCutoff_genType == self.__ctx.reportSaveModel_always:
                #重新生成
                # a.numerical(obj变量)和catigorey变量区分，并删除常数型变量
                obj_cols = [self.__ctx.train.data_label]
                for col in df.columns:
                    if str(df[col].dtype) == 'object':
                        obj_cols.append(col)
                print("     删除字符型(日期)变量:", obj_cols)
                numerical_cols = df.columns.drop(obj_cols)

                ChiMerge.numericalBinCut(df, numerical_cols, self.__ctx.train.data_label, [],
                                         self.__ctx.task_train_lr.para_singBin_maxPercentThreshHold,
                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivWoeCutoff),
                                         os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.model_singBinPcnOverThreshold),
                                         os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.model_singBinPcn),

                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_woeParaPickle),
                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivParaPickle),
                                         os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_cutoffParaPickle))

        self._loadPara(df)
        df[self.__ctx.train.data_label]=df_label
        print("     df.shape: ",df.shape)
        return df

###单变量分析--IV分析
class executor_singleVarIVAnalysisHandle(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_singleVarIVAnalysisHandle, self).__init__()
        self.__ctx = ctx

    def executor(self, df):
        print("[单变量分析--剔除低iv和高iv变量]: 删除iv>{}和iv<{}的变量".format(self.__ctx.task_train_lr.para_ivThreshold_high,self.__ctx.task_train_lr.para_ivThreshold_low))
        model_ivWoeCutoff=os.path.join(self.__ctx.task_train_lr.model_baseDir, self.__ctx.task_train_lr.model_ivWoeCutoff)
        assert os.path.exists(model_ivWoeCutoff), ("***can't find ivWoeCutoff report file %s" % model_ivWoeCutoff)
        # 删除低IV和高IV的变量
        iv_df = pd.read_csv(model_ivWoeCutoff, index_col=0)
        lowIV_cols = iv_df[iv_df["iv"] < self.__ctx.task_train_lr.para_ivThreshold_low].index
        highIV_cols = iv_df[iv_df["iv"] > self.__ctx.task_train_lr.para_ivThreshold_high].index
        df.drop(lowIV_cols, axis=1, inplace=True)
        df.drop(highIV_cols, axis=1, inplace=True)
        print("     删除IV<{}数量{}个".format(self.__ctx.task_train_lr.para_ivThreshold_low,len(lowIV_cols)))
        print("     删除IV>{}数量{}个".format(self.__ctx.task_train_lr.para_ivThreshold_high, len(highIV_cols)))
        print("     删除后df.shape:",df.shape)
        return df


###单变量分析--相关系数分析
class executor_singleVarCorrAnalysisHandle(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_singleVarCorrAnalysisHandle, self).__init__()
        self.__ctx = ctx
    def __sortByIV(self,cols,ivParaFile):
        iv_dict = pd.read_pickle(ivParaFile)
        sortCol = {}
        for col in cols:
            sortCol[col] = iv_dict[col]
        aa = sorted(sortCol.items(), key=lambda x: x[1], reverse=True)
        aa = [x[0] for x in aa]
        return aa

    def executor(self, df):
        print("[单变量分析--剔除高相关性变量]: 按IV排序，排序后删除corr>{}和corr<{}的变量".format(self.__ctx.task_train_lr.para_highCorrThreshhold_max,self.__ctx.task_train_lr.para_highCorrThreshhold_min))
        reports_corr=os.path.join(self.__ctx.task_train_lr.reports_baseDir, self.__ctx.task_train_lr.reports_corr)
        reports_highCorr=os.path.join(self.__ctx.task_train_lr.reports_baseDir, self.__ctx.task_train_lr.reports_highCorr)
        assert os.path.exists(reports_corr), ("***can't find corr report file %s" % reports_corr)
        ##############剔除高相关性变量##############
        df_corr = pd.read_csv(reports_highCorr)

        ## sortby IV
        merge_corr_df = pd.DataFrame(df_corr.groupby(df_corr.columns[0]).apply(
            lambda df_corr: df_corr[df_corr.columns[1]].tolist()).reset_index())
        merge_corr_df.columns = ["col1", "corr_col"]
        merge_corr_df["corr_col"] = merge_corr_df["col1"].apply(lambda x: [x]) + merge_corr_df["corr_col"]
        merge_corr_df["corl_col_len"] = merge_corr_df["corr_col"].apply(lambda x: len(x))

        merge_corr_df["corr_col"] = merge_corr_df["corr_col"].apply(lambda x: self.__sortByIV(x,os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivParaPickle)))
        merge_corr_df.sort_values(by="corl_col_len", ascending=False, inplace=True)

        del_lowIV_col = []
        all_col = []
        ## remove
        for item in merge_corr_df.iterrows():
            all_col = all_col + item[1]["corr_col"]
            all_col = list(set(all_col))
            lowIV_col = item[1]["corr_col"][1:]  # 每一列，只保留最高iv
            del_lowIV_col = del_lowIV_col + lowIV_col

        del_lowIV_col = list(set(del_lowIV_col))

        df.drop(del_lowIV_col, axis=1, inplace=True)
        print("     删除{}个相关性较高的变量，删除后df.shape:{}".format(len(del_lowIV_col), df.shape))

        return df

###生成vif报告
class executor_genVifReport(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_genVifReport, self).__init__()
        self.__ctx = ctx

    def executor(self, df):
        print("[生成vif报告]: vif报告生成方式:{},用于判断是否存在多重共线性".format(self.__ctx.task_train_lr.reports_vif_genType))
        # 生成corr报告
        reports_vif=os.path.join(self.__ctx.task_train_lr.reports_baseDir, self.__ctx.task_train_lr.reports_vif)
        model_ivWoeCutoff = os.path.join(self.__ctx.task_train_lr.model_baseDir, self.__ctx.task_train_lr.model_ivWoeCutoff)
        #报告不存在，则重新生成,或者当设置为never则不生成
        if not os.path.exists(reports_vif):
            if self.__ctx.task_train_lr.reports_corr_genType != self.__ctx.reportSaveModel_never:
                statistics.gen_vifRreport(df, model_ivWoeCutoff,reports_vif)
        #报告存在
        else:
            print("     已有报告存在:", reports_vif)
            if self.__ctx.task_train_lr.reports_corr_genType == self.__ctx.reportSaveModel_always:
                statistics.gen_vifRreport(df, model_ivWoeCutoff,reports_vif)
        return df


###多变量分析--剔除多重共线性变量
class executor_multicollinearityAnalysisHandle(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_multicollinearityAnalysisHandle, self).__init__()
        self.__ctx = ctx

    def executor(self, df):
        print("[多变量分析--剔除多重共线性变量]: corr报告生成方式:{}".format(self.__ctx.task_train_lr.reports_vif_genType))
        reports_vif=os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.reports_vif)
        assert os.path.exists(reports_vif), ("***can't find vif report file %s" % reports_vif)
        # 删除多重共线性
        vif_df = pd.read_csv(reports_vif)
        col_del = vif_df[vif_df["vif"] > self.__ctx.task_train_lr.para_vif_threshold]["col"].tolist()
        print("     vif>{}的变量共有{}个，将被剔除]".format(self.__ctx.task_train_lr.para_vif_threshold, len(col_del)))
        df.drop(col_del, axis=1, inplace=True)
        return df
###pValue报告生成
class executor_genPValueReport(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_genPValueReport, self).__init__()
        self.__ctx = ctx

    def _pvalue_check(self,df,target,pValuer_threshold,report_pValuePara):
        #检验1检验该变量本身不显著--将该变量单独与目标变量做逻辑回归，如果在单变量回归的情况下系数p仍然较高，表明该变量本身显著性很低
        #检验2 该变量显著，但由于一定的线性相关性或多重共线性，导致该变量在多元回归不显著
        #先检验1的可能性，如果排除，再检验2
        y=df[target]
        X=df.drop(target,axis=1)
        print("     LR x.shape: ",X.shape)
        LR = sm.Logit(y, X).fit()
        # summary = LR.summary2()


        pvals = LR.pvalues.to_dict()
        params = LR.params.to_dict()

        # 发现有变量不显著，因此需要单独检验显著性
        varLargeP = {k: v for k, v in pvals.items() if v >= pValuer_threshold}
        # 小于阈值赋0，单变量回归重新就按
        pvals_largeP_univariate = {k: 0 for k, v in pvals.items() if v < pValuer_threshold}

        for col in varLargeP.keys():
            X_temp = df[col].copy().to_frame()
            X_temp['intercept'] = [1] * X_temp.shape[0]
            LR = sm.Logit(y, X_temp).fit()
            pvals_largeP_univariate[col] = LR.pvalues[col]
            if(pvals_largeP_univariate[col]>= pValuer_threshold):
                print("     col:{}单变量逻辑回归pValure大于阈值{},需要被剔除".format(col,pValuer_threshold))

        # 发现有变量的系数为正，因此需要单独检验正确性
        varPositive = [k for k, v in params.items() if v >= 0]

        ceof_univariate = {k: -1 for k, v in params.items() if v < 0}
        # print("len(varPositive):{}, len(ceof_univariate):{}".format(len(varPositive), len(ceof_univariate)))
        # print("varPositive: ", varPositive)
        # print("ceof_univariate: ", ceof_univariate)
        for col in varPositive:
            X_temp = df[col].copy().to_frame()
            X_temp['intercept'] = [1] * X_temp.shape[0]
            LR = sm.Logit(y, X_temp).fit()
            ceof_univariate[col] = LR.params[col]
            if (ceof_univariate[col] > 0):
                print("     col:{}单变量逻辑回归系数为正,需要被剔除".format(col))
        # self.reports.gen_summaryPng(summary, self.dataSet.modelData.report_lrSummaryPng)
        statistics.gen_pValueParafRreport(pvals, params, pvals_largeP_univariate, ceof_univariate,
                                                    report_pValuePara)
    def executor(self, df):
        print("[生成pValue报告]: 报告生成方式:{},用于p值检验".format(self.__ctx.task_train_lr.model_pValuePara_genType))
        # 生成model_pValuePara报告
        model_pValuePara=os.path.join(self.__ctx.task_train_lr.model_baseDir, self.__ctx.task_train_lr.model_pValuePara)

        #报告不存在，则重新生成,或者当设置为never则不生成
        if not os.path.exists(model_pValuePara):
            if self.__ctx.task_train_lr.model_pValuePara_genType != self.__ctx.reportSaveModel_never:
                self._pvalue_check(df,self.__ctx.train.data_label,self.__ctx.task_train_lr.para_pValuer_threshold,model_pValuePara)
        #报告存在
        else:
            print("     已有报告存在:",model_pValuePara)
            if self.__ctx.task_train_lr.model_pValuePara_genType == self.__ctx.reportSaveModel_always:
                self._pvalue_check(df,self.__ctx.train.data_label,self.__ctx.task_train_lr.para_pValuer_threshold,model_pValuePara)
        return df
###p值检验
class executor_pvalueCheckHandle(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_pvalueCheckHandle, self).__init__()
        self.__ctx = ctx
    def executor(self,df):
        print("[p值检验]")
        print("     step1:单变量回归显著性--将该变量单独与目标变量做逻辑回归，如果p>{}，显著性低，剔除".format(self.__ctx.task_train_lr.para_pValuer_threshold))
        print("     step2:多元回归检验显著性，如果p>{}，显著性低，剔除".format(self.__ctx.task_train_lr.para_pValuer_threshold))

        report_pValuePara=os.path.join(self.__ctx.task_train_lr.model_baseDir, self.__ctx.task_train_lr.model_pValuePara)
        assert os.path.exists(report_pValuePara), ("***can't find report_pValuePara file %s" % report_pValuePara)
        # 单变量&&多变量回归系数为正的值，单变量&&多变量回归p-value>0.1
        df_coef_pValue = pd.read_csv(report_pValuePara)
        del_coef = df_coef_pValue[df_coef_pValue["Coef_univariate"] > 0]["col"]
        del_pvaluer = df_coef_pValue[df_coef_pValue["Coef_univariate"] > self.__ctx.task_train_lr.para_pValuer_threshold][
            "col"]
        df.drop(del_coef, axis=1, inplace=True)
        df.drop(del_pvaluer, axis=1, inplace=True)
        print("     不符合p检验和系数检验的变量{}个,将被剔除,剔除后df.shape:{}".format((len(del_coef) + len(del_pvaluer)), df.shape))
        return df
###逐步回归
class executor_stepwiseRegressionHandle(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_stepwiseRegressionHandle, self).__init__()
        self.__ctx = ctx
    def executor(self,df):
        warnings.filterwarnings('ignore')
        print("[逐步回归]")
        print("     step1:将变量按IV由高到低排序")
        print("     step2:逐一添加变量,需保证pValue<{}且回归系数<0".format(self.__ctx.task_train_lr.para_pValuer_threshold))

        df_iv = pd.read_csv(os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_ivWoeCutoff), index_col=0)
        df_iv.sort_values(by="iv", ascending=False, inplace=True)
        sortedColsbyIV_list = [i for i in df_iv.index if i in df.columns]
        selected_var = []
        y = df[self.__ctx.train.data_label]

        for i, var in enumerate(sortedColsbyIV_list):
            try_vars = selected_var + [var]
            X_temp = df[try_vars].copy()
            X_temp['intercept'] = [1] * X_temp.shape[0]

            print("y.shape:{},X_temp.shape:{}".format(y.shape, X_temp.shape))

            LR = sm.Logit(y, X_temp).fit()
            # summary = LR.summary2()
            pvals, params = LR.pvalues, LR.params
            del params['intercept']
            if max(pvals) < self.__ctx.task_train_lr.para_pValuer_threshold and max(params) < 0:
                print("     逐步回归，合格变量{}/{}:{},max_pValuer:{},max_Ceof:{}\n".format(i, len(sortedColsbyIV_list), var,
                                                                                   max(pvals), max(params)))
                selected_var.append(var)
            else:
                print("     逐步回归，不合格变量{}/{}:{},max_pValuer:{},max_Ceof:{}\n".format(i, len(sortedColsbyIV_list), var,
                                                                                  max(pvals), max(params)))
        df.drop(df.columns.drop(selected_var + [self.__ctx.train.data_label]), axis=1, inplace=True)
        print("     筛选后变量数为:{}，df.shape:{} ".format(len(selected_var), df.shape))
        return df

###生成LR summary报告
class executor_genSummaryPngHandle(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_genSummaryPngHandle, self).__init__()
        self.__ctx = ctx
    def __genSummaryPng(self,df,target,reportFile):
        X_temp = df.drop(target, axis=1)
        X_temp['intercept'] = [1] * X_temp.shape[0]
        LR = sm.Logit(df[target], X_temp).fit()
        summary = LR.summary2()
        statistics.gen_summaryPng(summary, reportFile)
        print("     finally summary: ", summary)

    def executor(self, df):
        print("[生成回归summary报告] 生成方式:",self.__ctx.task_train_lr.model_lrSummary_png_genType)

        report_lrSummary_png=os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_lrSummary_png)
        # 报告不存在，则重新生成,或者当设置为never则不生成
        if not os.path.exists(report_lrSummary_png):
            if self.__ctx.task_train_lr.model_lrSummary_png_genType != self.__ctx.reportSaveModel_never:
              self.__genSummaryPng(df,self.__ctx.train.data_label,report_lrSummary_png)
        # 报告存在
        else:
            print("     已有报告存在:", report_lrSummary_png)
            if self.__ctx.task_train_lr.model_lrSummary_png_genType == self.__ctx.reportSaveModel_always:
                self.__genSummaryPng(df,self.__ctx.train.data_label,report_lrSummary_png)
        return df

### 训练
class executor_lrModelTrainHandle(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_lrModelTrainHandle, self).__init__()
        self.__ctx = ctx
        self._model = None

    def __smLRTrain(self,x_train, x_test, y_train, y_test):

        x_train['intercept'] = [1] * x_train.shape[0]
        LR = sm.Logit(y_train, x_train).fit()
        summary = LR.summary2()
        print("train summary:",summary)
        x_test['intercept'] = [1] * x_test.shape[0]

        y_pred = LR.predict(x_test)

        scores = performance.Prob2Score(y_pred,self.__ctx.task_train_lr.para_basePoint, self.__ctx.task_train_lr.para_odds)
        report_ks=os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.reports_ks)
        pic_ks=os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.reports_ks_png)
        ks = performance.KS(scores, y_test, report_ks, pic_ks)
        print("     模型名称:lr")
        print("     [KS]: ", ks)
        auc = roc_auc_score(y_test, y_pred)
        print("     [auc]: ", auc)
        # performance.confusionMatrixcal(y_test, y_pred)
        return

    def __modelTrainCVn(self,x_train, x_test, y_train, y_test,cvn):
        warnings.filterwarnings('ignore')
        #################  逻辑回归模型  #################
        lr = LogisticRegression(random_state=2020, tol=1e-6)  #
        auc = cross_val_score(lr, x_train, y_train, scoring='roc_auc', cv=cvn)
        print("     模型名称：{}".format("LogisticRegression", cvn))
        print("     训练集auc.mean():", auc.mean())

        lr.fit(x_train,y_train)
        lr_y_pred = lr.predict_proba(x_test)
        lr_scores = performance.Prob2Score(lr_y_pred[:,1], self.__ctx.task.basePoint,self.__ctx.task.odds)


        ksReport=os.path.join(self.__ctx.task_train_lr.reports_baseDir,self.__ctx.task_train_lr.reports_ks)
        ksPng = os.path.join(self.__ctx.task_train_lr.reports_baseDir, self.__ctx.task_train_lr.reports_ks_png)
        lr_auc = roc_auc_score(y_test, lr_y_pred[:,1])
        lr_ks = performance.KS(lr_scores, lr_auc,y_test,ksReport,ksPng,self.__ctx.task_train_lr.reports_ks_scores_bin)
        print("     测试集KS：",lr_ks)
        print("     测试集AUC：",lr_auc)
        coefFile = os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_coef)
        joblibFile = os.path.join(self.__ctx.task_train_lr.model_baseDir,self.__ctx.task_train_lr.model_joblib_pkl)
        self.__modelExport_lr(lr,x_test.columns.tolist(),coefFile,joblibFile)
        print("     ----------------------")
        #################  lgb模型  #################
        self._model = lgb.LGBMClassifier(n_jobs=self.__ctx.task.cpu_core)  # lgb
        # self.__calScore(gbm, x_train, y_train, cvn,"lgb")
        # gbm = LogisticRegression(random_state=2020, tol=1e-6)  # 逻辑回归模型
        auc = cross_val_score(self._model, x_train, y_train, scoring='roc_auc', cv=cvn)
        print("     模型名称：{}".format("lgb", cvn))
        print("     训练集auc.mean():", auc.mean())
        self._model.fit(x_train,y_train)
        lgb_y_pred = self._model.predict_proba(x_test)
        lgb_scores = performance.Prob2Score(lgb_y_pred[:,1], self.__ctx.task.basePoint,self.__ctx.task.odds)
        lgb_auc = roc_auc_score(y_test, lgb_y_pred[:, 1])
        lgb_ks = performance.KS(lgb_scores, lgb_auc,y_test)
        print("     测试集KS：", lgb_ks)
        print("     测试集AUC：", lgb_auc)
        print("     ----------------------")

    def __modelExport_lr(self, model,features,coeFile,joblibFile):
        coef=np.array(model.coef_).flatten().tolist()
        params_dict = dict(zip(features,coef))
        params_dict["lr.intercept"]=model.intercept_[0]
        params_dict["lr.C"] = model.C
        params_dict["lr.solver"] = model.solver
        params_dict["lr.penalty"] = model.penalty
        params_dict["lr.fit_intercept"] = model.fit_intercept
        params_dict["lr.intercept_scaling"] = model.intercept_scaling
        report = pd.DataFrame.from_dict(params_dict, orient='index')
        report.columns=["Coef"]
        report.to_csv(coeFile)
        print("     [生成权重文件]:",coeFile)
        joblib.dump(model, joblibFile)
        print("     [生成模型文件]:",joblibFile)

    def __trainLrGrideSearch(self,x_train, x_test, y_train, y_test,cvN):
        penaltys = ['l1', 'l2']
        Cs = [0.01, 0.1, 1, 10, 100, 1000]
        # 调优的参数集合，搜索网格为2x5，在网格上的交叉点进行搜索
        parameters = dict(penalty=penaltys, C=Cs)

        lr_penalty = LogisticRegression(solver='liblinear')
        grid = GridSearchCV(lr_penalty, parameters, cv=cvN, scoring='neg_log_loss', n_jobs=4)
        grid.fit(x_train, y_train)
        print("-grid.best_score_: ", -grid.best_score_)
        print("grid.best_params_: ", grid.best_params_)

        lr = LogisticRegression(solver='liblinear', penalty=grid.best_params_["penalty"],
                                C=grid.best_params_["C"], fit_intercept=True, intercept_scaling=1,
                                multi_class='ovr')
        lr.fit(x_train, y_train)

        print("     lr.intercept_:        ", lr.intercept_)
        print("     lr.coef_:             ", lr.coef_)
        print("     lr.C:                 ", lr.C)
        print("     lr.solver:            ", lr.solver)
        print("     lr.penalty：          ", lr.penalty)
        print("     lr.fit_intercept:     ", lr.fit_intercept)
        print("     lr.intercept_scaling: ", lr.intercept_scaling)

        y_pred = lr.predict_proba(x_test)
        scores = performance.Prob2Score(y_pred[:, 1], self.__ctx.task_train_lr.para_basePoint,
                                           self.__ctx.task_train_lr.para_odds)
        ks = performance.KS(scores, y_test, )
        print("     [roc_auc_score]: ", roc_auc_score(y_test, y_pred[:, 1]))
        print("     [ks]:",ks)

    def executor(self, df):
        warnings.filterwarnings('ignore')
        print("[模型训练] basePoint:{} odds:{}".format(self.__ctx.task.basePoint, self.__ctx.task.odds))
        x = df.drop([self.__ctx.train.data_label], axis=1)
        y = df[self.__ctx.train.data_label]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=22)
        self.__modelTrainCVn(x_train, x_test, y_train, y_test,5)
        # self.__trainLrGrideSearch(x_train, x_test, y_train, y_test,5)
        return df

