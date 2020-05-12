import cdutil, pickle
import numpy                                                                   as np
import scipy.stats                                                             as stats
import matplotlib.pyplot                                                       as plt
import matplotlib.patches                                                      as patches
import statsmodels.api                                                         as sm
from Function_regressions                                                      import get_regression_prediction as GRP
def fig_contributions(instance_110):
    vORG_110      = instance_110.vORG
    HISm_mean_110 = instance_110.HISm_mean
    HISm_spat_110 = instance_110.HISm_spat
    EOFreturn1    = instance_110.class_cal_eofs(vORG_110, HISm_mean_110, HISm_spat_110, idx=[-1], REA_idx=True)
    CHG_Mean_126 = instance_110.CHG_Mean_126
    CHG_Mean_245 = instance_110.CHG_Mean_245
    CHG_Mean_370 = instance_110.CHG_Mean_370
    CHG_Mean_585 = instance_110.CHG_Mean_585
    predictor1    = np.c_[EOFreturn1['std_HISm'], EOFreturn1['std_EOFsOnHISm'][:,1:-1] ]
    input_predictand_reanalysis1  = np.r_[EOFreturn1['std_era20c'],   EOFreturn1['std_EOFs_era20c'][1:-1]  ]
    input_predictand_reanalysis2  = np.r_[EOFreturn1['std_20crv3'],   EOFreturn1['std_EOFs_20crv3'][1:-1]  ]
    def plot_bar_contribution(y_array, x_array, num):
        new_x_arrays = np.c_[np.ones(num), x_array]
        term1 = np.mean(EOFreturn1['std_HISm'])
        term2 = np.mean(EOFreturn1['std_EOFsOnHISm'][:,1:-1], axis=0)
        new_predictm = np.r_[1, term1, term2]
        new_predict1 = np.r_[1, input_predictand_reanalysis1]
        new_predict2 = np.r_[1, input_predictand_reanalysis2]
        
        regress = sm.OLS(y_array, new_x_arrays).fit()
        predicm = new_predictm * regress.params
        predic1 = new_predict1 * regress.params
        predic2 = new_predict2 * regress.params
        predicm_sum = np.sum(predicm)
        predic1_sum = np.sum(predic1)
        predic2_sum = np.sum(predic2)
        
        To_plot1 = np.r_[predic1_sum-predicm_sum, predic1[1:]-predicm[1:]]
        To_plot2 = np.r_[predic2_sum-predicm_sum, predic2[1:]-predicm[1:]]
        plt.plot(np.r_[-0.5, 4.5], np.r_[0,0], color='black', linewidth=0.5)
        plt.bar(np.arange(5)-0.1, np.array(To_plot1), 0.2)
        plt.bar(np.arange(5)+0.1, np.array(To_plot2), 0.2)
        plt.xlim(-0.5, 4.5)
        plt.show()
        plt.clf()
        plt.plot(np.r_[-1, 4], np.r_[0,0], color='black', linewidth=0.5)
        plt.bar(np.arange(4), regress.params[1:], 0.6)
        plt.xlim(-1, 4)
        plt.show()
        plt.clf()
    idx = 64
    plot_bar_contribution(CHG_Mean_585[:,idx], predictor1, 17)