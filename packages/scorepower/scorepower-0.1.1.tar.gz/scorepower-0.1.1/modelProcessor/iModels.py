# coding=utf-8
import abc

class models(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def model_pipline(self,*args,**kwargs):
        pass



