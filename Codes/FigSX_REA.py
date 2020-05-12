import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import statsmodels.api as sm

def separate_frequency_linear(HISm_mean, REA=0):
    hig_list = []
    low_list = []
    org_list = []
    if REA == 0:
        hig_list = []
        low_list = []
        org_list = []
        for i in range(HISm_mean.shape[0]):
            ts = HISm_mean[i]
            xx = np.c_[np.ones(ts.shape[0]), np.arange(ts.shape[0]) ]
            regress = sm.OLS(ts, xx).fit()
            predict = regress.get_prediction(xx)
            low = predict.predicted_mean
            hig = ts - low
            low_list.append(np.std(low))
            hig_list.append(np.std(hig))
            org_list.append(np.std( ts))
        low_list = np.array(low_list)
        hig_list = np.array(hig_list)
        org_list = np.array(org_list)
        return (org_list)
    if REA == 1:
        ts = HISm_mean
        xx = np.c_[np.ones(ts.shape[0]), np.arange(ts.shape[0]) ]
        regress = sm.OLS(ts, xx).fit()
        predict = regress.get_prediction(xx)
        low = predict.predicted_mean
        hig = ts - low
        return np.std(ts)

def CheckREA(instance, model_name):
    vORG      = instance.vORG
    HISm_mean = instance.HISm_mean
    HISm_spat = instance.HISm_spat
    EOFreturn1    = instance.class_cal_eofs(vORG, HISm_mean, HISm_spat, idx=[-1], REA_idx=True)
    HISp_mean_era20c   = EOFreturn1['HISp_mean_era20c']
    HISp_mean_20crv3   = EOFreturn1['HISp_mean_20crv3']
    modelEnsemble = np.mean(HISm_mean, axis=0)
    CHG_Mean_585   = instance.CHG_Mean_585
    plt.plot(np.arange(110)+1901, modelEnsemble-np.mean(modelEnsemble), color='black')
    plt.plot(np.arange(110)+1901, HISp_mean_era20c-np.mean(HISp_mean_era20c), color='green')
    plt.plot(np.arange(110)+1901, HISp_mean_20crv3-np.mean(HISp_mean_20crv3), color='royalblue')
    for i in range(17):
        plt.plot(np.arange(110)+1901, HISm_mean[i]-np.mean(HISm_mean[i]), color='black', linestyle='--')
    plt.xlim(1900, 2010)
    plt.show()
    plt.clf()