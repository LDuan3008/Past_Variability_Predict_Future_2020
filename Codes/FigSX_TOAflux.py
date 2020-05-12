import cdms2 as cdms, numpy as np
import cdutil
import matplotlib.pyplot as plt
import math
from Share_variables import data_path_return as new_data_path
import statsmodels.api as sm

def TOAswcs(HISSSP_3_110, model_name):
    vORG_110      = HISSSP_3_110.vORG
    HISm_mean_110 = HISSSP_3_110.HISm_mean
    HISm_spat_110 = HISSSP_3_110.HISm_spat
    EOFreturn1    = HISSSP_3_110.class_cal_eofs(vORG_110, HISm_mean_110, HISm_spat_110, idx=[-1], REA_idx=True)
    STDeof3 = EOFreturn1['std_EOFsOnHISm'][:, 3]
    vars_list = ['rsut', 'rsutcs']
    STDsw = []
    mondel_list = ['CNRM-CM6-1', 'CNRM-ESM2-1', 'MIROC-ES2L', 'UKESM1-0-LL']
    for idx1 in model_name:
        if idx1 in mondel_list:
            fopen2 = cdms.open(new_data_path + 'Returned_' + vars_list[1] + '_' + idx1 + '_historical_r1i1p1f2.nc')
        else:
            fopen2 = cdms.open(new_data_path + 'Returned_' + vars_list[1] + '_' + idx1 + '_historical_r1i1p1f1.nc')
        rsutcs  = fopen2('tEquArea',squeeze=1)
        used = cdutil.averager(rsutcs[-114:-4, -3:, :], axis='yx')
        std  = np.std(used)
        STDsw.append(std)
    STDsw = np.array(STDsw)
    fitT = sm.OLS(STDeof3, np.c_[np.ones(17), STDsw]).fit()
    pred = fitT.get_prediction(np.c_[np.ones(17), STDsw]).predicted_mean
    plt.scatter(STDsw, STDeof3)
    plt.plot(STDsw, pred, color='black')
    plt.xlim(0.6, 2.2)
    plt.ylim(0,  0.25)
    plt.show()
    plt.clf()