import cdutil, sys
import cdms2           as cdms
import MV2             as MV
import numpy           as np
from genutil           import statistics
from eofs.cdms         import Eof
from SUB_Class_CMIP6   import CMIP6_models
from Share_variables   import data_path, scaling_factor, EOFsSignAdjust

###############################################################################
###############################################################################
def set_time_axis(length):
    Time = cdms.createAxis(np.arange(length)+1)
    Time.id='time'
    return Time

def get_constant_term(eofs):
    Predictor_T = (eofs[0]*0+1).ravel()
    for i in range(int(eofs.shape[0])):
        Predictor_T = np.ma.vstack([Predictor_T, eofs[i].ravel()])
    Predictor = Predictor_T.T
    return Predictor

def get_EOFs(var1, num=5, scaling=0):
    lat = var1.getAxis(1)
    lon = var1.getAxis(2)
    var = MV.array(var1-np.mean(var1,axis=0))
    var.setAxis(1, lat)
    var.setAxis(2, lon)
    # solver = Eof(var, weights='area')
    solver = Eof(var)
    eofs   = solver.eofs(neofs=num, eofscaling=scaling)
    pc     = solver.pcs(npcs=num, pcscaling=scaling)
    vari   = solver.varianceFraction(num)
    eigv   = solver.eigenvalues(num)
    return eofs, pc, vari, eigv
    
###############################################################################
###############################################################################    
def get_eofs(v_HIS, num_eof, scaling_eof, flag_mask_MOD, selec):
    TotGriNum = v_HIS.shape[1] * v_HIS.shape[2]
    if flag_mask_MOD == True:
        fmask=cdms.open(data_path+'mask_subregions.nc')
        if selec==1: vMask = fmask('vHadCRUT_mask')
        if selec==2: vMask = fmask('vBerkEar_mask')
        fmask.close()
    else:
        vMask = 1
    v_rem_mean               = v_HIS - np.array(cdutil.averager(v_HIS, axis='yx'))[:, None, None]
    v_HIS_spat               = v_rem_mean - cdutil.averager(v_rem_mean, axis=0, weights='equal')
    eofs2, pc2, vari2, eigv2 = get_EOFs(v_HIS_spat, num=num_eof, scaling=scaling_eof)
    eofs2                    = eofs2 * np.sqrt(TotGriNum) * EOFsSignAdjust[:, None, None] # Normalized by RMS
    eofs2_MV                 = MV.array(eofs2); eofs2_MV.setAxis(1, v_HIS.getAxis(1)); eofs2_MV.setAxis(2, v_HIS.getAxis(2))
    predictor_OnlyPattern    = get_constant_term(eofs2)
    return_spat              = np.ma.filled(predictor_OnlyPattern, 0)
    return eofs2_MV, return_spat

def get_predictor1(data_path, predictor_source, varMEAN, length, selec):
    model_flg = 1
    if predictor_source == 'models_historical' or predictor_source == 'models_ssp':
        for instance in CMIP6_models.instances:
            if 'historical' in instance.CaseList and 'ssp585' in instance.CaseList:
                if predictor_source == 'models_historical': 
                    fopen = cdms.open(data_path + 'tp_'+instance.Name+'_historical_'+instance.VarLab[1][0]+'.nc')
                    vUsed = fopen(varMEAN)[int(-1*length-4):-4]
                if predictor_source == 'models_ssp':        
                    fopen = cdms.open(data_path + 'tp_'+instance.Name+'_ssp585_'+instance.VarLab[1][0]+'.nc')
                    vUsed = fopen(varMEAN)[int(-1*length):]
                fopen.close()
                vUsed_masked = vUsed - cdutil.averager(vUsed, axis=0, weights='equal')
                if model_flg == 1:
                    array_MEAN = [vUsed_masked]
                    lat,lon    = vUsed_masked.getAxis(1), vUsed_masked.getAxis(2)
                    model_flg += 1
                else:
                    array_MEAN = np.ma.concatenate([array_MEAN, [vUsed_masked]])
        return_ME = MV.array(array_MEAN)
        return_ME.setAxis(2, lat)
        return_ME.setAxis(3, lon)
        return return_ME

###############################################################################
###############################################################################
def get_vORG(varUsed, choice, length, selec):
    if choice == 'HIS_v':  vORG = get_predictor1(data_path, 'models_historical',   varUsed,  length,  selec) 
    if choice == 'SSP_v':  vORG = get_predictor1(data_path, 'models_ssp',          varUsed,  length,  selec)
    return vORG

###############################################################################
###############################################################################
def get_EOFs_predictors(vORG, choice, num_eof, flag_mask_MOD, selec):
    if choice == 'HIS_v' or choice == 'SSP_v':
        totnum = int(vORG.shape[0])
        for i in range(totnum):
            if i == 0:
                vORG_new = vORG[i]
            else:
                vORG_new = np.r_[vORG_new, vORG[i]]
        vORG_new = MV.array(vORG_new)
        vORG_new.setAxis(0, set_time_axis(vORG_new.shape[0]))
        vORG_new.setAxis(1, vORG.getAxis(2))
        vORG_new.setAxis(2, vORG.getAxis(3))
    else:
        vORG_new = vORG
    EOFs_2D, EOFs_spat = get_eofs(vORG_new, num_eof, scaling_factor, flag_mask_MOD, selec)
    return EOFs_2D, EOFs_spat