import numpy                                                                   as np
import matplotlib.pyplot                                                       as plt
import matplotlib.patches                                                      as patches
import statsmodels.api                                                         as sm
import pickle

def cal_MEMEX(instance):
    CHG_Mean_126   = instance.CHG_Mean_126
    CHG_Mean_245   = instance.CHG_Mean_245
    CHG_Mean_370   = instance.CHG_Mean_370
    CHG_Mean_585   = instance.CHG_Mean_585
    ECS_CMIP6      = instance.ECS_CMIP6
    SRstd_SSP126_STD, SRstd_SSP245_STD, SRstd_SSP370_STD, SRstd_SSP585_STD = [], [], [], []
    SRstd_SSP126_EOF, SRstd_SSP245_EOF, SRstd_SSP370_EOF, SRstd_SSP585_EOF = [], [], [], []
    SRstd_SSP126_LFO, SRstd_SSP245_LFO, SRstd_SSP370_LFO, SRstd_SSP585_LFO = [], [], [], []
    for idx in range(CHG_Mean_585.shape[1]):
        SRstd_SSP126, R2std_SSP126, Tpre_SSP126, Terr_SSP126 = instance.class_cal_loo(  'STD_only',  CHG_Mean_126[:,idx],  17, 1)
        SRstd_SSP245, R2std_SSP245, Tpre_SSP245, Terr_SSP245 = instance.class_cal_loo(  'STD_only',  CHG_Mean_245[:,idx],  17, 1)
        SRstd_SSP370, R2std_SSP370, Tpre_SSP370, Terr_SSP370 = instance.class_cal_loo(  'STD_only',  CHG_Mean_370[:,idx],  16, 1)
        SRstd_SSP585, R2std_SSP585, Tpre_SSP585, Terr_SSP585 = instance.class_cal_loo(  'STD_only',  CHG_Mean_585[:,idx],  17, 1)
        SRstd_SSP126_STD.append(SRstd_SSP126)
        SRstd_SSP245_STD.append(SRstd_SSP245)
        SRstd_SSP370_STD.append(SRstd_SSP370)
        SRstd_SSP585_STD.append(SRstd_SSP585)
        SReo3_SSP126, R2eo3_SSP126, Tpre_SSP126, Terr_SSP126 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_126[:,idx],  17, 1)
        SReo3_SSP245, R2eo3_SSP245, Tpre_SSP245, Terr_SSP245 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_245[:,idx],  17, 1)
        SReo3_SSP370, R2eo3_SSP370, Tpre_SSP370, Terr_SSP370 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_370[:,idx],  16, 1)
        SReo3_SSP585, R2eo3_SSP585, Tpre_SSP585, Terr_SSP585 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_585[:,idx],  17, 1)
        SRstd_SSP126_EOF.append(SReo3_SSP126)
        SRstd_SSP245_EOF.append(SReo3_SSP245)
        SRstd_SSP370_EOF.append(SReo3_SSP370)
        SRstd_SSP585_EOF.append(SReo3_SSP585)
        SReo3_LFO_SSP126 = instance.class_cal_lpo2(  'STD_EOFs',  CHG_Mean_126[:,idx],  17, 1)
        SReo3_LFO_SSP245 = instance.class_cal_lpo2(  'STD_EOFs',  CHG_Mean_245[:,idx],  17, 1)
        SReo3_LFO_SSP370 = instance.class_cal_lpo2(  'STD_EOFs',  CHG_Mean_370[:,idx],  16, 1)
        SReo3_LFO_SSP585 = instance.class_cal_lpo2(  'STD_EOFs',  CHG_Mean_585[:,idx],  17, 1)
        SRstd_SSP126_LFO.append(SReo3_LFO_SSP126)
        SRstd_SSP245_LFO.append(SReo3_LFO_SSP245)
        SRstd_SSP370_LFO.append(SReo3_LFO_SSP370)
        SRstd_SSP585_LFO.append(SReo3_LFO_SSP585)
    dict_return = {}
    dict_return['SRstd_SSP126_STD']        = SRstd_SSP126_STD
    dict_return['SRstd_SSP245_STD']        = SRstd_SSP245_STD
    dict_return['SRstd_SSP370_STD']        = SRstd_SSP370_STD
    dict_return['SRstd_SSP585_STD']        = SRstd_SSP585_STD
    dict_return['SRstd_SSP126_EOF']        = SRstd_SSP126_EOF
    dict_return['SRstd_SSP245_EOF']        = SRstd_SSP245_EOF
    dict_return['SRstd_SSP370_EOF']        = SRstd_SSP370_EOF
    dict_return['SRstd_SSP585_EOF']        = SRstd_SSP585_EOF
    dict_return['SRstd_SSP126_LFO']        = SRstd_SSP126_LFO
    dict_return['SRstd_SSP245_LFO']        = SRstd_SSP245_LFO
    dict_return['SRstd_SSP370_LFO']        = SRstd_SSP370_LFO
    dict_return['SRstd_SSP585_LFO']        = SRstd_SSP585_LFO
    import pickle
    with open('dict_test.pickle', 'wb') as handle:
        pickle.dump(dict_return, handle, protocol=pickle.HIGHEST_PROTOCOL)

