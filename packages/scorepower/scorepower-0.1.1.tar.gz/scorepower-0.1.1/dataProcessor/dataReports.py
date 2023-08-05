# coding=utf-8
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import itertools
from collections import defaultdict
class statistics():
    @staticmethod
    def gen_missingReprot_feature(df,miss_report_name,high_miss_report_name,high_miss_threshhold=0.5):

        # 字段行总数`
        total = df.shape[0]
        col_names=df.columns.tolist()
        df["total"] = total
        # 各个字段计数
        count = df.count()
        # 空缺率
        miss_percentage = 1 - count / total * 1.0
        miss_total = total - count
        ###########生成缺失报告###########
        df_missing=pd.DataFrame(list(zip(col_names,df["total"], miss_total, miss_percentage)),
                                         columns=["col_names","total", "missing_total", "missing_rate"])

        df_missing.set_index("col_names").sort_values("missing_rate").to_csv(miss_report_name)
        # self.gen_missingReprot_testData(df)
        ###########生成高缺失率报告###########

        df_missing_filter = df_missing[df_missing['missing_rate'] > high_miss_threshhold]
        df_missing_filter.set_index("col_names").sort_values("missing_rate").to_csv(high_miss_report_name)

        print("     [generated missRate report]: {}...".format(miss_report_name))
        print("     [generated missRate>{} missing rate report]: {}...".format(high_miss_threshhold,
                                                                                        high_miss_report_name))
        del df_missing
        del df_missing_filter
        del df["total"]

    @staticmethod
    def gen_missingReprot_itemData(df,miss_report_name,high_miss_report_name,high_miss_threshhold=0.5):
        pass

    @staticmethod
    def gen_corrReport(df,corrSaveFile,high_corrSaveFile,max_threshHold=0.7,min_threshHold=-0.7):
        # 变量相关性分析 pearson spearman kendall
        cor = df.corr('pearson')

        cor.loc[:, :] = np.tril(cor, k=-1)
        cor = cor.stack()
        # 仅仅列出高相关系数，数据呈现结构化
        high_corr_thresHold = cor[(cor > max_threshHold) | (cor < min_threshHold)]
        # 转换为dataframe结构
        df_cor = pd.DataFrame(cor)

        df_high_cor1 = pd.DataFrame(high_corr_thresHold)
        # df_high_cor1.columns=["col_1","col_N","corr"]
        # 保存到Excel
        df_high_cor1.to_csv(high_corrSaveFile)
        print("     [生成变量高相关性报告(corr>{}且corr<{})]:{}".format(max_threshHold,min_threshHold,high_corrSaveFile))
        df_cor.to_csv(corrSaveFile)
        print("     [生成变量相关报告]:",corrSaveFile)
        del df_cor
        del df_high_cor1

    @staticmethod
    def gen_outlierReport_quantile(df,threshHold,outliersSaveFile):
        # x>Q3+3(Q3-Q1) or x<Q1-3(Q3-Q1) Q3:75%, Q1:25%

        quantile_25 = df.quantile(q=0.25)
        quantile_75 = df.quantile(q=0.75)
        quantile_upper = pd.DataFrame(quantile_75 + (quantile_75 - quantile_25) * threshHold, columns=["quantile_upper"])
        quantile_lower = pd.DataFrame(quantile_25 - (quantile_75 - quantile_25) * threshHold, columns=["quantile_lower"])

        report = pd.merge(quantile_25, quantile_75, left_index=True, right_index=True, how="left")
        report = pd.merge(report, quantile_upper, left_index=True, right_index=True, how="left")
        report = pd.merge(report, quantile_lower, left_index=True, right_index=True, how="left")
        report.columns = ["quantile_25%", "quantile_75%", "quantile_upper", "quantile_lower"]

        report["outlier1_cnt"] = df[
            df > (df.quantile(q=0.75) + (df.quantile(q=0.75) - df.quantile(q=0.25)) * threshHold)].count()
        report["outlier2_cnt"] = df[
            df < (df.quantile(q=0.25) - (df.quantile(q=0.75) - df.quantile(q=0.25)) * threshHold)].count()
        report["outlier_cnt"] = report["outlier1_cnt"] + report["outlier2_cnt"]

        report.to_csv(outliersSaveFile)
        print("     [comepeted generate outlierQuantileReport]:", outliersSaveFile)

    @staticmethod
    def gen_outlierReport_std(df, outliersSaveFile):
        std_info = df.describe()
        report = pd.DataFrame(std_info.values.T, index=std_info.columns, columns=std_info.index)
        report["mean+3std"] = df.mean() + 3 * df.std()
        report["mean-3std"] = df.mean() - 3 * df.std()
        report["over_mean+3std_cnt"] = df[df > (df.mean() + 3 * df.std())].count()
        report["lowe_mean-3std_cnt"] = df[df < (df.mean() - 3 * df.std())].count()
        report.to_csv(outliersSaveFile)
        print("     [comepeted generate outlierStdReport]:", outliersSaveFile)


    #数据单一性或常数
    @staticmethod
    def gen_monotonyReports(df,categoryCols,threshHold):
        pass

    #数据集中度报告
    @staticmethod
    def gen_maxPercentageVariableReports(df,reportFile,target):
        # 计算多数值占比超过90%的字段中，少数值的坏样本率是否会显著高于多数值
        records_count = df.shape[0]
        col_most_values, col_large_value,bad_rate_diff = {}, {},{}
        for i,col in enumerate(df.columns.drop(target)):

            value_count = df[col].groupby(df[col]).count()
            col_most_values[col] = max(value_count) / records_count
            large_value = value_count[value_count == max(value_count)].index[0]
            col_large_value[col] = large_value

            #计算少数值坏样本率/多数值坏样本率
            temp = df[[col, target]]
            temp[col] = temp.apply(lambda x: int(x[col] == col_large_value[col]), axis=1)
            bad_rate = temp.groupby(col).mean()
            if bad_rate.iloc[0][target] == 0:
                bad_rate_diff[col] = 0
                continue
            print("     [特征{}/{}]:{}  [0]:{} [1]:{}".format(i, len(df.columns.drop(target).tolist()), col,
                                                                     bad_rate.iloc[0][target],bad_rate.iloc[1][target]))
            # print("bad_rate.iloc[0][target] : ", )
            # print("bad_rate.iloc[1][target] : ", bad_rate.iloc[1][target])
            bad_rate_diff[col] = (bad_rate.iloc[0][target] / bad_rate.iloc[1][target])

        col_most_values_df = pd.DataFrame.from_dict(col_most_values, orient='index')
        col_most_values_df.columns = ['max_percent']
        col_large_value_df = pd.DataFrame.from_dict(col_large_value, orient='index')
        col_large_value_df.columns = ['max_percent_value']
        min_max_badrate = pd.DataFrame.from_dict(bad_rate_diff, orient='index')
        min_max_badrate.columns = ['min_div_max_badrate']


        report =pd.merge(col_most_values_df,col_large_value_df,left_index=True, right_index=True,how="left")
        report = pd.merge(report, min_max_badrate, left_index=True, right_index=True, how="left")

        report.sort_values(by='max_percent', ascending=False,inplace=True)
        report.to_csv(reportFile,index_label="cols")
        print("     [完成报告]:",reportFile)


    @staticmethod
    def gen_featureImportanceReport(colms,cls_model,saveFile,savePng):
        df=pd.DataFrame({
            'column': colms,
            'importance': cls_model.feature_importances_,
        })
        df.sort_values(by='importance',inplace=True)
        df.to_csv(saveFile)
        ax=df.plot.barh(x='column', y="importance",title="feature importance")
        plt.tight_layout()
        ax.get_figure().savefig(savePng)
        print("     [生成特种重要性报告]: ", saveFile)
        print("     [生成特种重要性报告]: ", savePng)

    @staticmethod
    def gen_IV_WOE_CutOff_Report(iv_dic,woe_dic,cutoff_dic,saveFile):
        iv_df = pd.DataFrame.from_dict(iv_dic, orient='index')
        iv_df.columns = ["iv"]
        woe_df = pd.DataFrame.from_dict(woe_dic, orient='index')
        cols=[]
        for i in range(len(woe_df.columns)):
            cols.append("woe_bin"+str(i))
        # woe_df.columns = ["woe_bin0", "woe_bin1", "woe_bin2", "woe_bin3", "woe_bin4"]
        woe_df.columns=cols
        cols = []
        cutoff_df = pd.DataFrame.from_dict(cutoff_dic, orient='index')
        for i in range(len(cutoff_df.columns)):
            cols.append("cutoff_" + str(i))
        cutoff_df.columns = cols
        #
        report = pd.merge(iv_df, woe_df, left_index=True, right_index=True, how="left")
        report = pd.merge(report, cutoff_df, left_index=True, right_index=True, how="left")
        report.sort_values(by="iv", inplace=True)
        report.to_csv(saveFile)
        print("     [生成IV报告]: ", saveFile)

    @staticmethod
    def gen_singleBin_OverThreshold_Report(percent_dict,cutoff_dict , saveFile):

        pcnt_df = pd.DataFrame.from_dict(percent_dict, orient='index')

        cols=[]
        for i in range(len(pcnt_df.columns)):
            cols.append("bin"+str(i))
            # pcnt_df.columns = ["bin0", "bin1", "bin2", "bin3", "bin4"]
        pcnt_df.columns=cols
        cutoff_df = pd.DataFrame.from_dict(cutoff_dict, orient='index')
        cols = []


        for i in range(len(cutoff_df.columns)):
            cols.append("cutoff_" + str(i))
        cutoff_df.columns=cols
        # cutoff_df.columns = ["cutoff_0", "cutoff_1", "cutoff_2", "cutoff_3"]
        report = pd.merge(pcnt_df, cutoff_df, left_index=True, right_index=True, how="left")
        report.to_csv(saveFile)
        print("     [生成单一分箱超过最大阈值报告]: ", saveFile)

    @staticmethod
    def gen_vifRreport(df,iv_report,saveFile):

        ### (iii）检查是否有变量与其他所有变量的VIF > 10
        col_vif_dict = {}
        print("     [开始生成vif报告]...")
        df_iv=pd.read_csv(iv_report)#主要用来参考iv从低到高排序vif变量，用以后面处理多vif时候 将低iv值优先剔除
        vi_low2high=df_iv["Unnamed: 0"].values #iv从低到高排序
        sort_iv_columns=[i for i in vi_low2high if i in df.columns]#iv从低到高排序
        for i,col in enumerate(sort_iv_columns):

            x0 = df[col]
            X = df.drop(col,axis=1)
            regr = LinearRegression()
            clr = regr.fit(X, x0)
            x_pred = clr.predict(X)
            R2 = 1 - ((x_pred - x0) ** 2).sum() / ((x0 - x0.mean()) ** 2).sum()
            vif = 1 / (1 - R2)
            col_vif_dict[col] = vif
            print("     变量{}/{},vif:{},{}".format(i+1,(df.shape[1]),vif,col))

        vif_df = pd.DataFrame.from_dict(col_vif_dict, orient='index')
        vif_df.columns = ['vif']
        vif_df.sort_values(by="vif", inplace=True)
        vif_df.to_csv(saveFile,index_label="col")
    @staticmethod
    def gen_pValueParafRreport(pValue_dict,para_dict,largeP_dict,ceof_univariate, saveFile):
        pValue_df = pd.DataFrame.from_dict(pValue_dict, orient='index')
        ceof_df = pd.DataFrame.from_dict(para_dict, orient='index')
        ceof_univariate_df = pd.DataFrame.from_dict(ceof_univariate, orient='index')
        largeP_df = pd.DataFrame.from_dict(largeP_dict, orient='index')

        report=pd.merge(ceof_df, ceof_univariate_df, left_index=True, right_index=True, how="left")
        report = pd.merge(report, pValue_df, left_index=True, right_index=True, how="left")
        report = pd.merge(report, largeP_df, left_index=True, right_index=True, how="left")
        report.columns = ['Coef',"Coef_univariate",'pValuer',"pValuer_univariate"]
        report["col"]=report.index
        report.set_index("col",inplace=True)
        report.reset_index(inplace=True)
        report.sort_values(by="pValuer",inplace=True)
        report.to_csv(saveFile)
        print("     [生成pValuer和权重参数报告]: ", saveFile)

    @staticmethod
    def gen_summaryPng(summary,saveFile):

        # plt.rc('figure', figsize=(15, 5))
        plt.text(0.01, 0.05, str(summary), {'fontsize': 10},
                 fontproperties='monospace')  # approach improved by OP -> monospace!
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(saveFile,bbox_inches='tight',dpi=100)
        print("     [生成逻辑回归summary报告]: ", saveFile)

    @staticmethod
    def gen_confusionMatrixPng(confusionMatrix,threshold,saveFile, classes=[0,1],title='Confusion matrix',cmap=plt.cm.Blues,):

        plt.figure()
        plt.imshow(confusionMatrix, interpolation='nearest', cmap=cmap)
        title=title+"_threshold_{}".format(threshold)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=0)
        plt.yticks(tick_marks, classes)

        thresh = confusionMatrix.max() / 2.
        for i, j in itertools.product(range(confusionMatrix.shape[0]), range(confusionMatrix.shape[1])):
            plt.text(j, i, confusionMatrix[i, j],
                     horizontalalignment="center",
                     color="white" if confusionMatrix[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        saveFile=saveFile[:-4]+"_"+str(threshold)+".png"
        plt.savefig(saveFile)
        print("     [生成混淆矩阵]: ", saveFile)
    @staticmethod
    def gen_string2TXT(ss,saveFile):
        file = open(saveFile, 'w');
        file.write(ss);
        file.close();
        print("     [写入文件]:",saveFile)

    @staticmethod
    def gen_psiTrianTestReport(trainScore,testScore,saveFile):
        min=trainScore

    @staticmethod
    def gen_scoreCardReport(df, woe_vi_cutoffReport, coefReport, odds, saveFile):
        """
        dict={col1:{
                    cutoff:[]
                    bin:{bin0:[],bin1:[],bin2:[],bin3[]},
                    bad:{bin0:[],bin1:[],bin2:[],bin3[]},
                    pcnt:{bin0:[],bin1:[],bin2:[],bin3[]},
                    woe:{bin0:[],bin1:[],bin2:[],bin3[]},
                    iv:[],

                    score:{bin0:[],bin1:[],bin2[],bin3[]},
                    },
            col2:{  cutoff:[]
                    bin:{bin0:[],bin1:[],bin2:[],bin3[]},
                    bad:{bin0:[],bin1:[],bin2:[],bin3[]},
                    pcnt:{bin0:[],bin1:[],bin2:[],bin3[]},
                    woe:{bin0:[],bin1:[],bin2:[],bin3[]},
                    iv:[],
                    score:{bin0:[],bin1:[],bin2[],bin3[]},
                    },
                }
        """

        dict_list = defaultdict(dict)
        df_woe_iv_cutoff = pd.read_csv(woe_vi_cutoffReport, index_col=0);

        # print((df_woe_iv_cutoff[df_woe_iv_cutoff.index == "sum_last_order_settle_amount_repay_time_before_rate_last_1m_all"]["cutoff_1"].isnull()))

        # print(df_woe_iv_cutoff[df_woe_iv_cutoff.index=="sum_last_order_settle_amount_repay_time_before_rate_last_1m_all"]["iv"][0])
        print("计算iv相关...")
        for col in df.columns.drop("label"):
            tmp_df = df_woe_iv_cutoff[df_woe_iv_cutoff.index == col]
            # print(df_woe_iv_cutoff[df_woe_iv_cutoff.index==col]["cutoff_1"].isnull()[0])

            ## 1.填充IV
            dict_list[col]["iv"] = tmp_df["iv"][0]

            ##填充bin woe cutoff
            dict_list[col]["bin"] = {}
            dict_list[col]["woe"] = {}
            dict_list[col]["cutoff"] = []
            dict_list[col]["bin"]["bin0"] = "[min,{}]".format(tmp_df["cutoff_0"][0])
            dict_list[col]["woe"]["bin0"] = tmp_df["woe_bin0"][0]

            dict_list[col]["cutoff"].append(tmp_df["cutoff_0"][0])

            if (tmp_df["cutoff_1"].isnull()[0]):
                dict_list[col]["bin"]["bin1"] = "({},{}]".format(tmp_df["cutoff_0"][0], "max")
                dict_list[col]["woe"]["bin1"] = tmp_df["woe_bin1"][0]
            else:
                dict_list[col]["bin"]["bin1"] = "({},{}]".format(tmp_df["cutoff_0"][0], tmp_df["cutoff_1"][0])
                dict_list[col]["woe"]["bin1"] = tmp_df["woe_bin1"][0]
                dict_list[col]["cutoff"].append(tmp_df["cutoff_1"][0])

                if (tmp_df["cutoff_2"].isnull()[0]):  ##只有一个切分点
                    dict_list[col]["bin"]["bin2"] = "({},{}]".format(tmp_df["cutoff_1"][0], "max")
                    dict_list[col]["woe"]["bin2"] = tmp_df["woe_bin2"][0]
                else:
                    dict_list[col]["bin"]["bin2"] = "({},{}]".format(tmp_df["cutoff_1"][0], tmp_df["cutoff_2"][0])
                    dict_list[col]["woe"]["bin2"] = tmp_df["woe_bin2"][0]
                    dict_list[col]["cutoff"].append(tmp_df["cutoff_2"][0])
                    if (tmp_df["cutoff_3"].isnull()[0]):  ##只有两个切分点
                        dict_list[col]["bin"]["bin3"] = "({},{}]".format(tmp_df["cutoff_2"][0], "max")
                        dict_list[col]["woe"]["bin3"] = tmp_df["woe_bin3"][0]
                    else:
                        dict_list[col]["bin"]["bin3"] = "({},{}]".format(tmp_df["cutoff_2"][0], tmp_df["cutoff_3"][0])
                        dict_list[col]["bin"]["bin4"] = "({},{}]".format(tmp_df["cutoff_3"][0], "max")  ##有三个切分点
                        dict_list[col]["woe"]["bin3"] = tmp_df["woe_bin3"][0]
                        dict_list[col]["woe"]["bin4"] = tmp_df["woe_bin4"][0]
                        dict_list[col]["cutoff"].append(tmp_df["cutoff_3"][0])

        ## 2.填充bad  pcnt
        print("计算badrate和percent...")
        for col in df.columns.drop("label"):
            dict_list[col]["pcnt"] = {}
            dict_list[col]["bad"] = {}
            dict_list[col]["score"] = {}
            dict_list[col]["Coef_WOE"] = {}

        for i, row in enumerate(df.itertuples()):  # 按行遍历
            for col in df.columns.drop("label"):
                ## 判断属于哪一箱
                value = getattr(row, col)
                # 更新bin0 pcnt和bad
                # print("col:{},len:{} value：{} cutoff[0]:{} cutoff[1]:{}".format(col,len(dict_list[col]["cutoff"]),value,dict_list[col]["cutoff"][0],dict_list[col]["cutoff"][1]))
                if (value <= dict_list[col]["cutoff"][0]):  # bin0
                    if ("bin0" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin0"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin0"] = 1
                        ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin0" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin0"] = ll
                    else:
                        dict_list[col]["bad"]["bin0"] += ll
                elif (value > dict_list[col]["cutoff"][0] and len(dict_list[col]["cutoff"]) == 1):  # bin1
                    if ("bin1" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin1"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin1"] = 1
                    ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin1" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin1"] = ll
                    else:
                        dict_list[col]["bad"]["bin1"] += ll
                elif (dict_list[col]["cutoff"][0] < value <= dict_list[col]["cutoff"][1]):  # bin1
                    if ("bin1" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin1"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin1"] = 1
                    ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin1" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin1"] = ll
                    else:
                        dict_list[col]["bad"]["bin1"] += ll
                elif (dict_list[col]["cutoff"][1] < value and len(dict_list[col]["cutoff"]) == 2):  # bin2
                    if ("bin2" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin2"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin2"] = 1
                    ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin2" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin2"] = ll
                    else:
                        dict_list[col]["bad"]["bin2"] += ll
                elif (dict_list[col]["cutoff"][1] < value <= dict_list[col]["cutoff"][2]):  # bin2
                    if ("bin2" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin2"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin2"] = 1
                    ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin2" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin2"] = ll
                    else:
                        dict_list[col]["bad"]["bin2"] += ll
                elif (dict_list[col]["cutoff"][2] < value and len(dict_list[col]["cutoff"]) == 3):  # bin3
                    if ("bin3" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin3"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin3"] = 1
                    ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin3" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin3"] = ll
                    else:
                        dict_list[col]["bad"]["bin3"] += ll
                elif (dict_list[col]["cutoff"][2] < value <= dict_list[col]["cutoff"][3]):  # bin3
                    if ("bin3" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin3"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin3"] = 1
                    ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin3" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin3"] = ll
                    else:
                        dict_list[col]["bad"]["bin3"] += ll
                elif (dict_list[col]["cutoff"][3] < value):  # bin4
                    if ("bin4" in dict_list[col]["pcnt"].keys()):
                        dict_list[col]["pcnt"]["bin4"] += 1
                    else:
                        dict_list[col]["pcnt"]["bin4"] = 1
                        ##更新bad和 pcnt
                    ll = getattr(row, "label")
                    if ("bin4" not in dict_list[col]["bad"].keys()):
                        dict_list[col]["bad"]["bin4"] = ll
                    else:
                        dict_list[col]["bad"]["bin4"] += ll

        ## 3.计算badRation 和 pcntRation 以及score  score=base*log(2)*woe*0.01  和woe*ceof
        print("计算badRation, pcntRation, score和 woe*ceof...")
        for (col, v) in dict_list.items():

            bin_num = len(dict_list[col]["cutoff"])
            print("dict_list[col][cutoff]: ",dict_list[col]["cutoff"])
            print("col:{} bin_num:{}.dict_list[col][pcnt]:{}".format(col,bin_num,dict_list[col]["pcnt"]))
            pcnt = 0
            for i in range(bin_num+1):
                pcnt += dict_list[col]["pcnt"]["bin" + str(i)]

            dict_list[col]["bad"]["bin0"] = dict_list[col]["bad"]["bin0"] / dict_list[col]["pcnt"]["bin0"] * 100
            dict_list[col]["bad"]["bin1"] = dict_list[col]["bad"]["bin1"] / dict_list[col]["pcnt"]["bin1"] * 100

            dict_list[col]["pcnt"]["bin0"] = dict_list[col]["pcnt"]["bin0"] / pcnt * 100
            dict_list[col]["pcnt"]["bin1"] = dict_list[col]["pcnt"]["bin1"] / pcnt * 100
            dict_list[col]["score"]["bin0"] = odds * np.log(2) * dict_list[col]["woe"]["bin0"]


            dict_list[col]["score"]["bin1"] = odds * np.log(2) * dict_list[col]["woe"]["bin1"]

            if bin_num >= 2:
                dict_list[col]["bad"]["bin2"] = dict_list[col]["bad"]["bin2"] / dict_list[col]["pcnt"]["bin2"] * 100
                dict_list[col]["pcnt"]["bin2"] = dict_list[col]["pcnt"]["bin2"] / pcnt * 100

                dict_list[col]["score"]["bin2"] = odds * np.log(2) * dict_list[col]["woe"]["bin2"]
            if bin_num >= 3:
                dict_list[col]["bad"]["bin3"] = dict_list[col]["bad"]["bin3"] / dict_list[col]["pcnt"]["bin3"] * 100
                dict_list[col]["pcnt"]["bin3"] = dict_list[col]["pcnt"]["bin3"] / pcnt * 100
                dict_list[col]["score"]["bin3"] = odds * np.log(2) * dict_list[col]["woe"]["bin3"]
            if bin_num == 4:
                dict_list[col]["bad"]["bin4"] = dict_list[col]["bad"]["bin4"] /dict_list[col]["pcnt"]["bin4"]   * 100
                dict_list[col]["pcnt"]["bin4"] = dict_list[col]["pcnt"]["bin4"] / pcnt * 100

                dict_list[col]["score"]["bin4"] = odds * np.log(2) * dict_list[col]["woe"]["bin4"]

        # pValue_df = pd.DataFrame.from_dict(pValue_dict, orient='index')
        # report = pd.merge(ceof_df, ceof_univariate_df, left_index=True, right_index=True, how="left")
        # report = pd.merge(report, pValue_df, left_index=True, right_index=True, how="left")

        ##更新coef系数 coef*woe
        df_coef = pd.read_csv(coefReport, index_col=0)
        for col in df.columns.drop("label"):
            bin_num = len(dict_list[col]["cutoff"])
            dict_list[col]["Coef"] = df_coef[df_coef.index == col]["Coef"][0]
            # print(type(dict_list[col]["Coef"]),type(dict_list[col]["woe"]["bin0"]))
            dict_list[col]["Coef_WOE"]["bin0"] = float(dict_list[col]["Coef"]) * dict_list[col]["woe"]["bin0"]
            dict_list[col]["Coef_WOE"]["bin1"] = float(dict_list[col]["Coef"]) * dict_list[col]["woe"]["bin1"]
            if bin_num >= 2:
                dict_list[col]["Coef_WOE"]["bin2"] = float(dict_list[col]["Coef"]) * dict_list[col]["woe"]["bin2"]
            if bin_num >= 3:
                dict_list[col]["Coef_WOE"]["bin3"] = float(dict_list[col]["Coef"]) * dict_list[col]["woe"]["bin3"]
            if bin_num >= 4:
                dict_list[col]["Coef_WOE"]["bin4"] = float(dict_list[col]["Coef"]) * dict_list[col]["woe"]["bin4"]

        def splitCol(x, name):
            dic = eval(str(x))
            if (name in dic.keys()):
                return dic[name]
            else:
                return np.nan

        report = pd.DataFrame.from_dict(dict_list, orient='index')
        report["bin0"] = report["bin"].apply(lambda x: splitCol(x, "bin0"))
        report["bin1"] = report["bin"].apply(lambda x: splitCol(x, "bin1"))
        report["bin2"] = report["bin"].apply(lambda x: splitCol(x, "bin2"))
        report["bin3"] = report["bin"].apply(lambda x: splitCol(x, "bin3"))
        report["bin4"] = report["bin"].apply(lambda x: splitCol(x, "bin4"))

        report["woe_bin0"] = report["woe"].apply(lambda x: splitCol(x, "bin0"))
        report["woe_bin1"] = report["woe"].apply(lambda x: splitCol(x, "bin1"))
        report["woe_bin2"] = report["woe"].apply(lambda x: splitCol(x, "bin2"))
        report["woe_bin3"] = report["woe"].apply(lambda x: splitCol(x, "bin3"))
        report["woe_bin4"] = report["woe"].apply(lambda x: splitCol(x, "bin4"))

        report["pcnt_bin0"] = report["pcnt"].apply(lambda x: splitCol(x, "bin0"))
        report["pcnt_bin1"] = report["pcnt"].apply(lambda x: splitCol(x, "bin1"))
        report["pcnt_bin2"] = report["pcnt"].apply(lambda x: splitCol(x, "bin2"))
        report["pcnt_bin3"] = report["pcnt"].apply(lambda x: splitCol(x, "bin3"))
        report["pcnt_bin4"] = report["pcnt"].apply(lambda x: splitCol(x, "bin4"))

        report["bad_bin0"] = report["bad"].apply(lambda x: splitCol(x, "bin0"))
        report["bad_bin1"] = report["bad"].apply(lambda x: splitCol(x, "bin1"))
        report["bad_bin2"] = report["bad"].apply(lambda x: splitCol(x, "bin2"))
        report["bad_bin3"] = report["bad"].apply(lambda x: splitCol(x, "bin3"))
        report["bad_bin4"] = report["bad"].apply(lambda x: splitCol(x, "bin4"))

        report["score_bin0"] = report["score"].apply(lambda x: splitCol(x, "bin0"))
        report["score_bin1"] = report["score"].apply(lambda x: splitCol(x, "bin1"))
        report["score_bin2"] = report["score"].apply(lambda x: splitCol(x, "bin2"))
        report["score_bin3"] = report["score"].apply(lambda x: splitCol(x, "bin3"))
        report["score_bin4"] = report["score"].apply(lambda x: splitCol(x, "bin4"))

        report["woeCoef_bin0"] = report["Coef_WOE"].apply(lambda x: splitCol(x, "bin0"))
        report["woeCoef_bin1"] = report["Coef_WOE"].apply(lambda x: splitCol(x, "bin1"))
        report["woeCoef_bin2"] = report["Coef_WOE"].apply(lambda x: splitCol(x, "bin2"))
        report["woeCoef_bin3"] = report["Coef_WOE"].apply(lambda x: splitCol(x, "bin3"))
        report["woeCoef_bin4"] = report["Coef_WOE"].apply(lambda x: splitCol(x, "bin4"))
        report.drop(["bin", "woe", "pcnt", "bad", "score", "Coef_WOE"], inplace=True, axis=1)
        report.to_csv(saveFile)
        print("[生成评分卡完毕]")








