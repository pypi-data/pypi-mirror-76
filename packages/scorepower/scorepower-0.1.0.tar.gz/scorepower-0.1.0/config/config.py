# coding=utf-8
import configparser,os
import  abc
from .parameters import cfgPara
 
##抽象类，定义参数操作方法接口
class Ipara_op(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_para(self,name):
        pass

#TODO
#从命令行获取参数
class para_cmdHandl(Ipara_op):
    def __init__(self, args):
        self.args_string = args
    def get_para(self, name):
        pass

#从配置文件获取参数
class para_cfgHandl(Ipara_op):
    def __init__(self,cfgfile):
        self.__cfgPara=configparser.ConfigParser()
        self.__cfgPara.read(cfgfile)
    def get_para(self,name,section_name="task"):
        return self.__cfgPara.get(section_name, name)



class config(cfgPara):
    def __init__(self,cfgfile_handl):
        self._cfgPara=cfgfile_handl
        self.get_all_paras()

     #获取参数，
    def get_all_paras(self):
        print("*****************----[start get all config parameters]-----*****************")
        #*****************----task section----*****************#  cpu_core
        print("----------task section----------")
        cfgPara.task.task = self._cfgPara.get_para("task",cfgPara.task.section)
        print("[config] ：cfgPara.task.task:",cfgPara.task.task )
        cfgPara.task.cpu_core = int(self._cfgPara.get_para("cpu.cores", cfgPara.task.section))
        print("[config] ：cfgPara.task.cpu_core:", cfgPara.task.cpu_core)
        cfgPara.task.basePoint = float(self._cfgPara.get_para("basePoint", cfgPara.task.section))
        print("[config] ：cfgPara.task.basePoint:", cfgPara.task.basePoint)
        cfgPara.task.odds = float(self._cfgPara.get_para("odds", cfgPara.task.section))
        print("[config] ：cfgPara.train.odds:", cfgPara.task.odds)
        # *****************----train section----*****************#
        print("----------train section----------")
        cfgPara.train.method = self._cfgPara.get_para("method", cfgPara.train.section)
        print("[config] ：cfgPara.train.method：", cfgPara.train.method)
        cfgPara.train.data_path = self._cfgPara.get_para("data.path", cfgPara.train.section)
        print("[config] ：cfgPara.data.data_path:", cfgPara.train.data_path)
        cfgPara.train.data_label = self._cfgPara.get_para("data.label", cfgPara.train.section)
        print("[config] ：cfgPara.data.data_label:", cfgPara.train.data_label)
        cfgPara.train.data_label_good = self._cfgPara.get_para("data.label.good", cfgPara.train.section)
        print("[config] ：cfgPara.data.data_label_good:", cfgPara.train.data_label_good)
        cfgPara.train.data_label_bad = self._cfgPara.get_para("data.label.bad", cfgPara.train.section)
        print("[config] ：cfgPara.data.data_label_bad:", cfgPara.train.data_label_bad)
        # *****************----task_train_lr section----*****************#
        print("------task_train_lr section------")
        cfgPara.task_train_lr.reports_baseDir = self._cfgPara.get_para("lr.reports.baseDir", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_baseDir：", cfgPara.task_train_lr.reports_baseDir)

        cfgPara.task_train_lr.reports_missRate = self._cfgPara.get_para("lr.reports.missRate", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_missRate:", cfgPara.task_train_lr.reports_missRate)
        cfgPara.task_train_lr.reports_highMissRate = self._cfgPara.get_para("lr.reports.highMissRate",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_highMissRate:", cfgPara.task_train_lr.reports_highMissRate)
        cfgPara.task_train_lr.reports_missRate_genType = self._cfgPara.get_para("lr.reports.missRate.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_missRate_genType:", cfgPara.task_train_lr.reports_missRate_genType)

        cfgPara.task_train_lr.reports_maxPercent = self._cfgPara.get_para("lr.reports.maxPercent",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_maxPercent:",cfgPara.task_train_lr.reports_maxPercent)
        cfgPara.task_train_lr.reports_maxPercent_genType = self._cfgPara.get_para("lr.reports.maxPercent.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_maxPercent_genType:", cfgPara.task_train_lr.reports_maxPercent_genType)

        cfgPara.task_train_lr.reports_corr = self._cfgPara.get_para("lr.reports.corr",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_corr:", cfgPara.task_train_lr.reports_corr)
        cfgPara.task_train_lr.reports_highCorr = self._cfgPara.get_para("lr.reports.highCorr", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_highCorr:", cfgPara.task_train_lr.reports_highCorr)
        cfgPara.task_train_lr.reports_corr_genType = self._cfgPara.get_para("lr.reports.corr.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_corr_genType:", cfgPara.task_train_lr.reports_corr_genType)

        cfgPara.task_train_lr.reports_vif = self._cfgPara.get_para("lr.reports.vif", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_vif::", cfgPara.task_train_lr.reports_vif)
        cfgPara.task_train_lr.reports_vif_genType = self._cfgPara.get_para("lr.reports.vif.genType", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_vif_genType", cfgPara.task_train_lr.reports_vif_genType)

        cfgPara.task_train_lr.reports_featureImportance = self._cfgPara.get_para("lr.reports.featureImportance", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_featureImportance:", cfgPara.task_train_lr.reports_featureImportance)
        cfgPara.task_train_lr.reports_featureImportance_png = self._cfgPara.get_para("lr.reports.featureImportance.png",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_featureImportance_png:",cfgPara.task_train_lr.reports_featureImportance_png)
        cfgPara.task_train_lr.reports_featureImportance_genType = self._cfgPara.get_para("lr.reports.featureImportance.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_featureImportance_genType:",cfgPara.task_train_lr.reports_featureImportance_genType)

        cfgPara.task_train_lr.reports_ks = self._cfgPara.get_para("lr.reports.ks",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_ks:",cfgPara.task_train_lr.reports_ks)
        cfgPara.task_train_lr.reports_ks_png = self._cfgPara.get_para("lr.reports.ks.png", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_ks_png:", cfgPara.task_train_lr.reports_ks_png)
        cfgPara.task_train_lr.reports_ks_scores_bin = int(self._cfgPara.get_para("lr.reports.ks.scores.bin",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.reports_ks_scores_bin:", cfgPara.task_train_lr.reports_ks_scores_bin)
        cfgPara.task_train_lr.reports_ks_genType = self._cfgPara.get_para("lr.reports.ks.genType", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_ks_genType:", cfgPara.task_train_lr.reports_ks_genType)

        cfgPara.task_train_lr.reports_confusionMatrix_Png = self._cfgPara.get_para("lr.reports.confusionMatrix.Png", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_confusionMatrix_Png:", cfgPara.task_train_lr.reports_confusionMatrix_Png)
        cfgPara.task_train_lr.reports_confusionMatrix_genType = self._cfgPara.get_para("lr.reports.confusionMatrix.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.reports_confusionMatrix_genType:",cfgPara.task_train_lr.reports_confusionMatrix_genType)

        cfgPara.task_train_lr.model_baseDir = self._cfgPara.get_para("lr.model.baseDir",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_baseDir:",cfgPara.task_train_lr.model_baseDir)

        cfgPara.task_train_lr.model_ivParaPickle = self._cfgPara.get_para("lr.model.ivParaPickle", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_ivParaPickle:", cfgPara.task_train_lr.model_ivParaPickle)
        cfgPara.task_train_lr.model_woeParaPickle = self._cfgPara.get_para("lr.model.woeParaPickle",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_woeParaPickle:", cfgPara.task_train_lr.model_woeParaPickle)
        cfgPara.task_train_lr.model_cutoffParaPickle = self._cfgPara.get_para("lr.model.cutoffParaPickle",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_cutoffParaPickle:", cfgPara.task_train_lr.model_cutoffParaPickle)

        cfgPara.task_train_lr.model_ivWoeCutoff = self._cfgPara.get_para("lr.model.ivWoeCutoff", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_ivWoeCutoff:", cfgPara.task_train_lr.model_ivWoeCutoff)
        cfgPara.task_train_lr.model_singBinPcn = self._cfgPara.get_para("lr.model.singBinPcn",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_singBinPcn:", cfgPara.task_train_lr.model_singBinPcn)
        cfgPara.task_train_lr.model_singBinPcnOverThreshold = self._cfgPara.get_para("lr.model.singBinPcnOverThreshold", cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_singBinPcnOverThreshold:",cfgPara.task_train_lr.model_singBinPcnOverThreshold)
        cfgPara.task_train_lr.model_ivWoeCutoff_genType = self._cfgPara.get_para("lr.model.ivWoeCutoff.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_ivWoeCutoff_genType:",cfgPara.task_train_lr.model_ivWoeCutoff_genType)

        cfgPara.task_train_lr.model_pValuePara = self._cfgPara.get_para("lr.model.pValuePara",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_pValuePara:", cfgPara.task_train_lr.model_pValuePara)
        cfgPara.task_train_lr.model_pValuePara_genType = self._cfgPara.get_para("lr.model.pValuePara.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_pValuePara_genType:", cfgPara.task_train_lr.model_pValuePara_genType)

        cfgPara.task_train_lr.model_lrSummary_png = self._cfgPara.get_para("lr.model.lrSummary.png",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_lrSummary_png:", cfgPara.task_train_lr.model_lrSummary_png)
        cfgPara.task_train_lr.model_lrSummary_png_genType = self._cfgPara.get_para("lr.model.lrSummary.png.genType",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_lrSummary_png_genType:", cfgPara.task_train_lr.model_lrSummary_png_genType)

        cfgPara.task_train_lr.model_coef = self._cfgPara.get_para("lr.model.coef",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_coef:", cfgPara.task_train_lr.model_coef)
        cfgPara.task_train_lr.model_joblib_pkl = self._cfgPara.get_para("lr.model.joblib_pkl",cfgPara.task_train_lr.section)
        print("[config] ：cfgPara.task_train_lr.model_joblib_pkl:",cfgPara.task_train_lr.model_joblib_pkl)

        cfgPara.task_train_lr.para_highMissThreshold = float(self._cfgPara.get_para("lr.para.highMissThreshold",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_highMissThreshold:", cfgPara.task_train_lr.para_highMissThreshold)
        cfgPara.task_train_lr.para_maxPercent = float(self._cfgPara.get_para("lr.para.maxPercent",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_maxPercent:",cfgPara.task_train_lr.para_maxPercent)
        cfgPara.task_train_lr.para_min_div_max_badrate = float(self._cfgPara.get_para("lr.para.min_div_max_badrate", cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_min_div_max_badrate:", cfgPara.task_train_lr.para_min_div_max_badrate)
        cfgPara.task_train_lr.para_ivThreshold_low = float(self._cfgPara.get_para("lr.para.ivThreshold_low",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_ivThreshold_low:",cfgPara.task_train_lr.para_ivThreshold_low)
        cfgPara.task_train_lr.para_ivThreshold_high = float(self._cfgPara.get_para("lr.para.ivThreshold_high",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_ivThreshold_high:", cfgPara.task_train_lr.para_ivThreshold_high)
        cfgPara.task_train_lr.para_singBin_maxPercentThreshHold =float( self._cfgPara.get_para("lr.para.singBin_maxPercentThreshHold",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_ivThreshold_high:",cfgPara.task_train_lr.para_singBin_maxPercentThreshHold)
        cfgPara.task_train_lr.para_highCorrThreshhold_max = float(self._cfgPara.get_para("lr.para.highCorrThreshhold_max", cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_highCorrThreshhold_max:",cfgPara.task_train_lr.para_highCorrThreshhold_max)
        cfgPara.task_train_lr.para_highCorrThreshhold_min = float(self._cfgPara.get_para("lr.para.highCorrThreshhold_min",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_highCorrThreshhold_min:",cfgPara.task_train_lr.para_highCorrThreshhold_min)
        cfgPara.task_train_lr.para_vif_threshold = float(self._cfgPara.get_para("lr.para.vif_threshold",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_highCorrThreshhold_min:",cfgPara.task_train_lr.para_vif_threshold)
        cfgPara.task_train_lr.para_pValuer_threshold = float(self._cfgPara.get_para("lr.para.pValuer_threshold",cfgPara.task_train_lr.section))
        print("[config] ：cfgPara.task_train_lr.para_pValuer_threshold:",cfgPara.task_train_lr.para_pValuer_threshold)

        # *****************----task_train_lgb section----*****************#
        print("------task_train_lgb section------")
        cfgPara.task_train_lgb.reports_baseDir = self._cfgPara.get_para("lgb.reports.baseDir",cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_baseDir：", cfgPara.task_train_lgb.reports_baseDir)

        cfgPara.task_train_lgb.reports_missRate = self._cfgPara.get_para("lgb.reports.missRate", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_missRate:", cfgPara.task_train_lgb.reports_missRate)
        cfgPara.task_train_lgb.reports_highMissRate = self._cfgPara.get_para("lgb.reports.highMissRate",cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_highMissRate:", cfgPara.task_train_lgb.reports_highMissRate)
        cfgPara.task_train_lgb.reports_missRate_genType = self._cfgPara.get_para("lgb.reports.missRate.genType", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_missRate_genType:", cfgPara.task_train_lgb.reports_missRate_genType)

        cfgPara.task_train_lgb.reports_maxPercent = self._cfgPara.get_para("lgb.reports.maxPercent", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_maxPercent:", cfgPara.task_train_lgb.reports_maxPercent)
        cfgPara.task_train_lgb.reports_maxPercent_genType = self._cfgPara.get_para("lgb.reports.maxPercent.genType", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_maxPercent_genType:", cfgPara.task_train_lgb.reports_maxPercent_genType)

        cfgPara.task_train_lgb.reports_corr = self._cfgPara.get_para("lgb.reports.corr", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_corr:", cfgPara.task_train_lgb.reports_corr)
        cfgPara.task_train_lgb.reports_highCorr = self._cfgPara.get_para("lgb.reports.highCorr", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_highCorr:", cfgPara.task_train_lgb.reports_highCorr)
        cfgPara.task_train_lgb.reports_corr_genType = self._cfgPara.get_para("lgb.reports.corr.genType", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_corr_genType:", cfgPara.task_train_lgb.reports_corr_genType)

        cfgPara.task_train_lgb.reports_ks = self._cfgPara.get_para("lgb.reports.ks", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_ks:", cfgPara.task_train_lgb.reports_ks)
        cfgPara.task_train_lgb.reports_ks_png = self._cfgPara.get_para("lgb.reports.ks.png",cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_ks_png:", cfgPara.task_train_lgb.reports_ks_png)
        cfgPara.task_train_lgb.reports_ks_scores_bin = int(self._cfgPara.get_para("lgb.reports.ks.scores.bin", cfgPara.task_train_lgb.section))
        print("[config] ：cfgPara.task_train_lgb.reports_ks_scores_bin:", cfgPara.task_train_lgb.reports_ks_scores_bin)

        cfgPara.task_train_lgb.reports_ks_genType = self._cfgPara.get_para("lgb.reports.ks.genType",cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_ks_genType:", cfgPara.task_train_lgb.reports_ks_genType)

        cfgPara.task_train_lgb.reports_featureImportance = self._cfgPara.get_para("lgb.reports.featureImportance",cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_featureImportance:",cfgPara.task_train_lr.reports_featureImportance)
        cfgPara.task_train_lgb.reports_featureImportance_png = self._cfgPara.get_para("lgb.reports.featureImportance.png",cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_featureImportance_png:",cfgPara.task_train_lr.reports_featureImportance_png)
        cfgPara.task_train_lgb.reports_featureImportance_genType = self._cfgPara.get_para("lgb.reports.featureImportance.genType", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.reports_featureImportance_genType:",cfgPara.task_train_lr.reports_featureImportance_genType)

        cfgPara.task_train_lgb.para_highMissThreshold = float(self._cfgPara.get_para("lgb.para.highMissThreshold", cfgPara.task_train_lgb.section))
        print("[config] ：cfgPara.task_train_lgb.para_highMissThreshold:", cfgPara.task_train_lgb.para_highMissThreshold)
        cfgPara.task_train_lgb.para_maxPercent = float(self._cfgPara.get_para("lgb.para.maxPercent", cfgPara.task_train_lgb.section))
        print("[config] ：cfgPara.task_train_lgb.para_maxPercent:", cfgPara.task_train_lgb.para_maxPercent)
        cfgPara.task_train_lgb.para_min_div_max_badrate = float(self._cfgPara.get_para("lgb.para.min_div_max_badrate", cfgPara.task_train_lgb.section))
        print("[config] ：cfgPara.task_train_lgb.para_min_div_max_badrate:",cfgPara.task_train_lgb.para_min_div_max_badrate)

        cfgPara.task_train_lgb.model_baseDir = self._cfgPara.get_para("lgb.model.baseDir", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.model_baseDir:", cfgPara.task_train_lgb.model_baseDir)
        cfgPara.task_train_lgb.model_trian_type = (self._cfgPara.get_para("lgb.model.trian.type", cfgPara.task_train_lgb.section))
        print("[config] ：cfgPara.task_train_lgb.model_trian_type:",cfgPara.task_train_lgb.model_trian_type)

        cfgPara.task_train_lgb.model_coef = self._cfgPara.get_para("lgb.model.saveFile", cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.model_coef:", cfgPara.task_train_lgb.model_coef)
        cfgPara.task_train_lgb.model_joblib_pkl = self._cfgPara.get_para("lgb.model.joblib_pkl",cfgPara.task_train_lgb.section)
        print("[config] ：cfgPara.task_train_lgb.model_joblib_pkl:", cfgPara.task_train_lgb.model_joblib_pkl)

        # *****************----task_train_catboost section----*****************#
        print("------task_train_catboost section------")
        cfgPara.task_train_catboost.reports_baseDir = self._cfgPara.get_para("cb.reports.baseDir", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_baseDir：", cfgPara.task_train_catboost.reports_baseDir)

        cfgPara.task_train_catboost.reports_missRate = self._cfgPara.get_para("cb.reports.missRate", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_missRate:", cfgPara.task_train_catboost.reports_missRate)
        cfgPara.task_train_catboost.reports_highMissRate = self._cfgPara.get_para("cb.reports.highMissRate", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_highMissRate:", cfgPara.task_train_catboost.reports_highMissRate)
        cfgPara.task_train_catboost.reports_missRate_genType = self._cfgPara.get_para("cb.reports.missRate.genType", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_missRate_genType:", cfgPara.task_train_catboost.reports_missRate_genType)

        cfgPara.task_train_catboost.reports_maxPercent = self._cfgPara.get_para("cb.reports.maxPercent", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_maxPercent:", cfgPara.task_train_catboost.reports_maxPercent)
        cfgPara.task_train_catboost.reports_maxPercent_genType = self._cfgPara.get_para("cb.reports.maxPercent.genType", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_maxPercent_genType:", cfgPara.task_train_catboost.reports_maxPercent_genType)

        cfgPara.task_train_catboost.reports_corr = self._cfgPara.get_para("cb.reports.corr", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_corr:", cfgPara.task_train_catboost.reports_corr)
        cfgPara.task_train_catboost.reports_highCorr = self._cfgPara.get_para("cb.reports.highCorr", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_highCorr:", cfgPara.task_train_catboost.reports_highCorr)
        cfgPara.task_train_catboost.reports_corr_genType = self._cfgPara.get_para("cb.reports.corr.genType", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_corr_genType:", cfgPara.task_train_catboost.reports_corr_genType)

        cfgPara.task_train_catboost.reports_ks = self._cfgPara.get_para("cb.reports.ks", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_ks:", cfgPara.task_train_catboost.reports_ks)
        cfgPara.task_train_catboost.reports_ks_png = self._cfgPara.get_para("cb.reports.ks.png", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_ks_png:", cfgPara.task_train_catboost.reports_ks_png)
        cfgPara.task_train_catboost.reports_ks_scores_bin = int(self._cfgPara.get_para("cb.reports.ks.scores.bin",cfgPara.task_train_catboost.section))
        print("[config] ：cfgPara.task_train_catboost.reports_ks_scores_bin:", cfgPara.task_train_catboost.reports_ks_scores_bin)
        cfgPara.task_train_catboost.reports_ks_genType = self._cfgPara.get_para("cb.reports.ks.genType", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_ks_genType:", cfgPara.task_train_catboost.reports_ks_genType)

        cfgPara.task_train_catboost.reports_psi = (self._cfgPara.get_para("cb.reports.psi", cfgPara.task_train_catboost.section))
        print("[config] ：cfgPara.task_train_catboost.reports_psi:",cfgPara.task_train_catboost.reports_psi)
        cfgPara.task_train_catboost.reports_psi_png = self._cfgPara.get_para("cb.reports.psi.png",cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_psi_png:",cfgPara.task_train_catboost.reports_psi_png)
        cfgPara.task_train_catboost.reports_psi_bin = int(self._cfgPara.get_para("cb.reports.psi.bin",cfgPara.task_train_catboost.section))
        print("[config] ：cfgPara.task_train_catboost.reports_psi_bin:", cfgPara.task_train_catboost.reports_psi_bin)


        cfgPara.task_train_catboost.reports_featureImportance = self._cfgPara.get_para("cb.reports.featureImportance", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_featureImportance:", cfgPara.task_train_lr.reports_featureImportance)
        cfgPara.task_train_catboost.reports_featureImportance_png = self._cfgPara.get_para("cb.reports.featureImportance.png",cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_featureImportance_png:",cfgPara.task_train_lr.reports_featureImportance_png)
        cfgPara.task_train_catboost.reports_featureImportance_genType = self._cfgPara.get_para("cb.reports.featureImportance.genType", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.reports_featureImportance_genType:", cfgPara.task_train_lr.reports_featureImportance_genType)

        cfgPara.task_train_catboost.para_highMissThreshold = float( self._cfgPara.get_para("cb.para.highMissThreshold", cfgPara.task_train_catboost.section))
        print("[config] ：cfgPara.task_train_catboost.para_highMissThreshold:", cfgPara.task_train_catboost.para_highMissThreshold)
        cfgPara.task_train_catboost.para_maxPercent = float(self._cfgPara.get_para("cb.para.maxPercent", cfgPara.task_train_catboost.section))
        print("[config] ：cfgPara.task_train_catboost.para_maxPercent:", cfgPara.task_train_catboost.para_maxPercent)
        cfgPara.task_train_catboost.para_min_div_max_badrate = float(self._cfgPara.get_para("cb.para.min_div_max_badrate", cfgPara.task_train_catboost.section))
        print("[config] ：cfgPara.task_train_catboost.para_min_div_max_badrate:", cfgPara.task_train_catboost.para_min_div_max_badrate)

        cfgPara.task_train_catboost.model_baseDir = self._cfgPara.get_para("cb.model.baseDir", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_lgb.model_baseDir:", cfgPara.task_train_catboost.model_baseDir)
        cfgPara.task_train_catboost.model_trian_type = ( self._cfgPara.get_para("cb.model.trian.type", cfgPara.task_train_catboost.section))
        print("[config] ：cfgPara.task_train_catboost.model_trian_type:", cfgPara.task_train_catboost.model_trian_type)

        cfgPara.task_train_catboost.model_coef = self._cfgPara.get_para("cb.model.saveFile", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.model_coef:", cfgPara.task_train_catboost.model_coef)
        cfgPara.task_train_catboost.model_joblib_pkl = self._cfgPara.get_para("cb.model.joblib_pkl", cfgPara.task_train_catboost.section)
        print("[config] ：cfgPara.task_train_catboost.model_joblib_pkl:", cfgPara.task_train_catboost.model_joblib_pkl)


        # *****************----task_train_mlp section----*****************#
        print("------task_train_mlp section------")
        cfgPara.task_train_mlp.reports_baseDir = self._cfgPara.get_para("mlp.reports.baseDir",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_baseDir：", cfgPara.task_train_mlp.reports_baseDir)

        cfgPara.task_train_mlp.reports_missRate = self._cfgPara.get_para("mlp.reports.missRate",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_missRate:", cfgPara.task_train_mlp.reports_missRate)
        cfgPara.task_train_mlp.reports_highMissRate = self._cfgPara.get_para("mlp.reports.highMissRate",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_highMissRate:", cfgPara.task_train_mlp.reports_highMissRate)
        cfgPara.task_train_mlp.reports_missRate_genType = self._cfgPara.get_para("mlp.reports.missRate.genType",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_missRate_genType:",cfgPara.task_train_mlp.reports_missRate_genType)

        cfgPara.task_train_mlp.reports_maxPercent = self._cfgPara.get_para("mlp.reports.maxPercent",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_maxPercent:", cfgPara.task_train_mlp.reports_maxPercent)
        cfgPara.task_train_mlp.reports_maxPercent_genType = self._cfgPara.get_para("mlp.reports.maxPercent.genType",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_maxPercent_genType:",cfgPara.task_train_mlp.reports_maxPercent_genType)

        cfgPara.task_train_mlp.reports_corr = self._cfgPara.get_para("mlp.reports.corr", cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_corr:", cfgPara.task_train_mlp.reports_corr)
        cfgPara.task_train_mlp.reports_highCorr = self._cfgPara.get_para("mlp.reports.highCorr",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_highCorr:", cfgPara.task_train_mlp.reports_highCorr)
        cfgPara.task_train_mlp.reports_corr_genType = self._cfgPara.get_para("mlp.reports.corr.genType",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_corr_genType:", cfgPara.task_train_mlp.reports_corr_genType)

        cfgPara.task_train_mlp.reports_ks = self._cfgPara.get_para("mlp.reports.ks", cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_ks:", cfgPara.task_train_mlp.reports_ks)
        cfgPara.task_train_mlp.reports_ks_png = self._cfgPara.get_para("mlp.reports.ks.png",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_ks_png:", cfgPara.task_train_mlp.reports_ks_png)
        cfgPara.task_train_mlp.reports_ks_genType = self._cfgPara.get_para("mlp.reports.ks.genType",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_ks_genType:", cfgPara.task_train_mlp.reports_ks_genType)

        cfgPara.task_train_mlp.reports_featureImportance = self._cfgPara.get_para("mlp.reports.featureImportance",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_featureImportance:",cfgPara.task_train_mlp.reports_featureImportance)
        cfgPara.task_train_mlp.reports_featureImportance_png = self._cfgPara.get_para("mlp.reports.featureImportance.png",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_featureImportance_png:",cfgPara.task_train_mlp.reports_featureImportance_png)
        cfgPara.task_train_mlp.reports_featureImportance_genType = self._cfgPara.get_para("mlp.reports.featureImportance.genType", cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.reports_featureImportance_genType:",cfgPara.task_train_mlp.reports_featureImportance_genType)

        cfgPara.task_train_mlp.para_highMissThreshold = float(self._cfgPara.get_para("mlp.para.highMissThreshold", cfgPara.task_train_mlp.section))
        print("[config] ：cfgPara.task_train_mlp.para_highMissThreshold:", cfgPara.task_train_mlp.para_highMissThreshold)
        cfgPara.task_train_mlp.para_maxPercent = float(self._cfgPara.get_para("mlp.para.maxPercent", cfgPara.task_train_mlp.section))
        print("[config] ：cfgPara.task_train_mlp.para_maxPercent:", cfgPara.task_train_mlp.para_maxPercent)
        cfgPara.task_train_mlp.para_min_div_max_badrate = float(self._cfgPara.get_para("mlp.para.min_div_max_badrate", cfgPara.task_train_mlp.section))
        print("[config] ：cfgPara.task_train_mlp.para_min_div_max_badrate:",cfgPara.task_train_mlp.para_min_div_max_badrate)

        cfgPara.task_train_mlp.model_baseDir = self._cfgPara.get_para("mlp.model.baseDir",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.model_baseDir:", cfgPara.task_train_mlp.model_baseDir)
        cfgPara.task_train_mlp.model_trian_type = (self._cfgPara.get_para("mlp.model.trian.type", cfgPara.task_train_mlp.section))
        print("[config] ：cfgPara.task_train_mlp.model_trian_type:", cfgPara.task_train_mlp.model_trian_type)

        cfgPara.task_train_mlp.model_coef = self._cfgPara.get_para("mlp.model.saveFile", cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.model_coef:", cfgPara.task_train_mlp.model_coef)
        cfgPara.task_train_mlp.model_joblib_pkl = self._cfgPara.get_para("mlp.model.joblib_pkl",cfgPara.task_train_mlp.section)
        print("[config] ：cfgPara.task_train_mlp.model_joblib_pkl:", cfgPara.task_train_mlp.model_joblib_pkl)

        # *****************----task_psi section----*****************#
        print("------task_psi section------")
        cfgPara.task_psi.reports_baseDir = self._cfgPara.get_para("psi.reports.baseDir",cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.reports_baseDir：", cfgPara.task_psi.reports_baseDir)
        cfgPara.task_psi.reports_psi = self._cfgPara.get_para("psi.reports",cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.reports_psi：", cfgPara.task_psi.reports_psi)
        cfgPara.task_psi.reports_psi_png = self._cfgPara.get_para("psi.reports.png", cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.reports_psi_png：", cfgPara.task_psi.reports_psi_png)

        cfgPara.task_psi.psi_data1 = self._cfgPara.get_para("psi.data1", cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.psi_data1：", cfgPara.task_psi.psi_data1)
        cfgPara.task_psi.psi_data2 = self._cfgPara.get_para("psi.data2", cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.psi_data2：", cfgPara.task_psi.psi_data2)
        cfgPara.task_psi.psi_data1_name = self._cfgPara.get_para("psi.data1.name", cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.psi_data1_name：", cfgPara.task_psi.psi_data1_name)
        cfgPara.task_psi.psi_data2_name = self._cfgPara.get_para("psi.data2.name", cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.psi_data2_name：", cfgPara.task_psi.psi_data2_name)

        cfgPara.task_psi.psi_bins = int(self._cfgPara.get_para("psi.bins", cfgPara.task_psi.section))
        print("[config] ：cfgPara.task_psi.psi_bins：", cfgPara.task_psi.psi_bins)
        cfgPara.task_psi.psi_model_pkl = self._cfgPara.get_para("psi.mode.pkl", cfgPara.task_psi.section)
        print("[config] ：cfgPara.task_psi.psi_model_pkl：", cfgPara.task_psi.psi_model_pkl)

        print("*****************----[end get all config parameters]-----*****************")
