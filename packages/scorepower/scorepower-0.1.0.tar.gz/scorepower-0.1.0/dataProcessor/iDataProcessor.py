# coding=utf-8
import abc
from dataProcessor.featurTools import featureTools
class dataProcessor(featureTools,metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read_data(self):
        pass

    @abc.abstractmethod
    def data_fill(self,df):
        pass

    @abc.abstractmethod
    def feature_extract(self,df):
        pass

    @abc.abstractmethod
    def data_handler(self,saveFile):
        pass

