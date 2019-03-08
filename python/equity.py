import talib as ta
import pandas as pd
import numpy as np
import os
import shap
from pandas_finance import Equity
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot as plt


def get_candle_features(df, target='return_t+1', remove_zero_days=False):
    cdl_methods = [m for m in dir(ta) if 'CDL' in m]
    df_cdl = pd.DataFrame(index=df.index)

    for mtd in cdl_methods:
        df_cdl[mtd] = getattr(ta, mtd)(df['Open'], df['High'], df['Low'], df['Close'])
    tgt = df[target]

    if remove_zero_days:
        non_zero = df_cdl.sum(axis=1) > 0
        tgt = tgt[non_zero]
        df_cdl = df_cdl[non_zero]
    return df_cdl, tgt

def rmse(ytrue, ypred):
    return np.sqrt(mean_squared_error(ytrue, ypred))

def plot_res(ytrue, base_zero, base_avg, pred, name):
    r1,r2,r3 = rmse(ytrue, base_zero), rmse(ytrue, base_avg), rmse(ytrue, pred)
    r2 = r2 - r1
    r3 = r3 - r1

    name = "Difference from zero baseline - {}".format(name)
    fig = pd.Series([0,r2,r3], index=['Zero', 'Train average', 'Random Forest']).plot.bar(title=name)
    plt.tight_layout()
    plt.savefig(name)
    os.system("open '" + name + ".png'")

def train():
    sp500 = Equity("^GSPC").trading_data
    sp500['return_t+1'] = sp500['Adj Close'].pct_change(1).shift(-1)
    sp500['return_t+3'] = sp500['Adj Close'].pct_change(3).shift(-3)
    sp500 = sp500.iloc[:-5]

    xtrain, ytrain = get_candle_features(sp500.loc[:"2009-01-01"], 'return_t+1', True)
    xval, yval = get_candle_features(sp500.loc["2009-01-01":], 'return_t+1', True)
    base_avg = np.ones(yval.shape)*ytrain.mean()
    base_zero = np.zeros(yval.shape)

    mdl = RandomForestRegressor(n_estimators=10000, n_jobs=6)
    mdl.fit(xtrain, ytrain)

    p = mdl.predict(xval)
    plot_res(yval, base_zero, base_avg, p, "T+1 - Pre-selection")

    shap.initjs()
    explainer = shap.TreeExplainer(mdl)
    shap_values = explainer.shap_values(Xtrain)
    shap.summary_plot(shap_values, Xtrain)
