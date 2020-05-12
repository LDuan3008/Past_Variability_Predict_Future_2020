import numpy                                                                   as np
import matplotlib.pyplot                                                       as plt
import matplotlib.patches                                                      as patches
import statsmodels.api                                                         as sm
import pickle 

############
#### Panel 1 
############
def SRwithT():
    with open('dict_test_SRwithT.pickle', 'rb') as handle:
        dictSR = pickle.load(handle)
    SR_1array = np.array(dictSR['SR_1array'])
    SR_2array = np.array(dictSR['SR_2array'])
    SR_3array = np.array(dictSR['SR_3array'])
    plt.plot(np.arange(46)* 2 + 20, SR_1array, color='firebrick', linestyle='dotted')
    plt.plot(np.arange(46)* 2 + 20, SR_2array, color='firebrick', linestyle='dashed')
    plt.plot(np.arange(46)* 2 + 20, SR_3array, color='firebrick', linestyle='solid')
    # plt.yscale('log', basey=2)
    plt.xlim(20, 110)
    plt.ylim(0,  1.3)
    plt.show()
    plt.clf()