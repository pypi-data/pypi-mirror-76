from pipelineHandler.executorHandler.executors import *
from pipelineHandler.executorHandler.mlpTrainExecutors import *
from pipelineHandler.pipelineCreator import pipelineCreator
import os
class mlpTrianDefaultPipeline(pipelineCreator):
    def __init__(self,ctx):
        self.__ctx = ctx
        super(mlpTrianDefaultPipeline, self).__init__()

    def create(self):
        ###创建文件夹
        if not os.path.exists(self.__ctx.task_train_mlp.reports_baseDir):
            os.makedirs(self.__ctx.task_train_mlp.reports_baseDir)
        if not os.path.exists(self.__ctx.task_train_mlp.model_baseDir):
            os.makedirs(self.__ctx.task_train_mlp.reports_baseDir)

        # 数据读取
        s1 = executor_trainDataReader(self.__ctx)

        # 生成缺失率报告
        reports_missRate = os.path.join(self.__ctx.task_train_mlp.reports_baseDir,
                                        self.__ctx.task_train_mlp.reports_missRate)
        reports_highMissRate = os.path.join(self.__ctx.task_train_mlp.reports_baseDir,
                                            self.__ctx.task_train_mlp.reports_highMissRate)
        s2 = executor_genMissReport(self.__ctx,
                                    self.__ctx.task_train_mlp.reports_missRate_genType,
                                    reports_missRate,
                                    reports_highMissRate,
                                    self.__ctx.task_train_mlp.para_highMissThreshold)

        s3 = executor_dataFill(self.__ctx)  # 数据填充

        # 生成集中度报告
        reports_maxPercent = os.path.join(self.__ctx.task_train_mlp.reports_baseDir,
                                          self.__ctx.task_train_mlp.reports_maxPercent)
        s4 = executor_genMaxPercentageReport(self.__ctx,
                                             self.__ctx.task_train_mlp.reports_maxPercent_genType,
                                             reports_maxPercent)
        # 集中度处理
        reports_maxPercent = os.path.join(self.__ctx.task_train_mlp.reports_baseDir,
                                          self.__ctx.task_train_mlp.reports_maxPercent)
        s5 = executor_maxPercentHandle(self.__ctx, reports_maxPercent,
                                       self.__ctx.task_train_mlp.para_maxPercent,
                                       self.__ctx.task_train_mlp.para_min_div_max_badrate)

        s6 = executor_mlpModelTrainHandle(self.__ctx)  # 模型训练
        # 生成特种重要性报告
        reports_featureImportance = os.path.join(self.__ctx.task_train_mlp.reports_baseDir,
                                                 self.__ctx.task_train_mlp.reports_featureImportance)

        s7 = executor_genFeatureImportantReport(self.__ctx,
                                                self.__ctx.task_train_mlp.reports_featureImportance_genType,
                                                reports_featureImportance)
        self.setPipeLine(s1, s2, s3, s4, s5, s6, s7)

