from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler #规范化，使各特征的均值为1，方差为0
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

#%matplotlib inline

data = datasets.load_iris()
col_name = data.feature_names
X = data.data
y = data.target
X = pd.DataFrame(X)
X.head(n=10)
X.sample(n=10)

# 箱型图
X.plot(kind='box')
# 条形图
X.hist(figsize=(12,5),xlabelsize=1,ylabelsize=1)
# 密度图
X.plot(kind="density",subplots=True,layout=(1,4),figsize=(12,5))
# 特征相关图
pd.plotting.scatter_matrix(X,figsize=(10,10))

# 特征相关性的热力图
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
cax = ax.matshow(X.corr(),vmin=-1,vmax=1,interpolation="none")
fig.colorbar(cax)
ticks = np.arange(0,4,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(col_name)
ax.set_yticklabels(col_name)
plt.show()


# 查找最优模型
models = []
models.append(("AB",AdaBoostClassifier()))
models.append(("GBM",GradientBoostingClassifier()))
models.append(("RF",RandomForestClassifier()))
models.append(("ET",ExtraTreesClassifier()))
models.append(("SVC",SVC()))
models.append(("KNN",KNeighborsClassifier()))
models.append(("LR",LogisticRegression()))
models.append(("GNB",GaussianNB()))
models.append(("LDA",LinearDiscriminantAnalysis()))

names = []
results = []


for name,model in models:
    kfold = KFold(n_splits=5,random_state=42)
    result = cross_val_score(model,X,y,scoring="accuracy",cv=kfold)
    names.append(name)
    results.append(result)
    print("{}  Mean:{:.4f}(Std{:.4f})".format(name,result.mean(),result.std()))

# Pipeline的使用
pipeline = []
pipeline.append(("ScalerET", Pipeline([("Scaler",StandardScaler()),
                                       ("ET",ExtraTreesClassifier())])))
pipeline.append(("ScalerGBM", Pipeline([("Scaler",StandardScaler()),
                                        ("GBM",GradientBoostingClassifier())])))
pipeline.append(("ScalerRF", Pipeline([("Scaler",StandardScaler()),
                                       ("RF",RandomForestClassifier())])))

names = []
results = []
for name, model in pipeline:
    kfold = KFold(n_splits=5,random_state=42)
    result = cross_val_score(model, X, y, cv=kfold, scoring="accuracy")
    results.append(result)
    names.append(name)
    print("{}:  Error Mean:{:.4f} (Error Std:{:.4f})".format(
        name,result.mean(),result.std()))


# 模型调节： 网格搜索
param_grid = {
    "C":[0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.3, 1.5, 1.7, 2.0],
    "kernel":['linear', 'poly', 'rbf', 'sigmoid']
}
model = SVC()
kfold = KFold(n_splits=5, random_state=42)
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring="accuracy", cv=kfold)
grid_result = grid.fit(X, y)
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))
