import cdms2 as cdms
import cdutil
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import MV2 as MV

# Compare with observations
def get_data(flag):
    f1=cdms.open('tas_ERA_1901_2010.nc')
    f2=cdms.open('tas_NOAA_1836_2015.nc')
    f3=cdms.open('tas_observation.nc')
    if flag == 'EqualArea':
        ERA = f1('tas_ERA_EquArea')
        NOA = f2('tas_NOAAv3_EquArea')[65:-5]
        OBS = 0
    if flag == 'HadCRUT':
        ERA = f1('tas_ERA_HadCRUT')
        NOA = f2('tas_NOAAv3_HadCRUT')[65:-5]
        OBS = f3('tas_HadCRUT')[51:161]
    if flag == 'BerkEAR':
        ERA = f1('tas_ERA_BerkEAR')
        NOA = f2('tas_NOAAv3_BerkEAR')[65:-5]
        OBS = f3('tas_BerkEar')[51:161]
    f1.close()
    f2.close()
    f3.close()
    return ERA, NOA, OBS


# Full period
ERAsp, NOAsp, OBSsp = get_data('EqualArea')
YearLeng = 31
ERAgm = cdutil.averager(ERAsp,axis='yx')
NOAgm = cdutil.averager(NOAsp,axis='yx')
ERAgmCent = np.array(ERAgm - cdutil.averager(ERAgm, axis=0, weight='equal'))
NOAgmCent = np.array(NOAgm - cdutil.averager(NOAgm, axis=0, weight='equal'))
print (np.std(ERAgm[:-31]))
print (np.std(NOAgm[:-31]))
print (                   )
print (np.std(ERAgm[-31:]))
print (np.std(NOAgm[-31:]))
print (             )
print (np.std(ERAgm))
print (np.std(NOAgm))
print (             )
print (             )


# Other period
ERAsp, NOAsp, OBSsp = get_data('BerkEAR')
print (ERAsp.shape)
YearLeng = 110
OBSsp = OBSsp[-1*YearLeng:]
ERAsp = ERAsp[-1*YearLeng:]
NOAsp = NOAsp[-1*YearLeng:]
mask_org = OBSsp*0.+1
mask_org = MV.masked_not_equal(mask_org, 1)
mask_tot = np.sum(mask_org, axis=0)
mask_fin = MV.array(MV.masked_not_equal(mask_tot, mask_tot.max()) * 0. +1)
mask_fin.setAxis(0, mask_org.getAxis(1))
mask_fin.setAxis(1, mask_org.getAxis(2))
ERAsp = ERAsp * mask_fin
NOAsp = NOAsp * mask_fin
OBSsp = OBSsp * mask_fin
ERAgm = cdutil.averager(ERAsp,axis='yx')
NOAgm = cdutil.averager(NOAsp,axis='yx')
OBSgm = cdutil.averager(OBSsp + 273.15,axis='yx') 
ERAgmCent = np.array(ERAgm - cdutil.averager(ERAgm, axis=0, weight='equal'))
NOAgmCent = np.array(NOAgm - cdutil.averager(NOAgm, axis=0, weight='equal'))
OBSgmCent = np.array(OBSgm - cdutil.averager(OBSgm, axis=0, weight='equal'))        
print (             )
print (np.std(ERAgm[:-31]))
print (np.std(NOAgm[:-31]))
print (np.std(OBSgm[:-31]))
print (             )
print (np.std(ERAgm[-31:]))
print (np.std(NOAgm[-31:]))
print (np.std(OBSgm[-31:]))
print (             )
print (np.std(ERAgm))
print (np.std(NOAgm))
print (np.std(OBSgm))
print (             )
print (             )

ERAsp, NOAsp, OBSsp = get_data('HadCRUT')
print (ERAsp.shape)
YearLeng = 110
OBSsp = OBSsp[-1*YearLeng:]
ERAsp = ERAsp[-1*YearLeng:]
NOAsp = NOAsp[-1*YearLeng:]
mask_org = OBSsp*0.+1
mask_org = MV.masked_not_equal(mask_org, 1)
mask_tot = np.sum(mask_org, axis=0)
mask_fin = MV.array(MV.masked_not_equal(mask_tot, mask_tot.max()) * 0. +1)
mask_fin.setAxis(0, mask_org.getAxis(1))
mask_fin.setAxis(1, mask_org.getAxis(2))
ERAsp = ERAsp * mask_fin
NOAsp = NOAsp * mask_fin
OBSsp = OBSsp * mask_fin
ERAgm = cdutil.averager(ERAsp,axis='yx')
NOAgm = cdutil.averager(NOAsp,axis='yx')
OBSgm = cdutil.averager(OBSsp + 273.15,axis='yx') 
ERAgmCent = np.array(ERAgm - cdutil.averager(ERAgm, axis=0, weight='equal'))
NOAgmCent = np.array(NOAgm - cdutil.averager(NOAgm, axis=0, weight='equal'))
OBSgmCent = np.array(OBSgm - cdutil.averager(OBSgm, axis=0, weight='equal'))        
print (             )
print (np.std(ERAgm[:-31]))
print (np.std(NOAgm[:-31]))
print (np.std(OBSgm[:-31]))
print (             )
print (np.std(ERAgm[-31:]))
print (np.std(NOAgm[-31:]))
print (np.std(OBSgm[-31:]))
print (             )
print (np.std(ERAgm))
print (np.std(NOAgm))
print (np.std(OBSgm))
print (             )