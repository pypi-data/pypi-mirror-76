from ..pipelineExecutor import pipelineExecutor
from sklearn.model_selection import KFold
from modelProcessor.performance import performance
import os,gc,pickle
import statsmodels.api as sm
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
import warnings,joblib
from keras.wrappers.scikit_learn import KerasClassifier
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

###lgb模型训练
class executor_mlpModelTrainHandle(pipelineExecutor):
    def __init__(self,ctx):
        super(executor_mlpModelTrainHandle,self).__init__()
        self.__ctx = ctx
        self._model=None
        self._dim = None

    def __createModel(self):
        model = Sequential()
        # model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
        # model.add(Dense(8, init='uniform', activation='relu'))
        # model.add(Dense(1, init='uniform', activation='sigmoid'))

        # model.add(Dense(128, activation='relu', input_dim=self._dim))
        model.add(Dense(32, activation='relu',init='normal', input_dim=self._dim))
        model.add(Dense(16, activation='relu',init='normal',))
        model.add(Dense(8, activation='relu', init='normal', ))
        # model.add(Dropout(0.5))
        model.add(Dense(1, init='uniform',activation='sigmoid'))
        model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])
        return  model
    def _mlpGridSearch(self,x_train, x_test, y_train, y_test):
        model = KerasClassifier(build_fn=self.__createModel, verbose=0)
        batch_size = [10, 20, 40, 60, 80, 100]
        epochs = [10, 50, 100]
        param_grid = dict(batch_size=batch_size, nb_epoch=epochs)
        grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1)
        grid_result = grid.fit(x_train, y_train)
        print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))

        # for params, mean_score, scores in grid_result.s:
        #     print("%f (%f) with: %r" % (scores.mean(), scores.std(), params))


    def _mlpTrainDefault(self, x_train, x_test, y_train, y_test):

        model = KerasClassifier(build_fn=self.__createModel, nb_epoch=50, batch_size=10)
        kfold = StratifiedKFold(n_splits=5,shuffle=True,random_state=22)
        # auc = cross_val_score(model, x_train, y_train, cv=kfold)

        model.fit(x_train, y_train)

        y_pred = model.predict_proba(x_test)
        print("y_pred:::",y_pred     )
        scores = performance.Prob2Score(y_pred[:, 0], self.__ctx.task.basePoint, self.__ctx.task.odds)

        report_ks = os.path.join(self.__ctx.task_train_mlp.reports_baseDir, self.__ctx.task_train_mlp.reports_ks)
        pic_ks = os.path.join(self.__ctx.task_train_mlp.reports_baseDir, self.__ctx.task_train_mlp.reports_ks_png)

        ks = performance.KS(scores, y_test, report_ks, pic_ks)
        test_auc = roc_auc_score(y_test, y_pred[:, 0])
        # print("     训练集auc.mean():{},auc.std:{}".format(auc.mean(), auc.std()))
        print("     测试集KS：", ks)
        print("     测试集AUC：", test_auc)
        print("     ----------------------")

    def __modelExport(self):
        coefFile = os.path.join(self.__ctx.task_train_lgb.model_baseDir, self.__ctx.task_train_lgb.model_coef)
        joblibFile = os.path.join(self.__ctx.task_train_lgb.model_baseDir, self.__ctx.task_train_lgb.model_joblib_pkl)

        self._model.booster_.save_model(coefFile)
        print("     [生成权重文件]:", coefFile)
        joblib.dump(self._model, joblibFile)
        print("     [生成模型文件]:", joblibFile)

    def executor(self,df):
        warnings.filterwarnings('ignore')
        print("[mlp模型训练] 训练方式:",self.__ctx.task_train_mlp.model_trian_type)
        obj_cols = [self.__ctx.train.data_label]
        for col in df.columns:
            if str(df[col].dtype) == 'object':
                obj_cols.append(col)
        print("     删除字符型(日期)变量:", obj_cols)
        numerical_cols = df.columns.drop(obj_cols)

        x = df[numerical_cols]
        y = df[self.__ctx.train.data_label]
        df=df[numerical_cols.tolist()+[self.__ctx.train.data_label]]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=22)
        self._dim = x_train.shape[1]
        # self._mlpTrainDefault(x_train, x_test, y_train, y_test)
        self._mlpGridSearch(x_train, x_test, y_train, y_test)
        # self.__modelExport()
        return df