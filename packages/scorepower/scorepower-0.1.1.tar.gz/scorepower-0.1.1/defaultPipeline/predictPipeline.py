'''
@Author: your name
@Date: 2020-08-06 19:20:40
@LastEditTime: 2020-08-06 19:53:12
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /scorePower/src/defaultPipeline/predictPipeline.py
'''
from pipelineHandler.executorHandler.psiExecutors import *
from pipelineHandler.pipelineCreator import pipelineCreator
import os
class predictDefaultPipeline(pipelineCreator):
    def __init__(self,ctx):
        self.__ctx = ctx
        super(predictDefaultPipeline,self).__init__()

    def create(self):
        ###创建文件夹
        if not os.path.exists(self.__ctx.task_psi.reports_baseDir):
            os.makedirs(self.__ctx.task_psi.reports_baseDir)

        ##data获取
        s1 = executor_psiDataReader(self.__ctx)
        ##计算psi
        psiReport = os.path.join(self.__ctx.task_psi.reports_baseDir, self.__ctx.task_psi.reports_psi)
        psiReportPng = os.path.join(self.__ctx.task_psi.reports_baseDir, self.__ctx.task_psi.reports_psi_png)
        s2 = executor_psiCalc(self.__ctx,psiReport,psiReportPng)
        self.setPipeLine(s1,s2)
