# coding=utf-8

#参数枚举
class cfgConst:
    ##  [task]
    taskSection_name = "task"
    taskSection_task_train = "train"
    taskSection_task_predict = "predict"
    taskSection_task_psi = "psi"

    ##  [task_train]
    trainSection_name = "task_train"
    trainSection_method_lr = "lr"
    trainSection_method_lgb = "lgb"
    trainSection_method_catboost = "catboost"
    trainSection_method_mlp = "mlp"

    ##  [task_train_lr]
    trainLrSection_name = "task_train_lr"
    ##  [task_train_lgb]
    trainLgbSection_name = "task_train_lgb"
    task_train_lgbSection_train_default="default"
    task_train_lgbSection_train_gridSearch = "gridSearch"

    ##  [task_train_catboost]
    trainCatboostSection_name = "task_train_catboost"
    ##  [task_train_mlp]
    trainMlpSection_name = "task_train_mlp"

    ##  [task_psi]
    taskPsiSection_name = "task_psi"

    ## [task_predict]
    taskPredictSection_name = "task_predict"
    ## trian mode
    trainMode_gridSearch = "gridSearch"
    trainMode_default = "default"

    ## report save type
    reportSaveModel_ifNotPresent="ifNotPresent"
    reportSaveModel_always = "always"
    reportSaveModel_never = "never"

#定义配置参数
class cfgPara(cfgConst):

    class task:
        section=cfgConst.taskSection_name
        task = None
        cpu_core = None
        basePoint = None
        odds = None

    class train:
        section = cfgConst.trainSection_name
        method = None
        data_path = None
        data_label = None
        data_label_good = None
        data_label_bad = None

    class task_train_lr:
        section = cfgConst.trainLrSection_name
        reports_baseDir = None
        reports_missRate = None
        reports_highMissRate = None
        reports_missRate_genType = None

        reports_maxPercent = None
        reports_maxPercent_genType = None

        reports_corr = None
        reports_highCorr = None
        reports_corr_genType = None

        reports_vif = None
        reports_vif_genType = None

        reports_featureImportance = None
        reports_featureImportance_png = None
        reports_featureImportance_genType = None

        reports_ks = None
        reports_ks_png = None
        reports_ks_scores_bin = None
        reports_ks_genType = None

        reports_confusionMatrix_Png = None
        reports_confusionMatrix_genType = None

        model_baseDir = None
        model_ivParaPickle = None
        model_woeParaPickle = None
        model_cutoffParaPickle = None

        model_ivWoeCutoff = None
        model_singBinPcn = None
        model_singBinPcnOverThreshold = None
        model_ivWoeCutoff_genType = None


        model_pValuePara = None
        model_pValuePara_genType = None
        model_lrSummary_png = None
        model_lrSummary_png_genType = None
        model_coef = None
        model_joblib_pkl = None

        para_highMissThreshold = None
        para_maxPercent = None
        para_min_div_max_badrate = None
        para_ivThreshold_low = None  # 小于minIV_del将被剔除
        para_ivThreshold_high = None  # 大于maxIV_del将被剔除
        para_singBin_maxPercentThreshHold = None  # 单一分箱最大占比超过90%将被删除
        para_highCorrThreshhold_max = None
        para_highCorrThreshhold_min = None
        para_vif_threshold = None
        para_pValuer_threshold = None

    class task_train_lgb:
        section = cfgConst.trainLgbSection_name
        reports_baseDir =  None

        reports_missRate = None
        reports_highMissRate = None
        reports_missRate_genType = None

        # 数据集中度报告
        reports_maxPercent = None
        reports_maxPercent_genType = None

        # 相关性报告
        reports_corr = None
        reports_highCorr = None
        reports_corr_genType = None

        # vif
        reports_vif = None
        reports_vif_genType = None

        # featureImportance
        reports_featureImportance = None
        reports_featureImportance_png = None
        reports_featureImportance_genType = None

        # ks
        reports_ks = None
        reports_ks_png = None
        reports_ks_scores_bin = None
        reports_ks_genType = None

        model_baseDir = None
        model_trian_type = None
        model_coef = None
        model_joblib_pkl = None

        para_highMissThreshold = None
        para_maxPercent = None
        para_min_div_max_badrate = None

    class task_train_catboost:
        section = cfgConst.trainCatboostSection_name
        reports_baseDir =  None

        reports_missRate = None
        reports_highMissRate = None
        reports_missRate_genType = None

        # 数据集中度报告
        reports_maxPercent = None
        reports_maxPercent_genType = None

        # 相关性报告
        reports_corr = None
        reports_highCorr = None
        reports_corr_genType = None

        # vif
        reports_vif = None
        reports_vif_genType = None

        # featureImportance
        reports_featureImportance = None
        reports_featureImportance_png = None
        reports_featureImportance_genType = None

        # ks
        reports_ks = None
        reports_ks_png = None
        reports_ks_scores_bin = None
        reports_ks_genType = None
        #psi
        reports_psi = None
        reports_psi_png = None
        reports_psi_bin = None

        model_baseDir = None
        model_trian_type = None
        model_coef = None
        model_joblib_pkl = None

        para_highMissThreshold = None
        para_maxPercent = None
        para_min_div_max_badrate = None

    class task_train_mlp:
        section = cfgConst.trainMlpSection_name
        reports_baseDir = None

        reports_missRate = None
        reports_highMissRate = None
        reports_missRate_genType = None

        # 数据集中度报告
        reports_maxPercent = None
        reports_maxPercent_genType = None

        # 相关性报告
        reports_corr = None
        reports_highCorr = None
        reports_corr_genType = None

        # vif
        reports_vif = None
        reports_vif_genType = None

        # featureImportance
        reports_featureImportance = None
        reports_featureImportance_png = None
        reports_featureImportance_genType = None

        # ks
        reports_ks = None
        reports_ks_png = None
        reports_ks_genType = None

        model_baseDir = None
        model_trian_type = None
        model_coef = None
        model_joblib_pkl = None

        para_highMissThreshold = None
        para_maxPercent = None
        para_min_div_max_badrate = None

    class task_psi:
        section = cfgConst.taskPsiSection_name
        reports_baseDir = None
        reports_psi = None
        reports_psi_png = None
        psi_data1 = None
        psi_data1_name =None
        psi_data2 = None
        psi_data2_name = None
        psi_model_pkl = None
        psi_bins = None

    class task_predict:
        section = cfgConst.taskPredictSection_name
        reports_baseDir = None
        # ks
        reports_ks = None
        reports_ks_png = None
        reports_ks_scores_bin = None
        model_joblib_pkl = None
        
        

