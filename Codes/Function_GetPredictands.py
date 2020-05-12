import cdms2 as cdms
import numpy as np, MV2 as MV
import cdutil
from SUB_Class_CMIP6 import CMIP6_models
from Share_variables import data_path

###############################################################################
def get_predictand(predictand_flag, varMEAN, length, REA, flag_mask_MOD):
    model_flg = 1
    if flag_mask_MOD == True:
        fmask=cdms.open(data_path+'mask_subregions.nc')
        if REA==1: vMask2 = fmask('vHadCRUT_mask')
        if REA==2: vMask2 = fmask('vBerkEar_mask')
        vMask_used = np.array(vMask2.ravel())
    else:
        vMask_used = 1
        vMask2 = 1
        
    if predictand_flag == 'reanalysis':
        if REA == 1: f1=cdms.open(data_path+'tas_ECMWFear20c_1901_2010.nc');  vused_org = f1('ECMWFear20c_EquArea')[(-1*length):];  f1.close()
        if REA == 2: f1=cdms.open(data_path+'tas_NOAA20CRv3_1901_2010.nc');   vused_org = f1('NOAA20CRv3_EquArea')[(-1*length):];   f1.close()
        vused_mea = np.array(cdutil.averager(vused_org, axis='yx'))
        vused_spa = vused_org - vused_mea[:, None, None]
        for subidx in range(vused_org.shape[0]):
            if subidx == 0:
                array_vorg  = [vused_org[subidx].ravel()]
                array_vspa  = [vused_spa[subidx].ravel()]
            else:
                array_vorg  = np.ma.concatenate([array_vorg, [vused_org[subidx].ravel()]])
                array_vspa  = np.ma.concatenate([array_vspa, [vused_spa[subidx].ravel()]])
        return array_vorg, array_vspa, vused_mea
    
    if predictand_flag == 'historical':
        for instance in CMIP6_models.instances:
            if 'historical' in instance.CaseList and 'ssp585' in instance.CaseList:
                fname_open = 'tp_'+instance.Name+'_historical_'+instance.VarLab[1][0]+'.nc'
                fopen = cdms.open(data_path + fname_open)
                vused = fopen(varMEAN)[int(-1*length-4):-4]
                fopen.close()
                vused_v_org = vused * vMask2
                vused_v_mea = np.array(cdutil.averager(vused_v_org, axis='yx'))
                vused_v_spa = vused_v_org - vused_v_mea[:, None, None]
                for subidx in range(vused_v_org.shape[0]):
                    if subidx == 0:
                        tmp_array_vorg = [vused_v_org[subidx].ravel()]
                        tmp_array_vspa = [vused_v_spa[subidx].ravel()]
                    else:
                        tmp_array_vorg = np.ma.concatenate([tmp_array_vorg, [vused_v_org[subidx].ravel()]])
                        tmp_array_vspa = np.ma.concatenate([tmp_array_vspa, [vused_v_spa[subidx].ravel()]])                        
                if model_flg == 1:
                    array_vorg = [tmp_array_vorg]
                    array_vspa = [tmp_array_vspa]
                    array_vmea = [vused_v_mea]
                    model_flg += 1
                else:
                    array_vorg = np.ma.concatenate([array_vorg, [tmp_array_vorg]])
                    array_vspa = np.ma.concatenate([array_vspa, [tmp_array_vspa]])
                    array_vmea = np.ma.concatenate([array_vmea, [vused_v_mea]])
        print ('-----------------get predictand done here -----------------')
        return array_vorg, array_vspa, array_vmea
    
    
    if predictand_flag == 'time_series':
        for instance in CMIP6_models.instances:
            if 'historical' in instance.CaseList and 'ssp585' in instance.CaseList:
                fname_his     = 'tp_'+instance.Name+'_historical_'+instance.VarLab[1][0]+'.nc'
                fopen_his     = cdms.open(data_path + fname_his)
                v_HIS         = fopen_his(varMEAN)[int(-1*110-4):-4]
                v_HIS_full    = fopen_his(varMEAN)
                v_HIS_Mean    = cdutil.averager(v_HIS,axis='yx')
                v_HIS_MeanYr  = cdutil.averager(v_HIS_Mean,axis=0,weights='equal')
                fopen_his.close()
                def get_ssp(fname_ssp):
                    fopen_ssp     = cdms.open(data_path + fname_ssp)
                    v_SSP         = fopen_ssp(varMEAN)
                    v_SSP_Mean    = cdutil.averager(v_SSP,axis='yx') - v_HIS_MeanYr
                    v_SSP_DeTr    = np.convolve(v_SSP_Mean, np.ones(21)/21, mode='valid')
                    fopen_ssp.close()
                    HIS_full_Mean = cdutil.averager(v_HIS_full,axis='yx') - v_HIS_MeanYr
                    SSP_full_Mean = cdutil.averager(v_SSP,axis='yx')      - v_HIS_MeanYr
                    COM_full_Mean = np.r_[HIS_full_Mean, SSP_full_Mean]
                    COM_full_DeTr = np.convolve(COM_full_Mean, np.ones(21)/21, mode='valid')
                    return COM_full_DeTr, v_SSP_DeTr
                v126Full, v126SSP = get_ssp('tp_'+instance.Name+'_ssp126_'+instance.VarLab[1][0]+'.nc')
                v245Full, v245SSP = get_ssp('tp_'+instance.Name+'_ssp245_'+instance.VarLab[1][0]+'.nc')
                if instance.Name != 'NESM3': v370Full, v370SSP = get_ssp('tp_'+instance.Name+'_ssp370_'+instance.VarLab[1][0]+'.nc')
                v585Full, v585SSP = get_ssp('tp_'+instance.Name+'_ssp585_'+instance.VarLab[1][0]+'.nc')
                if model_flg == 1 and instance.Name != 'NESM3':
                    array126Full, array126SSP = [v126Full], [v126SSP]
                    array245Full, array245SSP = [v245Full], [v245SSP]
                    array370Full, array370SSP = [v370Full], [v370SSP]
                    array585Full, array585SSP = [v585Full], [v585SSP]
                    model_flg += 1
                else:
                    array126Full, array126SSP = np.ma.concatenate([array126Full, [v126Full]]), np.ma.concatenate([array126SSP, [v126SSP]])
                    array245Full, array245SSP = np.ma.concatenate([array245Full, [v245Full]]), np.ma.concatenate([array245SSP, [v245SSP]])
                    if instance.Name != 'NESM3': array370Full, array370SSP = np.ma.concatenate([array370Full, [v370Full]]), np.ma.concatenate([array370SSP, [v370SSP]])
                    array585Full, array585SSP = np.ma.concatenate([array585Full, [v585Full]]), np.ma.concatenate([array585SSP, [v585SSP]])
        print ('-----------------get predictand done here -----------------')
        return [array126Full, array245Full, array370Full, array585Full,
                array126SSP,  array245SSP,  array370SSP,  array585SSP ]