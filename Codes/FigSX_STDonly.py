import numpy                                                                   as np
import matplotlib.pyplot                                                       as plt
import statsmodels.api                                                         as sm
def fig_StdGMSATonly(instance):
    std_HISm  = instance.std_HISm
    CHG_Mean_126 = instance.CHG_Mean_126
    CHG_Mean_245 = instance.CHG_Mean_245
    CHG_Mean_370 = instance.CHG_Mean_370
    CHG_Mean_585 = instance.CHG_Mean_585
    EOFreturn  = instance.class_cal_eofs(instance.vORG, instance.HISm_mean, instance.HISm_spat, idx=[-1], REA_idx=True)
    MeaEra20c = EOFreturn['HISp_mean_era20c']
    Mea20crv3 = EOFreturn['HISp_mean_20crv3']
    def plotSSP(std_HISm, CHG_Mean, is370, left, right, upper, name, MeaEra20c, Mea20crv3):
        TotNum = std_HISm.shape[0]
        DeltaT_SSP_2079_2099 = CHG_Mean[:,-1]
        std_HISm_AddCon = np.c_[np.ones(TotNum), std_HISm]
        text1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' I' ,'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
        total_index_lit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        if is370 == True:
            TotNum          = TotNum - 1
            std_HISm        = np.delete(std_HISm, 15)
            std_HISm_AddCon = np.delete(std_HISm_AddCon, 15, axis=0)
            text1           = np.delete(text1, 15)
            total_index_lit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        fitT                = sm.OLS(DeltaT_SSP_2079_2099, std_HISm_AddCon).fit()
        pred                = fitT.get_prediction(std_HISm_AddCon)
        Tcen                = pred.predicted_mean
        extended_left_cen   = fitT.get_prediction([1, left]).predicted_mean
        extended_right_cen  = fitT.get_prediction([1, right]).predicted_mean
        std_HISm_extend     = np.r_[left, std_HISm, right]
        Tcen_extend         = np.r_[extended_left_cen, Tcen, extended_right_cen]
        Tstd                = pred.se_obs
        extended_left_std   = fitT.get_prediction([1, left]).se_obs
        extended_right_std  = fitT.get_prediction([1, right]).se_obs
        Tstd_extend = np.r_[extended_left_std, Tstd, extended_right_std]
        Lboun = Tcen_extend - Tstd_extend
        Uboun = Tcen_extend + Tstd_extend
        sortarg = np.argsort(std_HISm_extend)
        std_era20c = np.std(MeaEra20c)
        std_20crv3 = np.std(Mea20crv3)
        # Now Plot
        plt.plot(std_HISm_extend[sortarg], Tcen_extend[sortarg],  linewidth=1, color='black', linestyle='dashdot')
        plt.plot(std_HISm_extend[sortarg], Lboun[sortarg],        linewidth=1, color='black', linestyle='dashed')
        plt.plot(std_HISm_extend[sortarg], Uboun[sortarg],        linewidth=1, color='black', linestyle='dashed')
        plt.fill_between(std_HISm_extend[sortarg], Lboun[sortarg], Uboun[sortarg], facecolor='grey', alpha=0.2)
        for i in range(TotNum):
            plt.text(std_HISm[i], DeltaT_SSP_2079_2099[i], text1[i], {'color': 'firebrick', 'fontsize':8, 'ha':'center', 'va':'center'})
        plt.plot(np.r_[std_era20c, std_era20c], np.r_[0, upper], color='green', linestyle='--')
        plt.plot(np.r_[std_20crv3, std_20crv3], np.r_[0, upper], color='royalblue', linestyle='--')
        plt.xlim(left, right)
        plt.ylim(0,    upper)
        plt.show()
        plt.clf()
    plotSSP(std_HISm, CHG_Mean_126, False, 0.18, 0.40, 3, 'P1FSX', MeaEra20c, Mea20crv3)
    plotSSP(std_HISm, CHG_Mean_245, False, 0.18, 0.40, 5, 'P2FSX', MeaEra20c, Mea20crv3)
    plotSSP(std_HISm, CHG_Mean_370, True,  0.18, 0.40, 6, 'P3FSX', MeaEra20c, Mea20crv3)
    plotSSP(std_HISm, CHG_Mean_585, False, 0.18, 0.40, 8, 'P4FSX', MeaEra20c, Mea20crv3)