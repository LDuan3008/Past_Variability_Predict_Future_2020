import cdms2 as cdms
import MV2 as MV
import cdutil
import matplotlib.pyplot as plt
import numpy as np
import genutil.statistics as stat
import skill_metrics as sm
from eofs.cdms         import Eof

# Compare with observations
def get_data(flag):
    fmask=cdms.open('mask_subregions.nc')
    f1=cdms.open('tas_ERA_1901_2010.nc')
    f2=cdms.open('tas_NOAA_1836_2015.nc')
    f3=cdms.open('tas_observation.nc')
    if flag == 'HadCRUT':
        mask = fmask('vHadCRUT_mask')
        ERA = f1('tas_ERA_HadCRUT') * mask
        NOA = f2('tas_NOAAv3_HadCRUT')[65:-5] * mask
        OBS = f3('tas_HadCRUT')[51:161] * mask
    if flag == 'BerkEAR':
        mask = fmask('vBerkEar_mask')
        ERA = f1('tas_ERA_BerkEAR') * mask
        NOA = f2('tas_NOAAv3_BerkEAR')[65:-5] * mask
        OBS = f3('tas_BerkEar')[51:161] * mask
    fmask.close()
    f1.close()
    f2.close()
    f3.close()
    return ERA, NOA, OBS

# Prepare data
ERAsp, NOAsp, OBSsp = get_data('HadCRUT') #'BerkEAR'; 'HadCRUT'
ERAgm = cdutil.averager(ERAsp,axis='yx')
NOAgm = cdutil.averager(NOAsp,axis='yx')
OBSgm = cdutil.averager(OBSsp + 273.15,axis='yx') 
ERAgmCent = np.array(ERAgm - cdutil.averager(ERAgm, axis=0, weight='equal'))
NOAgmCent = np.array(NOAgm - cdutil.averager(NOAgm, axis=0, weight='equal'))
OBSgmCent = np.array(OBSgm - cdutil.averager(OBSgm, axis=0, weight='equal'))
ERAsp = ERAsp - np.array(cdutil.averager(ERAsp, axis='yx'))[:, None, None]
NOAsp = NOAsp - np.array(cdutil.averager(NOAsp, axis='yx'))[:, None, None]
OBSsp = OBSsp - np.array(cdutil.averager(OBSsp, axis='yx'))[:, None, None]
ERAsp = ERAsp - cdutil.averager(ERAsp, axis=0, weights='equal')
NOAsp = NOAsp - cdutil.averager(NOAsp, axis=0, weights='equal')
OBSsp = OBSsp - cdutil.averager(OBSsp, axis=0, weights='equal')

# Test EOFs
def get_constant_term(eofs):
    Predictor_T = (eofs[0]*0+1).ravel()
    for i in range(int(eofs.shape[0])):
        Predictor_T = np.ma.vstack([Predictor_T, eofs[i].ravel()])
    Predictor = Predictor_T.T
    return Predictor
def set_time_axis(length):
    Time = cdms.createAxis(np.arange(length)+1)
    Time.id='time'
    return Time
def get_EOFs(var1, num=3, scaling=2):
    lat = var1.getAxis(1)
    lon = var1.getAxis(2)
    var = MV.array(var1-np.mean(var1,axis=0))
    var.setAxis(1, lat)
    var.setAxis(2, lon)
    solver = Eof(var, weights='area')
    eofs   = solver.eofs(neofs=num, eofscaling=scaling)
    pc     = solver.pcs(npcs=num, pcscaling=scaling)
    vari   = solver.varianceFraction(num)
    eigv   = solver.eigenvalues(num)
    return eofs, pc, vari, eigv
ERAsp.setAxis(0, set_time_axis(ERAsp.shape[0]))
NOAsp.setAxis(0, set_time_axis(NOAsp.shape[0]))
OBSsp.setAxis(0, set_time_axis(OBSsp.shape[0]))
eofs1, pc1, vari1, eigv1 = get_EOFs(ERAsp, num=3, scaling=0)
eofs2, pc2, vari2, eigv2 = get_EOFs(NOAsp, num=3, scaling=0)
eofs3, pc3, vari3, eigv3 = get_EOFs(OBSsp, num=3, scaling=0)
cor11 = np.abs(stat.correlation(eofs1[0], eofs3[0], axis='yx'))
cor21 = np.abs(stat.correlation(eofs2[0], eofs3[0], axis='yx'))
cor12 = np.abs(stat.correlation(eofs1[1], eofs3[1], axis='yx'))
cor22 = np.abs(stat.correlation(eofs2[1], eofs3[1], axis='yx'))
cor13 = np.abs(stat.correlation(eofs1[2], eofs3[2], axis='yx'))
cor23 = np.abs(stat.correlation(eofs2[2], eofs3[2], axis='yx'))
print (cor11, cor21)
print (cor12, cor22)
print (cor13, cor23)
print ()
print ((cor21 - cor11)/cor11*100)
print ((cor22 - cor12)/cor12*100)
print ((cor23 - cor13)/cor13*100)
plt.bar(np.r_[0, 4, 8], np.r_[cor11, cor12, cor13], width=1)
plt.bar(np.r_[1, 5, 9], np.r_[cor21, cor22, cor23], width=1)
plt.ylim(0, 1)
plt.show()
plt.clf()


# Test taylor diagrom here:
TSstd1, TSstd2 = [], []
TSrms1, TSrms2 = [], []
TScor1, TScor2 = [], []
flag = 1
for idx in range(OBSsp.shape[0]):
    aaa = ERAsp[idx]
    bbb = NOAsp[idx]
    ccc = OBSsp[idx]
    std0 = stat.std(ccc, axis='yx')
    std1 = stat.std(aaa, axis='yx') / std0
    std2 = stat.std(bbb, axis='yx') / std0
    cor1 = stat.correlation(aaa, ccc, axis='yx')
    cor2 = stat.correlation(bbb, ccc, axis='yx')
    rms1 = stat.rms(aaa, ccc, axis='yx', centered=0)
    rms2 = stat.rms(bbb, ccc, axis='yx', centered=0)
    TSstd1.append(std1)
    TSstd2.append(std2)
    TSrms1.append(rms1)
    TSrms2.append(rms2)
    TScor1.append(cor1)
    TScor2.append(cor2)
    if flag == 1:
        sm.taylor_diagram(np.array([1.0, np.mean(TSstd1)]),
                          np.array([0.0, np.mean(TSrms1)]),
                          np.array([1.0, np.mean(TScor1)]),
                          markerColor = 'firebrick',
                          colOBS = 'black', markerobs = 'x')
        flag += 1
    else:
        sm.taylor_diagram(np.array([1.0, np.mean(TSstd1)]),
                          np.array([0.0, np.mean(TSrms1)]),
                          np.array([1.0, np.mean(TScor1)]),
                          markerColor = 'firebrick',
                          colOBS = 'black', markerobs = 'x',
                          overlay = 'on')
    sm.taylor_diagram(np.array([1.0, np.mean(TSstd2)]),
                      np.array([0.0, np.mean(TSrms2)]),
                      np.array([1.0, np.mean(TScor2)]),
                      markerColor = 'royalblue',
                      colOBS = 'black', markerobs = 'x',
                      overlay = 'on')
plt.show()
plt.clf()