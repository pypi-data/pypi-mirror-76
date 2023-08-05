
# coding=utf-8
import os
import numbers
from sklearn.preprocessing import LabelEncoder
from dataProcessor.binCut import *
from dataProcessor.dataReports import statistics as Reports
import matplotlib.pyplot as plt
import numpy as np
class normalization:
    @staticmethod
    def maxMinNormalization(df, scale_columns):
        min_max_scaler = lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
        df[scale_columns] = df[scale_columns].apply(min_max_scaler)
        print("[completed min_max_scale!!!]")

    @staticmethod
    def stdNormalization(df, scale_columns):
        z_score_scaler = lambda x: (x - np.mean(x)) / (np.std(x))
        df[scale_columns] = df[scale_columns].apply(z_score_scaler)

class featureCalc:
    @staticmethod
    #删除只有单一值的变量
    def __delConstantFeature(df):
        findFlag=False
        print("df.shape:",df.shape)
        cls=df.columns.tolist()
        for col in cls:
            conValue = []
            for i in range(df.shape[0]):
                if  df.iloc[i][col] not in conValue:
                    conValue.append(df[col][i])
                    if len(conValue)>1:
                        break;
                if i==df.shape[0]:
                    findFlag=True
                    print('[delete {} from the dataset because it is a constant]'.format(col))
                    del df[col]
        if findFlag == False:
            print("[didn't find any constant feature]")
    #获取数值特征
    @staticmethod
    def getNumericalCols(df,n=10):
        print("----getNumericalCols----df.shape:", df.shape)
        numerical_var=[]
        #1,删除单一值值变量
        featureCalc.__delConstantFeature(df)
        #2,返回数值型变量
        for i,col in enumerate(df.columns):
            print("正在处理第{}个特征：{}".format(i,col))
            uniq_vals = []
            ##   是实数 且大于n
            if isinstance(df[col][0], numbers.Real):
                for i  in range(df.shape[0]):
                    if df.iloc[i][col] not in uniq_vals:
                        uniq_vals.append(df.iloc[i][col])
                        if len(uniq_vals)>=n:
                            numerical_var.append(col)
                            break

        return numerical_var

    #检查变量的最多值的占比情况,以及每个变量中占比最大的值，生成前500名报告
    @staticmethod
    def genMaxFeatureValuePercent(df):
        col_most_values, col_large_value = {}, {}
        records_count = df.shape[0]
        for col in df.columns:
            value_count = df[col].groupby(df[col]).count()
            col_most_values[col] = max(value_count) / records_count
            large_value = value_count[value_count == max(value_count)].index[0]
            col_large_value[col] = large_value
        col_most_values_df = pd.DataFrame.from_dict(col_most_values, orient='index')
        col_most_values_df.columns = ['max percent']
        col_most_values_df = col_most_values_df.sort_values(by='max percent', ascending=False)
        pcnt = list(col_most_values_df[:500]['max percent'])
        vars = list(col_most_values_df[:500].index)

        # dis=df[col].value_counts(dropna=False)
        dis = col_most_values_df[:500]['max percent']
        ax = dis.plot(title=col + "distribution", kind="bar", figsize=(18, 12), fontsize=14)
        ax.get_figure().savefig("maxPercentFeatureValue.png")
        return  col_most_values_df,col_large_value

    @staticmethod
    def checkMaxPercentageVariable(df,col_most_values_df,col_large_value):
        # 计算多数值占比超过90%的字段中，少数值的坏样本率是否会显著高于多数值
        large_percent_cols = list(col_most_values_df[col_most_values_df['max percent'] >= 0.9].index)
        bad_rate_diff = {}
        for col in large_percent_cols:
            large_value = col_large_value[col]
            temp = df[[col, 'target']]
            temp[col] = temp.apply(lambda x: int(x[col] == large_value), axis=1)
            bad_rate = temp.groupby(col).mean()
            if bad_rate.iloc[0]['target'] == 0:
                bad_rate_diff[col] = 0
                continue
            bad_rate_diff[col] = np.log(bad_rate.iloc[0]['target'] / bad_rate.iloc[1]['target'])
        bad_rate_diff_sorted = sorted(bad_rate_diff.items(), key=lambda x: x[1], reverse=True)
        bad_rate_diff_sorted_values = [x[1] for x in bad_rate_diff_sorted]
        plt.bar(x=range(len(bad_rate_diff_sorted_values)), height=bad_rate_diff_sorted_values)

        ##TBD 删除没有显著高于多数值的特征

        # 由于所有的少数值的坏样本率并没有显著高于多数值，意味着这些变量可以直接剔除
        for col in large_percent_cols:
            if col in numerical_var:
                numerical_var.remove(col)
            else:
                categorical_var.remove(col)
            del allData[col]
    @staticmethod
    def __missingCategorial(df, x):
        missing_vals = df[x].map(lambda x: int(x != x))
        return sum(missing_vals) * 1.0 / df.shape[0]
    @staticmethod
    def delHighMissCategoryFeature(df,categoryList,threshHold = 0.8):
        #删除缺失值高于80%的特征，对于低于80%的用特殊值替代
        for col in categoryList:
            missingRate = featureTools.featureCalc.__missingCategorial(df, col)
            print('{0} has missing rate as {1}'.format(col, missingRate))
            if missingRate > threshHold:
                # categorical_var.remove(col)
                del df[col]
            if 0 < missingRate < threshHold:
                uniq_valid_vals = [i for i in df[col] if i == i]
                uniq_valid_vals = list(set(uniq_valid_vals))
                if isinstance(uniq_valid_vals[0], numbers.Real):
                    missing_position = df.loc[df[col] != df[col]][col].index
                    not_missing_sample = [-1] * len(missing_position)
                    df.loc[missing_position, col] = not_missing_sample
                else:
                    # In this way we convert NaN to NAN, which is a string instead of np.nan
                    df[col] = df[col].map(lambda x: str(x).upper())

    # 异常值分析
    @staticmethod
    def Outlier_Dectection(df, x):
        '''
        :param df:
        :param x:
        :return:
        '''
        p25, p75 = np.percentile(df[x], 25), np.percentile(df[x], 75)
        d = p75 - p25
        upper, lower = p75 + 3 * d, p25 - 3 * d
        truncation = df[x].map(lambda x: max(min(upper, x), lower))
        return truncation



