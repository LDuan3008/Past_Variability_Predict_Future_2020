import numpy                                                                   as np
import matplotlib.pyplot                                                       as plt
import matplotlib.patches                                                      as patches
import statsmodels.api                                                         as sm
import pickle
def fig_cross_validation3(instance):
    CHG_Mean_126   = instance.CHG_Mean_126
    CHG_Mean_245   = instance.CHG_Mean_245
    CHG_Mean_370   = instance.CHG_Mean_370
    CHG_Mean_585   = instance.CHG_Mean_585
    SRstd_SSP126_STDLFO, SRstd_SSP245_STDLFO, SRstd_SSP370_STDLFO, SRstd_SSP585_STDLFO = [], [], [], []
    for idx in range(CHG_Mean_585.shape[1]):
        SR_LFO_SSP126 = instance.class_cal_lpo2( 'STD_only',  CHG_Mean_126[:,idx],  17, 1)
        SR_LFO_SSP245 = instance.class_cal_lpo2( 'STD_only',  CHG_Mean_245[:,idx],  17, 1)
        SR_LFO_SSP370 = instance.class_cal_lpo2( 'STD_only',  CHG_Mean_370[:,idx],  16, 1)
        SR_LFO_SSP585 = instance.class_cal_lpo2( 'STD_only',  CHG_Mean_585[:,idx],  17, 1)
        SRstd_SSP126_STDLFO.append(SR_LFO_SSP126)
        SRstd_SSP245_STDLFO.append(SR_LFO_SSP245)
        SRstd_SSP370_STDLFO.append(SR_LFO_SSP370)
        SRstd_SSP585_STDLFO.append(SR_LFO_SSP585)
    with open('dict_test_sub11.pickle', 'rb') as handle:
        dict126 = pickle.load(handle)
    with open('dict_test_sub22.pickle', 'rb') as handle:
        dict245 = pickle.load(handle)
    with open('dict_test_sub33.pickle', 'rb') as handle:
        dict370 = pickle.load(handle)
    with open('dict_test_sub44.pickle', 'rb') as handle:
        dict585 = pickle.load(handle)
    SRstd_SSP126_LFO = dict126['SRstd_SSP126_LFO']
    SRstd_SSP245_LFO = dict245['SRstd_SSP245_LFO']
    SRstd_SSP370_LFO = dict370['SRstd_SSP370_LFO']
    SRstd_SSP585_LFO = dict585['SRstd_SSP585_LFO']
    plt.boxplot(SRstd_SSP126_STDLFO, positions=[0.1], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='green'))
    plt.boxplot(SRstd_SSP245_STDLFO, positions=[0.2], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='orange'))
    plt.boxplot(SRstd_SSP370_STDLFO, positions=[0.3], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='brown'))
    plt.boxplot(SRstd_SSP585_STDLFO, positions=[0.4], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='red'))
    plt.boxplot(SRstd_SSP126_LFO, positions=[0.7], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='green'))
    plt.boxplot(SRstd_SSP245_LFO, positions=[0.8], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='orange'))
    plt.boxplot(SRstd_SSP370_LFO, positions=[0.9], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='brown'))
    plt.boxplot(SRstd_SSP585_LFO, positions=[1.0], widths=0.08, flierprops=dict(marker='o', markersize=4), medianprops=dict(color='red'))
    plt.axis('square')
    plt.xlim(0, 1.1)
    plt.ylim(0, 1.0)
    plt.show()
    plt.clf()