'''
@Author: your name
@Date: 2020-07-07 14:48:44
@LastEditTime: 2020-07-29 15:45:53
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /scorePower/src/defaultPipeline/lrTrianPipeline.py
'''
from pipelineHandler.executorHandler.executors import *
from pipelineHandler.executorHandler.lrTrainExecutors import *
from pipelineHandler.pipelineCreator import pipelineCreator
import os
class lrTrianDefaultPipeline(pipelineCreator):
    def __init__(self,ctx):
        self.__ctx=ctx
        super(lrTrianDefaultPipeline, self).__init__()

    def create(self):
        ###创建文件夹
        if not os.path.exists(self.__ctx.task_train_lr.reports_baseDir):
            os.makedirs(self.__ctx.task_train_lr.reports_baseDir)
        if not os.path.exists(self.__ctx.task_train_lr.model_baseDir):
            os.makedirs(self.__ctx.task_train_lr.model_baseDir)

        s1 = executor_trainDataReader(self.__ctx)  # 数据读取

        # 生成缺失率报告
        reports_missRate = os.path.join(self.__ctx.task_train_lr.reports_baseDir,
                                        self.__ctx.task_train_lr.reports_missRate)
        reports_highMissRate = os.path.join(self.__ctx.task_train_lr.reports_baseDir,
                                            self.__ctx.task_train_lr.reports_highMissRate)
        s2 = executor_genMissReport(self.__ctx,
                                    self.__ctx.task_train_lr.reports_missRate_genType,
                                    reports_missRate,
                                    reports_highMissRate,
                                    self.__ctx.task_train_lr.para_highMissThreshold)
        s3 = executor_dataFill(self.__ctx)  # 数据填充

        # 生成集中度报告
        reports_maxPercent = os.path.join(self.__ctx.task_train_lr.reports_baseDir,
                                          self.__ctx.task_train_lr.reports_maxPercent)
        s4 = executor_genMaxPercentageReport(self.__ctx,
                                             self.__ctx.task_train_lr.reports_maxPercent_genType,
                                             reports_maxPercent)
        # 集中度处理
        reports_maxPercent = os.path.join(self.__ctx.task_train_lr.reports_baseDir,
                                          self.__ctx.task_train_lr.reports_maxPercent)
        s5 = executor_maxPercentHandle(self.__ctx, reports_maxPercent,
                                       self.__ctx.task_train_lr.para_maxPercent,
                                       self.__ctx.task_train_lr.para_min_div_max_badrate)

        s6 = executor_binCutHandle(self.__ctx)  # 分箱
        s7 = executor_singleVarIVAnalysisHandle(self.__ctx)  # 单变量分析,删除低于和超过IV阈值的变量
        s8 = executor_genCorrReport(self.__ctx)  # 生成相关性报告
        s9 = executor_singleVarCorrAnalysisHandle(self.__ctx)  # 单变量相关性分析
        s10 = executor_genVifReport(self.__ctx)  # 生成vif报告
        s11 = executor_multicollinearityAnalysisHandle(self.__ctx)  # 多重共线性分析
        s12 = executor_genPValueReport(self.__ctx)  # 生成pValue报告
        s13 = executor_pvalueCheckHandle(self.__ctx)  # pValue检测
        s14 = executor_stepwiseRegressionHandle(self.__ctx)  # 逐步回归筛选变量
        s15 = executor_genSummaryPngHandle(self.__ctx)  # 生成回归summary报告
        s16 = executor_lrModelTrainHandle(self.__ctx)  # 模型训练

        # 生成特种重要性报告
        reports_featureImportance = os.path.join(self.__ctx.task_train_lr.reports_baseDir,
                                                 self.__ctx.task_train_lr.reports_featureImportance)
        reports_featureImportance_png = os.path.join(self.__ctx.task_train_lr.reports_baseDir,
                                                 self.__ctx.task_train_lr.reports_featureImportance_png)
        s17 = executor_genFeatureImportantReport(self.__ctx,
                                                 self.__ctx.task_train_lr.reports_featureImportance_genType,
                                                 reports_featureImportance,
                                                 reports_featureImportance_png,
                                                 s16._model)
        self.setPipeLine(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17)


