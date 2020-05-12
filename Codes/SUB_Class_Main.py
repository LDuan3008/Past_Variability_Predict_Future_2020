import numpy                                                                   as np
import MV2                                                                     as MV
import scipy.stats                                                             as stats
import statsmodels.api                                                         as sm
from SUB_Class_CMIP6                                                           import set_class_instance; set_class_instance()
from Function_GetPredictors                                                    import get_vORG
from Function_GetPredictors                                                    import get_EOFs_predictors
from Function_GetPredictands                                                   import get_predictand
from Function_regressions                                                      import get_regression_ModelYearEofs
from Function_regressions                                                      import get_regression_prediction
from sklearn.model_selection                                                   import LeaveOneOut
from sklearn.model_selection                                                   import LeavePOut
import random

class Results_cluster:
    instances = []
    def __init__(self, Xinput, num_eof, length1, length2, comb, LatLen):
        self.__class__.instances.append(self)
        
        if Xinput[4:7] == 'REA':
            flag_mask_MOD, WgtSrc = False, 'reanalysis'
            if Xinput[:3] == 'HIS': varMEAN, sources, selects = 'tEquArea'+LatLen, 'HIS_v', int(Xinput[-1])
            if Xinput[:3] == 'REA': varMEAN, sources, selects = 'tEquArea'+LatLen, 'REA_v', int(Xinput[-1])
        if Xinput[4:7] == 'OBS':
            flag_mask_MOD, WgtSrc = True, 'observation'
            if int(Xinput[-1]) == 1: 
                if Xinput[:3] == 'HIS': varMEAN, sources, selects = 'tHadCRUT', 'HIS_v', 1
                if Xinput[:3] == 'OBS': varMEAN, sources, selects = 'tHadCRUT', 'OBS_v', 1
            if int(Xinput[-1]) == 2: 
                if Xinput[:3] == 'HIS': varMEAN, sources, selects = 'tBerkEAR', 'HIS_v', 2
                if Xinput[:3] == 'OBS': varMEAN, sources, selects = 'tBerkEAR', 'OBS_v', 2
        
        self.flag_mask_MOD = flag_mask_MOD
        self.WgtSrc        = WgtSrc
        self.varMEAN       = varMEAN
        self.sources       = sources
        self.selects       = selects
        self.num_eof       = num_eof
        self.length1       = length1
        self.length2       = length2
        self.comb          = comb
        self.LatLen        = LatLen
        
        print ()
        print ('#--- Control parameters are listed below ---#')
        print ('flag_mask_MOD = ', flag_mask_MOD)
        print ('WgtSrc  = ', WgtSrc)
        print ('varMEAN = ', varMEAN)
        print ('sources = ', sources)
        print ('selects = ', selects)
        print ('#--- Control parameters end here ---#')
        print ()
        
        ######################### Normal calculation as before #########################
        print ('#--- Start getting all variables ---#')
        vORG                            = get_vORG(varMEAN, sources, length1, selects)
        HISm_both, HISm_spat, HISm_mean = get_predictand('historical', varMEAN, length2, selects, flag_mask_MOD)
        mea_HISm                        = np.mean( HISm_mean, axis=1) 
        std_HISm                        = np.std(  HISm_mean, axis=1)
        [CHG_Both_126, CHG_Both_245, CHG_Both_370, CHG_Both_585,
         CHG_Mean_126, CHG_Mean_245, CHG_Mean_370, CHG_Mean_585] = get_predictand('time_series', varMEAN, 'not used', selects, flag_mask_MOD)
        ECS_CMIP6 = np.array([3.02, 2.29, 5.64, 5.15, 4.68, 4.90, 4.79, 4.10, 4.33, 2.80, 3.89, 4.56, 2.66, 2.60, 3.13, 4.77, 5.36])
        
        self.vORG            = vORG
        self.HISm_both       = HISm_both
        self.HISm_spat       = HISm_spat
        self.HISm_mean       = HISm_mean
        self.mea_HISm        = mea_HISm
        self.std_HISm        = std_HISm
        
        self.CHG_Both_126    = CHG_Both_126
        self.CHG_Both_245    = CHG_Both_245
        self.CHG_Both_370    = CHG_Both_370
        self.CHG_Both_585    = CHG_Both_585
        self.CHG_Mean_126    = CHG_Mean_126
        self.CHG_Mean_245    = CHG_Mean_245
        self.CHG_Mean_370    = CHG_Mean_370
        self.CHG_Mean_585    = CHG_Mean_585
        self.ECS_CMIP6       = ECS_CMIP6
        
    def class_cal_eofs(self, vORG, HISm_mean, HISm_spat, idx=[-1], REA_idx=False):
        sources              = self.sources
        num_eof              = self.num_eof
        flag_mask_MOD        = self.flag_mask_MOD
        selects              = self.selects
        lat, lon             = vORG.getAxis(2), vORG.getAxis(3)
        if len(idx) != 1 or idx != -1: print('delete the following: ',idx); vORG = np.delete(vORG, idx, axis=0)
        vORG = MV.array(vORG); vORG.setAxis(2, lat); vORG.setAxis(3, lon)
        EOFs_2D, EOFs_spat   = get_EOFs_predictors(vORG, sources, num_eof, flag_mask_MOD, selects)
        mea_HISm             = np.mean( HISm_mean, axis=1) 
        std_HISm             = np.std(  HISm_mean, axis=1)
        mea_EOFsOnHISm       = np.mean( get_regression_ModelYearEofs(EOFs_spat, HISm_spat, num_eof,  REA=0), axis=1)
        std_EOFsOnHISm       = np.std(  get_regression_ModelYearEofs(EOFs_spat, HISm_spat, num_eof,  REA=0), axis=1)
        
        dict_return = {}
        dict_return['num_eof']        = num_eof
        dict_return['EOFs_2D']        = EOFs_2D
        dict_return['EOFs_spat']      = EOFs_spat
        dict_return['mea_HISm']       = mea_HISm
        dict_return['std_HISm']       = std_HISm
        dict_return['mea_EOFsOnHISm'] = mea_EOFsOnHISm
        dict_return['std_EOFsOnHISm'] = std_EOFsOnHISm
        if REA_idx == True:
            WgtSrc, varMEAN, length2 = self.WgtSrc, self.varMEAN, self.length2
            HISp_both_era20c, HISp_spat_era20c, HISp_mean_era20c = get_predictand(WgtSrc, varMEAN, length2, 1, flag_mask_MOD)
            HISp_both_20crv3, HISp_spat_20crv3, HISp_mean_20crv3 = get_predictand(WgtSrc, varMEAN, length2, 2, flag_mask_MOD)
            dict_return['HISp_spat_era20c'],   dict_return['HISp_mean_era20c']  = HISp_spat_era20c,   HISp_mean_era20c
            dict_return['HISp_spat_20crv3'],   dict_return['HISp_mean_20crv3']  = HISp_spat_20crv3,   HISp_mean_20crv3
            dict_return['std_era20c']        = np.std(HISp_mean_era20c)
            dict_return['std_20crv3']        = np.std(HISp_mean_20crv3)
            dict_return['std_EOFs_era20c']   = np.std(get_regression_ModelYearEofs(EOFs_spat, HISp_spat_era20c,   num_eof,  REA=1), axis=0)
            dict_return['std_EOFs_20crv3']   = np.std(get_regression_ModelYearEofs(EOFs_spat, HISp_spat_20crv3,   num_eof,  REA=1), axis=0)
        return dict_return
    
    def class_cal_loo(self, X_idx, Y, tot, add_const):
        loo                    = LeaveOneOut()
        test_Y, stds_Y, real_Y = [], [], []
        vORG                   = self.vORG
        HISm_mean              = self.HISm_mean
        HISm_spat              = self.HISm_spat
        lat, lon               = vORG.getAxis(2), vORG.getAxis(3)
        if tot == 16:
            # Remove NESM3
            vORG      = np.delete(vORG,      15, axis=0)
            vORG      = MV.array(vORG); vORG.setAxis(2, lat); vORG.setAxis(3, lon)
            HISm_mean = np.delete(HISm_mean, 15, axis=0)
            HISm_spat = np.delete(HISm_spat, 15, axis=0)
        for train_index, test_index in loo.split(np.arange(tot)):
            num = train_index.shape[0]
            if X_idx == 'STD_only': X = np.std(HISm_mean, axis=1)
            if X_idx == 'STD_EOFs':
                EOFreturn = self.class_cal_eofs(vORG, HISm_mean, HISm_spat, test_index)
                std_HISm        = EOFreturn['std_HISm']
                std_EOFsOnHISm  = EOFreturn['std_EOFsOnHISm']
                X               = np.c_[std_HISm, std_EOFsOnHISm[:, 1:-1]]
            train_X, train_Y    = X[train_index], Y[train_index]
            tests_X, tests_Y    = X[test_index],  Y[test_index]
            if add_const == 0: train_X, tests_X = train_X, tests_X
            if add_const == 1: train_X, tests_X = np.c_[np.ones(num), train_X], np.c_[1, tests_X]
            central_regressions = sm.OLS(train_Y, train_X).fit()
            central_predictions = central_regressions.get_prediction(tests_X)
            predicted_val       = central_predictions.predicted_mean
            predicted_std       = central_predictions.se_obs
            test_Y.append(float(predicted_val))
            stds_Y.append(float(predicted_std))
            real_Y.append(float(tests_Y))
        test_Y2, real_Y2 = np.array(test_Y), np.array(real_Y)
        mean_Y           = np.mean( real_Y)
        mse_REA          = np.sum(  (real_Y2 - mean_Y )**2  ) / real_Y2.shape[0]
        mse_TES          = np.sum(  (real_Y2 - test_Y2)**2  ) / test_Y2.shape[0]
        SR               = mse_TES / mse_REA
        R2               = stats.pearsonr(real_Y2, test_Y2)[0]**2        
        return SR, R2, test_Y2, stds_Y

    def class_cal_lpo2(self, X_idx, Y, tot, add_const):
        vORG                   = self.vORG
        HISm_mean              = self.HISm_mean
        HISm_spat              = self.HISm_spat
        lat, lon               = vORG.getAxis(2), vORG.getAxis(3)
        total_index_lit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        if tot == 16:
            vORG      = np.delete(vORG,      15, axis=0)
            vORG      = MV.array(vORG)
            vORG.setAxis(2, lat)
            vORG.setAxis(3, lon)
            HISm_mean = np.delete(HISm_mean, 15, axis=0)
            HISm_spat = np.delete(HISm_spat, 15, axis=0)
            total_index_lit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        SR_array = []
        for idx in range(1000):
            get_test  = random.sample(total_index_lit, 4)
            get_train = [ elem for elem in total_index_lit if elem not in get_test]
            test_index  = np.array(get_test)
            train_index = np.array(get_train)
            num1 = train_index.shape[0]
            num2 = test_index.shape[0]
            if X_idx == 'STD_only': X = np.std(HISm_mean, axis=1)
            if X_idx == 'STD_EOFs':
                EOFreturn = self.class_cal_eofs(vORG, HISm_mean, HISm_spat, test_index)
                std_HISm        = EOFreturn['std_HISm']
                std_EOFsOnHISm  = EOFreturn['std_EOFsOnHISm']
                X               = np.c_[std_HISm, std_EOFsOnHISm[:, 1:-1]]
            train_X, train_Y    = X[train_index], Y[train_index]
            tests_X, tests_Y    = X[test_index],  Y[test_index]
            if add_const == 0: train_X, tests_X = train_X, tests_X
            if add_const == 1: train_X, tests_X = np.c_[np.ones(num1), train_X], np.c_[np.ones(num2), tests_X]
            regressions   = sm.OLS(train_Y, train_X).fit()
            predicted_val = []
            for idx_test in range(test_index.shape[0]):
                tmp_predictand = regressions.get_prediction(tests_X[idx_test]).predicted_mean
                predicted_val.append(float(tmp_predictand))
            real_Y2 = np.array(Y)
            test_Y2 = np.array(predicted_val)
            mean_Y  = np.mean(real_Y2)
            real_Y3 = np.array(tests_Y)
            mse2    = np.sum( ( real_Y2 -  mean_Y)**2 ) / real_Y2.shape[0]
            mse     = np.sum( ( real_Y3 - test_Y2)**2 ) / test_Y2.shape[0]
            SR      = mse/mse2
            SR_array.append(SR)
        SR_means = np.mean(np.array(SR_array))
        return SR_means