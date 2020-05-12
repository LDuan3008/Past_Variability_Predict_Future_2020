from SUB_Class_Main                                                            import Results_cluster
from SUB_Class_CMIP6                                                           import CMIP6_models
import numpy                                                                   as np

if __name__=='__main__':
    # FigSX SRwithT
    SR_1list, SR_2list, SR_3list = [], [], []
    for idx in range(46):
        length = idx * 2 + 20
        print ('#----------> ', length)
        HISSSP_3 = Results_cluster('HIS_REA_1', 3, 110, length, 'HISSSP', '')
        HISSSP_2 = Results_cluster('HIS_REA_1', 2, 110, length, 'HISSSP', '')    
        HISSSP_1 = Results_cluster('HIS_REA_1', 1, 110, length, 'HISSSP', '')
        SR_3, R2, test_array2, std_testay = HISSSP_3.class_cal_loo('STD_EOFs', HISSSP_3.CHG_Mean_585[:,-1], 17, 1)
        SR_2, R2, test_array2, std_testay = HISSSP_2.class_cal_loo('STD_EOFs', HISSSP_2.CHG_Mean_585[:,-1], 17, 1)
        SR_1, R2, test_array2, std_testay = HISSSP_1.class_cal_loo('STD_EOFs', HISSSP_1.CHG_Mean_585[:,-1], 17, 1)
        SR_3list.append(SR_3)
        SR_2list.append(SR_2)
        SR_1list.append(SR_1)
    SR_1array, SR_2array, SR_3array = np.array(SR_1list), np.array(SR_2list), np.array(SR_3list)
    
    dict_return = {}
    dict_return['SR_1array']    = SR_1array
    dict_return['SR_2array']    = SR_2array
    dict_return['SR_3array']    = SR_3array
    
    import pickle
    with open('dict_test_SRwithT.pickle', 'wb') as handle:
        pickle.dump(dict_return, handle, protocol=pickle.HIGHEST_PROTOCOL)