class encoder:
    @staticmethod
    def labeEncoder( df, columns,encoderOutputFolder):
        for col in columns:
            encoder = LabelEncoder().fit(df[col])
            df[col] = encoder.transform(df[col])
            np.savetxt(os.path.join(encoderOutputFolder,col),encoder.classes_,delimiter=",")
            # np.savetxt(os.path.join("./dataReports/labelEncode", col), encoder.classes_, delimiter=",")

        print("[completed labeEncoder!!!] encode info saved in ./dataReports/labelEncode")

    @staticmethod
    def oneHotEncoder(df,cols):
        df=pd.get_dummies(df,columns=cols)
        ##TBD: save onehot info
        print("[completed oneHotEncoder!!!]")
        return df
class factorCalc:
    @staticmethod
    def genCorrReports(df):
        pass

    #VIF>10可以认为变量间存在多重共线性
    @staticmethod
    def genVIFReports(df):
        pass
    @staticmethod
    def genIVReport(df):
        print("[Compeleted calIV_genReport!!!]")

class featureTools():
    reports=Reports()
    binCut=binCut()
    normalization=normalization()
    encoder=encoder()
    featureCalc=featureCalc()
    factorCalc=factorCalc()


    class timeWindowCal:
        @staticmethod
        ### 对时间窗口，计算累计产比 ###
        def timeWindowSelection(df, daysCol, time_windows):
            '''
            :param df: the dataset containg variabel of days
            :param daysCol: the column of days
            :param time_windows: the list of time window
            :return:
            '''
            freq_tw = {}
            for tw in time_windows:
                freq = sum(df[daysCol].apply(lambda x: int(x <= tw)))
                freq_tw[tw] = freq
            return freq_tw


