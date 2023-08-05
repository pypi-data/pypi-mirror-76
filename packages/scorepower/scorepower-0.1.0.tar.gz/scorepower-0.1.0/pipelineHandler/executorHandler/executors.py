from ..pipelineExecutor import pipelineExecutor
import  pandas as pd
from dataProcessor.dataReports import statistics
import lightgbm as lgb
from dataProcessor.binCut import ChiMerge
from modelProcessor.performance import performance
import os,gc,pickle
from sklearn.model_selection import train_test_split,GridSearchCV
###数据获取
class executor_trainDataReader(pipelineExecutor):
    def __init__(self,ctx,removeList=None):
        self.__ctx=ctx
        self.__removeList=removeList
    def executor(self):
        print("[读取数据]:",self.__ctx.train.data_path)
        assert os.path.exists(self.__ctx.train.data_path), ("***can't find data file %s" % self.__ctx.train.data_path)
        df=pd.read_csv(self.__ctx.train.data_path)
        assert (self.__ctx.train.data_label in df.columns), ("***can't find label %s" % self.__ctx.train.data_label)

        print("     total shape:", df.shape)
        df.dropna(subset=[self.__ctx.train.data_label], inplace=True)
        print("     label dropna shape:", df.shape)

        label_good_cnt = df[df[self.__ctx.train.data_label] == int(self.__ctx.train.data_label_good)].shape[0]
        label_bad_cnt = df[df[self.__ctx.train.data_label] == int(self.__ctx.train.data_label_bad)].shape[0]
        labe_total = df.shape[0]

        print("     label_good_cnt: {},good_ratio: {}".format(label_good_cnt, label_good_cnt / labe_total))
        print("     label_bad_cnt: {},bad_ratio: {}".format(label_bad_cnt, label_bad_cnt / labe_total))
        return df

###生成缺失值报告
class executor_genMissReport(pipelineExecutor):
    def __init__(self,ctx,reports_missRate_genType,reportFile,highMissReportFile,highMissThreshold):
        self.__ctx = ctx
        self.__reports_missRate_genType = reports_missRate_genType
        self.__missReport = reportFile
        self.__highMissReport = highMissReportFile
        self.__highMissThreshold = highMissThreshold

    def executor(self,df):
        print("[生成缺失值报告] 生成方式:", self.__reports_missRate_genType)
        if not os.path.exists(self.__missReport):
            if self.__reports_missRate_genType != self.__ctx.reportSaveModel_never:
                statistics.gen_missingReprot_feature(df, self.__missReport,self.__highMissReport,self.__highMissThreshold)
        else:
            print("     已有报告存在:",self.__missReport)
            if self.__ctx.task_train_lr.reports_missRate_genType == self.__ctx.reportSaveModel_always:
                statistics.gen_missingReprot_feature(df, self.__missReport,self.__highMissReport,self.__highMissThreshold)
        return df

###数据填充
class executor_dataFill(pipelineExecutor):
    def __init__(self,ctx):
        self.__ctx = ctx
    def executor(self,df):
        print("[数据填充]...")
        df.fillna(0, inplace=True)
        return df

###数据集中度报告
class executor_genMaxPercentageReport(pipelineExecutor):
    def __init__(self,ctx,reports_maxPercent_genType,reports_maxPercent):
        super(executor_genMaxPercentageReport,self).__init__()
        self.__ctx = ctx
        self.__reports_maxPercent_genType=reports_maxPercent_genType
        self.__reports_maxPercent=reports_maxPercent

    def executor(self,df):
        print("[生成数据集中度报告] 生成方式:", self.__reports_maxPercent_genType)
        if not os.path.exists(self.__reports_maxPercent):
            if self.__reports_maxPercent_genType != self.__ctx.reportSaveModel_never:
                statistics.gen_maxPercentageVariableReports(df, self.__reports_maxPercent,self.__ctx.train.data_label)
        else:
            print("     已有报告存在:",self.__reports_maxPercent)
            if self.__reports_maxPercent_genType == self.__ctx.reportSaveModel_always:
                statistics.gen_maxPercentageVariableReports(df, self.__reports_maxPercent,self.__ctx.train.data_label)

        return df

