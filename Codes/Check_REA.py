import cdms2 as cdms
import MV2 as MV
import cdutil
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import genutil.statistics as stat

# Compare with observations
def GetData(idx):
    if idx == 1: fopen=cdms.open('tas_ECMWFear20c_1901_2010.nc'); DATAsp = fopen('ECMWFear20c_EquArea')[79:]
    if idx == 2: fopen=cdms.open('tas_NOAA20CRv3_1901_2010.nc');  DATAsp = fopen('NOAA20CRv3_EquArea') [79:]
    if idx == 3: fopen=cdms.open('tas_NCEPpNCAR_1948_2010.nc');   DATAsp = fopen('NCEPpNCAR_EquArea')[32:]
    if idx == 4: fopen=cdms.open('tas_JRA55_1958_2013.nc');       DATAsp = fopen('JRA55_EquArea')[22:-3]
    if idx == 5: fopen=cdms.open('tp_CFSR_detrended.nc');         DATAsp = fopen('tas')[:-4]
    if idx == 6: fopen=cdms.open('tp_ERA5_detrended.nc');         DATAsp = fopen('tas')[:-4]
    if idx == 7: fopen=cdms.open('tp_MERRA2_detrended.nc');       DATAsp = fopen('tas')[:-4]
    fopen.close()
    
    DATAgm = cdutil.averager(DATAsp,axis='yx')
    DATAgmCent = np.array(DATAgm - cdutil.averager(DATAgm, axis=0, weight='equal'))
    return DATAsp, np.array(DATAgm), np.array(DATAgmCent)

import pickle
import skill_metrics as sm
with open('savetwo.pickle', 'rb') as handle:
    [HISm_mean, HISm_spat] = pickle.load(handle)
EMgm = np.mean(HISm_mean[:,-31:], axis=0)
EMgmCent = EMgm - np.mean(EMgm)
EMsp = cdutil.averager(HISm_spat[:,79:], axis=0, weights='equal')

ERACsp, ERACgm, ERACgmCent = GetData(1)
NOAAsp, NOAAgm, NOAAgmCent = GetData(2)
NCEPsp, NCEPgm, NCEPgmCent = GetData(3)
JRA5sp, JRA5gm, JRA5gmCent = GetData(4)
CFSRsp, CFSRgm, CFSRgmCent = GetData(5)
ERA5sp, ERA5gm, ERA5gmCent = GetData(6)
MER2sp, MER2gm, MER2gmCent = GetData(7)

print ('ERA20C: ', np.std(ERACgm))
print ('20CRv3: ', np.std(NOAAgm))
print ('JRC55: ', np.std(JRA5gm))
print ('CFSR: ', np.std(CFSRgm))
print ('ERA5: ', np.std(ERA5gm))
print ('MERRA2: ', np.std(MER2gm))