from datetime import  datetime
import abc
class modelValidation(metaclass=abc.ABCMeta):
    def __init__(self,model):
        self.__model=model

    def K_fold(self,numFold,isShuffle=True):
        pass