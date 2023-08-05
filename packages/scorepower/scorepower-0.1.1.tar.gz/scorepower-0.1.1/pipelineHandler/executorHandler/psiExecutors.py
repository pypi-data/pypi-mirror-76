from ..pipelineExecutor import pipelineExecutor
import os
import pandas as pd
import joblib
from modelProcessor.performance import performance
###数据获取
class executor_psiDataReader(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_psiDataReader, self).__init__()
        self.__ctx=ctx
    def executor(self):
        print("[读取数据]:",self.__ctx.task_psi.psi_data1,self.__ctx.task_psi.psi_data2)
        assert os.path.exists(self.__ctx.task_psi.psi_data1), ("***can't find data file %s" % self.__ctx.task_psi.psi_data1)
        assert os.path.exists(self.__ctx.task_psi.psi_data2), ("***can't find data file %s" % self.__ctx.task_psi.psi_data2)
        df1 = pd.read_csv(self.__ctx.task_psi.psi_data1)
        df2 = pd.read_csv(self.__ctx.task_psi.psi_data2)
        return df1,df2
##psi计算
class executor_psiCalc(pipelineExecutor):
    def __init__(self,ctx,psiReport,psiReportPng):
        super(executor_psiCalc, self).__init__()
        self.__ctx=ctx
        self.__psiReport=psiReport
        self.__psiReportPng=psiReportPng

    def executor(self,df):
        print("[psi计算]:加载模型：",self.__ctx.task_psi.psi_model_pkl)
        assert os.path.exists(self.__ctx.task_psi.psi_model_pkl), ("***can't find data file %s" % self.__ctx.task_psi.psi_model_pkl)
        self.__model = joblib.load(self.__ctx.task_psi.psi_model_pkl)
        
        performance.psi_calculation2Set(self.__model,
                                        self.__psiReport,
                                        self.__psiReportPng,
                                        df[0],
                                        df[1],
                                        self.__ctx.task_psi.psi_data1_name,
                                        self.__ctx.task_psi.psi_data2_name,
                                        self.__ctx.task.basePoint,
                                        self.__ctx.task.odds,
                                        self.__ctx.task_psi.psi_bins)

        return df