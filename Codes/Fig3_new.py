import cdutil, pickle
import numpy                                                                   as np
import scipy.stats                                                             as stats
import matplotlib.pyplot                                                       as plt
import matplotlib.patches                                                      as patches
from Function_regressions                                                      import get_regression_prediction as GRP

def fig_Tpredict(instance):
    vORG      = instance.vORG
    HISm_mean = instance.HISm_mean
    HISm_spat = instance.HISm_spat
    EOFreturn    = instance.class_cal_eofs(vORG, HISm_mean, HISm_spat, idx=[-1], REA_idx=True)
    CHG_Mean_126 = instance.CHG_Mean_126
    CHG_Mean_245 = instance.CHG_Mean_245
    CHG_Mean_370 = instance.CHG_Mean_370
    CHG_Mean_585 = instance.CHG_Mean_585
    PreMOD   = np.c_[EOFreturn['std_HISm'  ],   EOFreturn['std_EOFsOnHISm'][:,1:-1] ]
    PreREA1  = np.r_[EOFreturn['std_era20c'],   EOFreturn['std_EOFs_era20c'][1:-1]  ]
    PreREA2  = np.r_[EOFreturn['std_20crv3'],   EOFreturn['std_EOFs_20crv3'][1:-1]  ]
    with open('dictSRLOO.pickle', 'rb') as handle:
        dict1 = pickle.load(handle)
    SRstd_SSP126_EOF = np.array(dict1['SRstd_SSP126_EOF'])
    SRstd_SSP245_EOF = np.array(dict1['SRstd_SSP245_EOF'])
    SRstd_SSP370_EOF = np.array(dict1['SRstd_SSP370_EOF'])
    SRstd_SSP585_EOF = np.array(dict1['SRstd_SSP585_EOF'])
    def cal(data, SR, Del, PreMOD, PreREA1, PreREA2):
        if Del != -1: PreMOD = np.delete(PreMOD, 15, axis=0)
        RawArray, RawStdArray = [], []
        PreArra1, PreStdArra1 = [], []
        PreArra2, PreStdArra2 = [], []
        for idx in range(int(data.shape[1])):
            Raw_spread  = data[:,idx]
            Pre_Tchang1 = GRP(PreMOD, Raw_spread, PreREA1, add_const=1).predicted_mean
            Pre_Tchang2 = GRP(PreMOD, Raw_spread, PreREA2, add_const=1).predicted_mean
            Raw_ensmea  = np.mean(Raw_spread)
            Raw_std     = np.std(Raw_spread) * 2
            SR_scaler   = SR[idx]
            REA_std     = SR_scaler * Raw_std
            RawArray.append(Raw_ensmea)
            RawStdArray.append(Raw_std)
            PreArra1.append(float(Pre_Tchang1)); PreStdArra1.append(REA_std)
            PreArra2.append(float(Pre_Tchang2)); PreStdArra2.append(REA_std)
        return np.array(RawArray), np.array(RawStdArray), np.array(PreArra1), np.array(PreStdArra1), np.array(PreArra2), np.array(PreStdArra2)
    Raw126, RawStd126, Pre126_1, PreStd126_1, Pre126_2, PreStd126_2 = cal(CHG_Mean_126, SRstd_SSP126_EOF, -1, PreMOD, PreREA1, PreREA2)
    Raw245, RawStd245, Pre245_1, PreStd245_1, Pre245_2, PreStd245_2 = cal(CHG_Mean_245, SRstd_SSP245_EOF, -1, PreMOD, PreREA1, PreREA2)
    Raw370, RawStd370, Pre370_1, PreStd370_1, Pre370_2, PreStd370_2 = cal(CHG_Mean_370, SRstd_SSP370_EOF, 15, PreMOD, PreREA1, PreREA2)
    Raw585, RawStd585, Pre585_1, PreStd585_1, Pre585_2, PreStd585_2 = cal(CHG_Mean_585, SRstd_SSP585_EOF, -1, PreMOD, PreREA1, PreREA2)
    
    def plot(Var1, Var1Std, Var2, Var2Std, Var3, Var3Std, Y):
        ax1=plt.subplot(111)
        ax1.plot(np.arange(65)+2025, np.zeros(65)+2, color='black', linestyle='--')
        ax1.plot(np.arange(65)+2025, Var1, color='firebrick')
        ax1.fill_between(np.arange(65)+2025, Var1-Var1Std, Var1+Var1Std, facecolor='firebrick', alpha=0.3)
        ax1.plot(np.arange(65)+2025, Var2, color='green', linestyle='--')
        ax1.fill_between(np.arange(65)+2025, Var2-Var2Std, Var2+Var2Std, facecolor='green', alpha=0.3)
        ax1.plot(np.arange(65)+2025, Var3, color='royalblue', linestyle='--')
        ax1.fill_between(np.arange(65)+2025, Var3-Var3Std, Var3+Var3Std, facecolor='royalblue', alpha=0.3)
        ax1.set_xlim(2025, 2090)
        ax1.set_ylim(0, Y)
        plt.show()
        plt.clf()
    plot(Raw126, RawStd126, Pre126_1, PreStd126_1, Pre126_2, PreStd126_2, 3)
    plot(Raw245, RawStd245, Pre245_1, PreStd245_1, Pre245_2, PreStd245_2, 5)
    plot(Raw370, RawStd370, Pre370_1, PreStd370_1, Pre370_2, PreStd370_2, 5.5)
    plot(Raw585, RawStd585, Pre585_1, PreStd585_1, Pre585_2, PreStd585_2, 7) 
    