def fig_LOObox():
    with open('dictSRLOO.pickle', 'rb') as handle:
        dict1 = pickle.load(handle)
    SRstd_SSP126_STD, SRstd_SSP126_EOF = np.array(dict1['SRstd_SSP126_STD']), np.array(dict1['SRstd_SSP126_EOF'])
    SRstd_SSP245_STD, SRstd_SSP245_EOF = np.array(dict1['SRstd_SSP245_STD']), np.array(dict1['SRstd_SSP245_EOF'])
    SRstd_SSP370_STD, SRstd_SSP370_EOF = np.array(dict1['SRstd_SSP370_STD']), np.array(dict1['SRstd_SSP370_EOF'])
    SRstd_SSP585_STD, SRstd_SSP585_EOF = np.array(dict1['SRstd_SSP585_STD']), np.array(dict1['SRstd_SSP585_EOF'])
    plt.boxplot(SRstd_SSP126_STD, positions=[0.1], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='green'))
    plt.boxplot(SRstd_SSP245_STD, positions=[0.2], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='orange'))
    plt.boxplot(SRstd_SSP370_STD, positions=[0.3], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='brown'))
    plt.boxplot(SRstd_SSP585_STD, positions=[0.4], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='red'))
    plt.boxplot(SRstd_SSP126_EOF, positions=[0.7], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='green'))
    plt.boxplot(SRstd_SSP245_EOF, positions=[0.8], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='orange'))
    plt.boxplot(SRstd_SSP370_EOF, positions=[0.9], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='brown'))
    plt.boxplot(SRstd_SSP585_EOF, positions=[1.0], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='red'))
    plt.axis('square')
    plt.xlim(0, 1.1)
    plt.ylim(0, 1.0)
    plt.show()
    plt.clf()

def fig_LOOprediction(instance):
    CHG_Mean_126   = instance.CHG_Mean_126
    CHG_Mean_245   = instance.CHG_Mean_245
    CHG_Mean_370   = instance.CHG_Mean_370
    CHG_Mean_585   = instance.CHG_Mean_585
    ECS_CMIP6      = instance.ECS_CMIP6
    idx = -1
    print ('start')
    SRstd_SSP126, R2std_SSP126, Tstd_SSP126, Terr_SSP126 = instance.class_cal_loo(  'STD_only',  CHG_Mean_126[:,idx],  17, 1)
    SRstd_SSP245, R2std_SSP245, Tstd_SSP245, Terr_SSP245 = instance.class_cal_loo(  'STD_only',  CHG_Mean_245[:,idx],  17, 1)
    SRstd_SSP370, R2std_SSP370, Tstd_SSP370, Terr_SSP370 = instance.class_cal_loo(  'STD_only',  CHG_Mean_370[:,idx],  16, 1)
    SRstd_SSP585, R2std_SSP585, Tstd_SSP585, Terr_SSP585 = instance.class_cal_loo(  'STD_only',  CHG_Mean_585[:,idx],  17, 1)
    
    SReo3_SSP126, R2eo3_SSP126, Treo_SSP126, Terr_SSP126 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_126[:,idx],  17, 1)
    SReo3_SSP245, R2eo3_SSP245, Treo_SSP245, Terr_SSP245 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_245[:,idx],  17, 1)
    SReo3_SSP370, R2eo3_SSP370, Treo_SSP370, Terr_SSP370 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_370[:,idx],  16, 1)
    SReo3_SSP585, R2eo3_SSP585, Treo_SSP585, Terr_SSP585 = instance.class_cal_loo(  'STD_EOFs',  CHG_Mean_585[:,idx],  17, 1)
    print ('end')
    def plot_each_case(ax, Treal, Tpred1, Tpred2, color):
        ax.scatter(Treal, Tpred1, s=20, color=color)
        ax.scatter(Treal, Tpred2, s=20, color=color, facecolor='none')
    ax = plt.subplot(111)
    ax.plot(np.arange(8), np.arange(8), linestyle='--', linewidth=0.5, color='black')
    plot_each_case(ax, CHG_Mean_126[:,idx], Treo_SSP126, Tstd_SSP126, 'green')
    plot_each_case(ax, CHG_Mean_245[:,idx], Treo_SSP245, Tstd_SSP245, 'orange')
    plot_each_case(ax, CHG_Mean_370[:,idx], Treo_SSP370, Tstd_SSP370, 'brown')
    plot_each_case(ax, CHG_Mean_585[:,idx], Treo_SSP585, Tstd_SSP585, 'red')
    plt.axis('square')
    plt.xlim(0,7)
    plt.ylim(0,7)
    plt.show()
    plt.clf()