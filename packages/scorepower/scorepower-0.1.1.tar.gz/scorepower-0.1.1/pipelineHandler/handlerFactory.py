'''
@Author: your name
@Date: 2020-06-30 11:53:19
@LastEditTime: 2020-07-29 16:14:51
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /scorePower/src/pipelineHandler/handlerFactory.py
'''
# coding=utf-8
from config.config import config,para_cfgHandl
from config.parameters import cfgConst
import abc,sys,argparse,os

class iCreateFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self):
        pass
class cfgFactory(iCreateFactory):
    def __init__(self,cfgFile=None):
        self.__cfgfile=self.__get_configfile(cfgFile)
    def create(self):
        paraCfg = para_cfgHandl(self.__cfgfile)
        return  config(paraCfg)

    def __get_configfile(self,configFile=None):
        if configFile == None:
            parser = argparse.ArgumentParser(description='scorePower model for A/B card ')
            parser.add_argument('-c', "--cfgFile", help='the file path of config for scorePower')

            args = parser.parse_args()
            config_file = args.cfgFile
        else:
            config_file=configFile
        assert (config_file != None), "***args -c or --cfgFile is empty"
        assert os.path.exists(config_file), ("***can't find file %s" % config_file)
        return config_file
class predictFactory(iCreateFactory):
    def __init__(self,ctx):
        self.__ctx=ctx
    def create(self):
        sys.path.append(self.__ctx.inference_dir)
        module = __import__(self.__ctx.inference_file)
        predictor = getattr(module, self.__ctx.inference_class)()
        return predictor

class trainFactory(iCreateFactory):
    def __init__(self,ctx):
        self.__ctx=ctx
    def create(self,startHandler):
        return startHandler


class handlerFactory(iCreateFactory):
    def __init__(self,cfgfile):
        self.__cfgFile=cfgfile
    def create(self,startHandler):
        handler=None
        # create context from configfile
        ctx =cfgFactory(self.__cfgFile).create()

        #create train task
        if(ctx.task.task==cfgConst.task_train):
            handler = trainFactory(ctx).create(startHandler)

        return handler