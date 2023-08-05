'''
@Author: your name
@Date: 2020-07-07 15:30:47
@LastEditTime: 2020-07-29 16:14:14
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /scorePower/src/scorePower.py
'''
from pipelineHandler.handlerFactory import cfgFactory
from defaultPipeline.lgbTrianPipeline import *
from defaultPipeline.lrTrianPipeline import *
from defaultPipeline.mlpTrianPipeline import *
from defaultPipeline.catboostTrianPipeline import *
from defaultPipeline.psiCalPipeline import *
class scorePower(pipelineCreator):
    def __init__(self,cfgFile=None):
        super(scorePower,self).__init__()
        self.__cfgFile=cfgFile
    def __getDefaultPipeline(self):
        ##trian task
        if self.__ctx.task.task == self.__ctx.taskSection_task_train:
            ## lr trian task
            if self.__ctx.train.method == self.__ctx.trainSection_method_lr:
                return lrTrianDefaultPipeline(self.__ctx)
            ## lgb trian task
            elif self.__ctx.train.method == self.__ctx.trainSection_method_lgb:
                return lgbTrianDefaultPipeline(self.__ctx)
            ## mlp trian task
            elif  self.__ctx.train.method == self.__ctx.trainSection_method_mlp:
                return mlpTrianDefaultPipeline(self.__ctx)
            ##catboost
            elif  self.__ctx.train.method == self.__ctx.trainSection_method_catboost:
                return catboostTrianDefaultPipeline(self.__ctx)
        elif self.__ctx.task.task == self.__ctx.taskSection_task_psi:
            return psiCalDefaultPipeline(self.__ctx)
        elif self.__ctx.task.task == self.__ctx.taskSection_task_predict:
            return  

    def run(self):
        ##采用配置文件的默认pipeline
        if self._pipelineStartExcutor == None:
            if self.__cfgFile == None:
                self.__ctx = cfgFactory().create()
            else:
                self.__ctx = cfgFactory(self.__cfgFile).create()
            
            self._pipelineStartExcutor = self.__getDefaultPipeline()._pipelineStartExcutor
        ##采用外部set的pipeline
        next = self._pipelineStartExcutor.nextExecutor
        print("■■■step1■■■")
        lastRst = self._pipelineStartExcutor.executor()
        ss = 2
        while (next != None):
            print("■■■step%s■■■" % ss)
            ss = ss + 1
            lastRst = next.executor(lastRst)
            next = next.nextExecutor
