'''
@Author: your name
@Date: 2020-06-30 11:55:29
@LastEditTime: 2020-07-24 10:58:54
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /scorePower/src/pipelineHandler/pipelineCreator.py
'''
import abc
class pipelineCreator():
    def  __init__(self):
        self._pipelineStartExcutor=None
        self.create()
    @abc.abstractmethod
    def create(self):
        pass

    def setPipeLine(self, *arg, **kwargs):
        for i in range(len(arg) - 1):
            arg[i].nextExecutor=arg[i + 1]
        self._pipelineStartExcutor = arg[0]


