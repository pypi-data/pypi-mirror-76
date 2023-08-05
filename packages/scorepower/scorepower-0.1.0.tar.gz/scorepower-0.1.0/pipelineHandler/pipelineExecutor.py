
import abc
class pipelineExecutor(metaclass=abc.ABCMeta):
    def __init__(self):
        self.nextExecutor=None
    @abc.abstractmethod
    def executor(self):
        pass