def fig_ECS_prediction(instance_110):
    SR_EOFloo = 0.4560970172201759
    vORG_110      = instance_110.vORG
    HISm_mean_110 = instance_110.HISm_mean
    HISm_spat_110 = instance_110.HISm_spat
    EOFreturn1    = instance_110.class_cal_eofs(vORG_110, HISm_mean_110, HISm_spat_110, idx=[-1], REA_idx=True)
    ECS_tests  = instance_110.ECS_CMIP6
    predictor1    = np.c_[EOFreturn1['std_HISm'], EOFreturn1['std_EOFsOnHISm'][:,1:-1] ]
    input_predictand_reanalysis1  = np.r_[EOFreturn1['std_era20c'],   EOFreturn1['std_EOFs_era20c'][1:-1]  ]
    input_predictand_reanalysis2  = np.r_[EOFreturn1['std_20crv3'],   EOFreturn1['std_EOFs_20crv3'][1:-1]  ]
    PcenREA1_predict = GRP(predictor1, ECS_tests, input_predictand_reanalysis1, add_const=1).predicted_mean
    PcenREA2_predict = GRP(predictor1, ECS_tests, input_predictand_reanalysis2, add_const=1).predicted_mean
    mea_ECS_tests = np.mean(ECS_tests)
    std_ECS_tests = np.std(ECS_tests)
    std_ECS_reana = std_ECS_tests * SR_EOFloo
    def plot_box(ax, pos, means, std1, std2):
        ax.plot(np.r_[means,means], np.r_[pos-0.2, pos+0.2], color='black', linewidth=1)
        ax.add_patch( plt.Rectangle((means-std1, pos-0.2), std1*2, 0.4,   color='g', ec='none', lw=0.3, alpha=0.5) )
        ax.plot(np.r_[means-std2, means-std1], np.r_[pos,pos], color='royalblue', linestyle='--', linewidth=1)
        ax.plot(np.r_[means+std1, means+std2], np.r_[pos,pos], color='royalblue', linestyle='--', linewidth=1)
        ax.plot(np.r_[means-std2, means-std2], np.r_[pos-0.1, pos+0.1], color='black', linewidth=1)
        ax.plot(np.r_[means+std2, means+std2], np.r_[pos-0.1, pos+0.1], color='black', linewidth=1)
    tvalue95 = stats.t.ppf(1-0.05/2, 17-2)
    tvalue50 = stats.t.ppf(1-0.50/2, 17-2)
    # std_ECS_95mod = std_ECS_tests * tvalue95
    # std_ECS_50mod = std_ECS_tests * tvalue50
    std_ECS_95mod = std_ECS_tests * 2
    std_ECS_50mod = std_ECS_tests * 1
    std_ECS_95rea = std_ECS_95mod * SR_EOFloo
    std_ECS_50rea = std_ECS_50mod * SR_EOFloo
    ax=plt.subplot(221)
    plot_box(ax, 3, PcenREA2_predict, std_ECS_50rea, std_ECS_95rea)
    plot_box(ax, 2, PcenREA1_predict, std_ECS_50rea, std_ECS_95rea)
    plot_box(ax, 1, mea_ECS_tests, std_ECS_50mod, std_ECS_95mod)
    plt.xlim(0, 8)
    plt.ylim(0.5, 3.5)
    plt.show()
    plt.clf()