import numpy as np
import pandas as pd
import os
#混淆矩阵计算
from sklearn.metrics import precision_score
from sklearn.metrics import roc_auc_score,accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import cross_val_score

class performance:
    @staticmethod
    def Prob2Score(prob, basePoint, PDO):
        # 将概率转化成分数且为正整数
        y = np.log(prob / (1 - prob))
        y2 = basePoint + PDO / np.log(2) * (-y)
        score = y2.astype("int")
        return score
    @staticmethod
    ### 计算KS值
    def KS(scores,auc,y_test,dataFile=None,picFile=None,bins=20):

        df = pd.DataFrame({'y_real': list(y_test), 'score': scores})
        total = df.groupby(["score"])["y_real"].count()
        bad = df.groupby(["score"])["y_real"].sum()
        all = pd.DataFrame({'total': total, 'bad': bad})
        all['good'] = all['total'] - all['bad']
        all["scores"] = all.index
        all = all.sort_values(by="scores")
        all.index = range(len(all))
        all["badCnt"] = all['bad'].cumsum()
        all["goodCnt"] = all['good'].cumsum()
        all['badCumRate'] = all["badCnt"] / all['bad'].sum()
        all['goodCumRate'] = all["goodCnt"] / all['good'].sum()
        all['KS'] = all.apply(lambda x: x.badCumRate - x.goodCumRate, axis=1)
        if dataFile!=None:
            all.to_csv(dataFile)
            print("     [completed save ksReport!!]:", dataFile)
        if picFile!=None:
            # pic = all[["badCumRate", "goodCumRate","scores"]]
            # pic = pic.set_index("scores")
            # ax = pic.plot(title="ks="+str(max(all['KS'] ))+"\nauc="+str(auc), figsize=(18, 12), fontsize=14, )
            # ax.get_figure().savefig(picFile)

            # interval = (all["scores"].max() - all["scores"].min()) / bins
            # freq_bins = np.arange(all["scores"].min() * 0.9, all["scores"].max() * 1.1, interval)

            ## ax1:ks曲线
            fig = plt.figure(figsize=(20, 12))
            ax1 = fig.add_subplot(111)
            ax1.plot(all[["scores"]], all[["badCumRate"]], label="badRate")
            ax1.plot(all[["scores"]], all[["goodCumRate"]], label="goodRate")
            ax1.set_ylabel("PD")
            ax1.set_xlabel("scores")
            ax1.set_title("ks=" + str(max(all['KS'])) + "\nauc=" + str(auc))

            ## ax2:scores分布
            freq_bins = np.linspace(df["score"].min() - 1, df["score"].max(), int(bins) + 1)
            df.sort_values(by="score",inplace=True)
            df["bin"] = pd.cut(df["score"], freq_bins)
            grop = pd.DataFrame(df.groupby("bin")["score"].count())
            grop.columns = ["cnt"]
            final = pd.merge(df, grop, on='bin', how='left')
            final.drop_duplicates(subset=["bin"], inplace=True)
            final["ratio"] = final["cnt"] / final["cnt"].sum()
            ax2 = ax1.twinx()

            ax2.plot(final["score"], final["ratio"], 'o-', color='grey', label="user distribution")
            ax2.bar(final["score"], final["ratio"], width=5, align='center', color='r', label="user distribution")
            # 变化率标签
            for i in final.index:
                x = final.loc[i, "score"]
                y_ratio = final.loc[i, "ratio"]
                y_cnt = final.loc[i, "cnt"]
                y_bin = final.loc[i, "bin"]
                if True:#大于10% 文字内容显示在下方
                    ax2.text(x, y_ratio - final["ratio"].max() * 0.03, ('%i' % y_cnt), ha='center',
                             va='bottom', fontsize=13)
                    ax2.text(x, y_ratio - final["ratio"].max() * 0.05, ('%s' % (y_bin)), ha='center', va='bottom',
                             fontsize=13)
                    ax2.text(x, y_ratio + final["ratio"].max() * 0.02, ('%.2f%%' % (y_ratio * 100)), ha='center', va='bottom',
                             fontsize=13)
                else:##小于10%,文字内容显示在上方
                    ax2.text(x, y_ratio + final["ratio"].max() * 0.04, ('%.2f%% %i' % (y_ratio * 100,y_cnt)), ha='center', va='bottom',fontsize=13)
                    ax2.text(x, y_ratio + final["ratio"].max() * 0.02, ('%s' % (y_bin)), ha='center', va='bottom',fontsize=13)
            ax2.set_ylabel("ratio")
            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            plt.legend(handles1 + handles2, labels1 + labels2, loc='upper right')

            ax1.get_figure().savefig(picFile, bbox_inches='tight')
            print("     [completed save ks.png!!]:", picFile)

        return max(all['KS'] )

    @staticmethod
    def confusionMatrixcal(y_test,y_pred):
        # f1 = f1_score(y_test, y_pred, average='binary')
        aauc = roc_auc_score(y_test, y_pred)
        print("     [auc]: ", aauc)

        # p = precision_score(y_test, y_pred, average='binary')
        # r = recall_score(y_test, y_pred, average='binary')
        # # aauc = accuracy_score(y_test, y_pred)
        #
        # print('[f1]:  ', f1)
        # print('[p]:   ', p)
        # print('[r]:   ', r)


    @staticmethod
    def cv5_performance(model,df_X,df_y):
        warnings.filterwarnings('ignore')
        accuracy = cross_val_score(model, df_X, df_y, scoring='accuracy', cv=5)
        precision = cross_val_score(model, df_X, df_y, scoring='precision', cv=5)
        recall = cross_val_score(model, df_X, df_y, scoring='recall', cv=5)
        f1_score1 = cross_val_score(model, df_X, df_y, scoring='f1', cv=5)
        auc = cross_val_score(model, df_X, df_y, scoring='roc_auc', cv=5)
        print("准确率:", accuracy.mean())
        print("精确率:", precision.mean())
        print("召回率:", recall.mean())
        print("F1_score:", f1_score1.mean())
        print("AUC:", auc.mean())

    @staticmethod
    def psi_calculation2Set(model,psi_report,psi_png,df1,df2,name1,name2,basePoint,odds,bins=10):
        ## score df
        pred_df1=model.predict_proba(df1)
        score_df1=performance.Prob2Score(pred_df1[:, 1],basePoint, odds)
        ddf1=pd.DataFrame(score_df1.tolist(),columns=["score"])
        ddf1.sort_values(by="score",inplace=True)
        ddf1=ddf1.reset_index(drop=True)

        pred_df2 = model.predict_proba(df2)
        score_df2 = performance.Prob2Score(pred_df2[:, 1], basePoint, odds)
        ddf2 = pd.DataFrame(score_df2.tolist(),columns=["score"])
        ddf2.sort_values(by="score",inplace=True)
        ddf2=ddf2.reset_index(drop=True)
        ## bin df
        mmax=max(score_df1.max(),score_df2.max())
        mmin = min(score_df1.min(), score_df2.min())

        freq_bins=np.linspace(mmin-1, mmax, bins+1)

        ddf1["bin_score"] = pd.cut(ddf1["score"], freq_bins)
        ddf2["bin_score"] = pd.cut(ddf2["score"], freq_bins)

        ##agg df
        agg1 = pd.DataFrame(ddf1.groupby("bin_score").count())
        agg1.columns=[name1]
        rst1 = pd.merge(ddf1,agg1,on="bin_score",how="left")
        rst1.drop_duplicates(subset="bin_score",inplace=True)
        rst1[name1+"_ratio"]=rst1[name1]/rst1[name1].sum()

        agg2 = pd.DataFrame(ddf2.groupby("bin_score").count())
        agg2.columns = [name2]
        rst2 = pd.merge(ddf2, agg2, on="bin_score", how="left")
        rst2.drop_duplicates(subset="bin_score", inplace=True)
        rst2[name2+"_ratio"] = rst2[name2] / rst2[name2].sum()

        ## final df
        final =pd.merge(rst1,rst2,on="bin_score",how="left")[["bin_score",name1,name1+"_ratio",name2,name2+"_ratio"]]
        final[name1+"_"+name2+"_psi"]=(final[name1+"_ratio"]-final[name2+"_ratio"])*np.log(final[name1+"_ratio"]/final[name2+"_ratio"])
        final["total_psi"]=final[name1+"_"+name2+"_psi"].sum()

        ## save report
        final.to_csv(psi_report,index=None)
        fig = plt.figure(figsize=(18, 12))
        ax1 = fig.add_subplot(111)
        ax1.plot(final.index, final[name1+"_"+name2+"_psi"], 'o-',label="psi")
        ax1.bar(final.index, final[name1+"_"+name2+"_psi"],width=.3, align='center',color='r',  label="psi")
        ax1.set_ylabel("psi")
        ax1.set_xlabel("bin_score")
        ax1.set_xticks(final.index)
        ax1.set_xticklabels(final["bin_score"])

        ax1.set_title("total psi={}%\n {}_count={},{}_count={}\n".format(final[name1+"_"+name2+"_psi"].sum()*100,
                                                                              name1,final[name1].sum(),
                                                                              name2,final[name2].sum()))

        # 变化率标签
        for i in final.index:
            psi = final.loc[i, name1+"_"+name2+"_psi"]
            cnt1 = final.loc[i, name1]
            cnt2 = final.loc[i, name2]
            ax1.text(i, psi + final[name1+"_"+name2+"_psi"].max() * 0.01, ('{}_cnt={}\n{}_cnt={}'.format(name1,cnt1,name2,cnt2)), ha='center',
                     va='bottom', fontsize=13)
            ax1.text(i, psi + final[name1+"_"+name2+"_psi"].max() * 0.06, ('%.2f%%' % (psi * 100)), ha='center',
                     va='bottom',
                     fontsize=13)

        handles1, labels1 = ax1.get_legend_handles_labels()
        plt.legend(handles1 , labels1 , loc='upper right')
        ax1.get_figure().savefig(psi_png, bbox_inches='tight')
        print("     [已生成Psi报告]:", psi_report,psi_png)

