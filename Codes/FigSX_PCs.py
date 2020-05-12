import numpy as np
import matplotlib.pyplot as plt
from Function_regressions import get_regression_ModelYearEofs
from SUB_Class_CMIP6      import CMIP6_models

def plot_PCs(instance, model_name):
    print (model_name)
    EOF_to_check = 3
    num_eof   = instance.num_eof
    HISm_spat = instance.HISm_spat
    ECS_CMIP6 = instance.ECS_CMIP6
    EOFreturn = instance.class_cal_eofs(instance.vORG, instance.HISm_mean, instance.HISm_spat, REA_idx=True)
    num_eof   = EOFreturn['num_eof']
    EOFs_spat = EOFreturn['EOFs_spat']
    mea_EOFsOnHISm = EOFreturn['mea_EOFsOnHISm']
    std_EOFsOnHISm = EOFreturn['std_EOFsOnHISm']
    eofv = std_EOFsOnHISm[:,EOF_to_check]
    eofm = mea_EOFsOnHISm[:,EOF_to_check]
    rank = np.argsort(eofv)
    rank_ECS = np.argsort(ECS_CMIP6)
    for i in range(ECS_CMIP6.shape[0]):
        print (model_name[rank[i]], ' ',  ECS_CMIP6[rank[i]], ' ',  std_EOFsOnHISm[rank[i],EOF_to_check], ' ',  mea_EOFsOnHISm[rank[i],EOF_to_check])    
    aaa = get_regression_ModelYearEofs(EOFs_spat, HISm_spat, num_eof,  REA=0)
    stdEOFmax = np.argmax(std_EOFsOnHISm[:,EOF_to_check])
    stdEOFmin = np.argmin(std_EOFsOnHISm[:,EOF_to_check])
    for ii in range(17):
        i = rank[ii]
        aaa_cent = aaa[i,:,EOF_to_check]-np.mean(aaa[i,:,EOF_to_check])
        aaa_detr = np.convolve(aaa_cent, np.ones(11)/11, mode='valid')
        colors = np.array(['royalblue']*len(aaa_cent))
        colors[aaa_cent>=0] = 'orangered'
        plt.plot(np.arange(110)+1901, np.zeros(110), color='black', linewidth=1)
        plt.bar(np.arange(110)+1901, aaa_cent, width=1, color=colors)
        plt.plot(np.arange(100)+1906, aaa_detr, color='black')
        plt.xlim(1901,2010)
        plt.ylim(-0.8,0.8)
        plt.show()
        plt.clf()
    def plot_x(x, idx, ty, name):
        xx_cent = x[:,idx]-np.mean(x[:,idx])
        xx_detr = np.convolve(xx_cent, np.ones(11)/11, mode='valid')
        colors = np.array(['royalblue']*len(xx_cent))
        colors[xx_cent>=0] = 'orangered'
        plt.plot(np.arange(110)+1901, np.zeros(110), color='black', linewidth=1)
        plt.bar(np.arange(ty)+1901+(110-ty), xx_cent, width=1, color=colors)
        plt.plot(np.arange(ty-10)+1906+(110-ty), xx_detr, color='black')
        plt.xlim(1901,2010)
        plt.ylim(-0.8,0.8)
        plt.show()
        plt.clf()
    HISp_spat_era20c   = np.array(EOFreturn['HISp_spat_era20c'])
    HISp_spat_20crv3   = np.array(EOFreturn['HISp_spat_20crv3'])
    a = get_regression_ModelYearEofs(EOFs_spat, HISp_spat_era20c, num_eof,   REA=1)
    b = get_regression_ModelYearEofs(EOFs_spat, HISp_spat_20crv3, num_eof,   REA=1)
    plot_x(a, EOF_to_check, 110, 'era20c')
    plot_x(b, EOF_to_check, 110, '20crv3')
    print (np.std(a, axis=0))
    print (np.mean(a, axis=0))