###数据集中度处理
class executor_maxPercentHandle(pipelineExecutor):
    def __init__(self,ctx,reports_maxPercent,para_maxPercent,para_min_div_max_badrate):
        super(executor_maxPercentHandle,self).__init__()
        self.__ctx = ctx
        self.__reports_maxPercent=reports_maxPercent
        self.__para_maxPercent = para_maxPercent
        self.__para_min_div_max_badrate = para_min_div_max_badrate

    def executor(self,df):
        print("[数据集中度处理]:检查数据集中度，删除集中度>{}，且少数/多数坏样本率>{}不显著的变量".format(self.__para_maxPercent,
                                                                      self.__para_min_div_max_badrate))

        df_maxpercent = pd.read_csv(self.__reports_maxPercent)
        df_maxpercent = df_maxpercent[df_maxpercent["max_percent"] >= self.__para_maxPercent]
        df_maxpercent_del = df_maxpercent[
            df_maxpercent["min_div_max_badrate"] < self.__para_min_div_max_badrate]
        df_maxpercent_keep = df_maxpercent[
            df_maxpercent["min_div_max_badrate"] >= self.__para_min_div_max_badrate].cols.tolist()
        del_maxpercent_cols = df_maxpercent_del.cols
        print("     删除{}个变量:{}".format(len(del_maxpercent_cols), del_maxpercent_cols.values.tolist()))
        df.drop(del_maxpercent_cols, axis=1, inplace=True)
        print("     删除后shape:", df.shape)

        return df

###数据异常值报告
class executor_genOutlierReport(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_genOutlierReport,self).__init__()
        self.__ctx = ctx

    def executor(self,df):
        #数据填充
        print("[生成异常值数据报告] 生成方式:")

        # self.reports.gen_outlierReport_quantile(df.drop(["label","today_overdue_days"],axis=1),5,"./dataReports/outlierReport.csv")
        # self.reports.gen_outlierReport_std(df.drop(["label", "today_overdue_days"], axis=1),"./dataReports/outlierStdReport.csv")

        return df

###生成变量相关性报告
class executor_genCorrReport(pipelineExecutor):
    def __init__(self, ctx):
        super(executor_genCorrReport, self).__init__()
        self.__ctx = ctx

    def executor(self, df):
        print("[生成变量相关性报告]: corr报告生成方式:{}".format(self.__ctx.task_train_lr.reports_corr_genType))
        # 生成corr报告
        reports_corr=os.path.join(self.__ctx.task_train_lr.reports_baseDir, self.__ctx.task_train_lr.reports_corr)
        reports_highCorr=os.path.join(self.__ctx.task_train_lr.reports_baseDir, self.__ctx.task_train_lr.reports_highCorr)
        #报告不存在，则重新生成,或者当设置为never则不生成
        if not os.path.exists(reports_corr):
            if self.__ctx.task_train_lr.reports_corr_genType != self.__ctx.reportSaveModel_never:
                statistics.gen_corrReport(df, reports_corr,reports_highCorr,self.__ctx.task_train_lr.para_highCorrThreshhold_max,self.__ctx.task_train_lr.para_highCorrThreshhold_min)
        #报告存在
        else:
            print("     已有报告存在:", reports_corr)
            if self.__ctx.task_train_lr.reports_corr_genType == self.__ctx.reportSaveModel_always:
                statistics.gen_corrReport(df, reports_corr,reports_highCorr,self.__ctx.task_train_lr.para_highCorrThreshhold_max,self.__ctx.task_train_lr.para_highCorrThreshhold_min)
        return df

###生成特征重要性报告
class executor_genFeatureImportantReport(pipelineExecutor):
    def __init__(self, ctx,reports_featureImportance_genType,reports_importance,reports_importance_png,model=None):
        super(executor_genFeatureImportantReport, self).__init__()
        self.__ctx = ctx
        self.__model = model
        self.__reports_featureImportance_genType= reports_featureImportance_genType
        self.__reports_importance = reports_importance
        self.__reports_importance_png = reports_importance_png
    def executor(self, df):
        print("[生成特种重要性报告]: 报告生成方式:{}".format(self.__reports_featureImportance_genType))
        x = df.drop([self.__ctx.train.data_label], axis=1)
        y = df[self.__ctx.train.data_label]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=22)

        # 报告不存在，则重新生成,或者当设置为never则不生成
        if not os.path.exists(self.__reports_importance):
            if self.__reports_featureImportance_genType != self.__ctx.reportSaveModel_never:
                x = df.drop([self.__ctx.train.data_label], axis=1)
                y = df[self.__ctx.train.data_label]
                if self.__model == None:
                    self.__model = lgb.LGBMClassifier()
                self.__model.fit(x_train, y_train)
                statistics.gen_featureImportanceReport(x.columns, self.__model, self.__reports_importance,self.__reports_importance_png)
        # 报告存在
        else:
            print("     已有报告存在:", self.__reports_importance)
            if self.__reports_featureImportance_genType == self.__ctx.reportSaveModel_always:
                x = df.drop([self.__ctx.train.data_label], axis=1)
                y = df[self.__ctx.train.data_label]
                if self.__model == None:
                    self.__model = lgb.LGBMClassifier()
                self.__model.fit(x_train, y_train)
                statistics.gen_featureImportanceReport(x.columns, self.__model, self.__reports_importance,self.__reports_importance_png)
        return df

