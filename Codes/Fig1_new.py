import numpy                                                                   as np
import matplotlib.pyplot                                                       as plt
import statsmodels.api                                                         as sm

def fig_EOFs(instance):
    EOFreturn = instance.class_cal_eofs(instance.vORG, instance.HISm_mean, instance.HISm_spat)
    num_eof   = EOFreturn['num_eof']
    eofs      = EOFreturn['EOFs_2D']
    axis1     = eofs.getAxis(1)
    axis2     = eofs.getAxis(2)
    lat_bnd   = axis1.getBounds(); lat = np.r_[lat_bnd[:,0], lat_bnd[-1,1]]
    lon_bnd   = axis2.getBounds(); lon = np.r_[lon_bnd[:,0], lon_bnd[-1,1]]
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import cartopy.crs       as ccrs
    import cartopy.feature   as cfeature
    from matplotlib.axes     import Axes
    from cartopy.mpl.geoaxes import GeoAxes
    GeoAxes._pcolormesh_patched = Axes.pcolormesh
    cmaps = plt.get_cmap('bwr', 30)
    for i in range(num_eof):
        ax = plt.axes(projection = ccrs.Mollweide(central_longitude=180.))
        ax.set_global()
        ax.add_feature(cfeature.COASTLINE)
        mp = ax.pcolor(lon, lat, eofs[i], cmap=cmaps, norm=mcolors.Normalize(vmin=-3,vmax=3), transform=ccrs.PlateCarree())
        plt.colorbar(mp, ax=ax, orientation='horizontal', shrink=0.8, extend='both')
        plt.show()
        plt.clf()
    
def fig_STDloadings(instance, Name):
    vORG      = instance.vORG
    HISm_mean = instance.HISm_mean
    HISm_spat = instance.HISm_spat
    EOFreturn    = instance.class_cal_eofs(vORG, HISm_mean, HISm_spat, idx=[-1], REA_idx=True)
    STDSTDloadingsMOD  = EOFreturn['std_HISm']
    STDSTDloadingsREA1 = EOFreturn['std_era20c']
    STDSTDloadingsREA2 = EOFreturn['std_20crv3']
    STDloadingsMOD  = EOFreturn['std_EOFsOnHISm']
    STDloadingsREA1 = EOFreturn['std_EOFs_era20c']
    STDloadingsREA2 = EOFreturn['std_EOFs_20crv3']
    STD0 = np.r_[STDSTDloadingsMOD,   STDSTDloadingsREA1, STDSTDloadingsREA2]
    STD1 = np.r_[STDloadingsMOD[:,1], STDloadingsREA1[1], STDloadingsREA2[1]]
    STD2 = np.r_[STDloadingsMOD[:,2], STDloadingsREA1[2], STDloadingsREA2[2]]
    STD3 = np.r_[STDloadingsMOD[:,3], STDloadingsREA1[3], STDloadingsREA2[3]]
    Name.append('ERA')
    Name.append('20C')
    def plotSTD(STD, j):
        num = STD.shape[0]
        sort = np.argsort(STD)[::-1]
        for i in range(num):
            print (Name[sort[i]])
        print ()
        plt.barh(np.arange(num), STD[sort[::-1]], height=0.8)
        plt.yticks(np.arange(num))
        plt.ylim(-1, 19)
        plt.xlim(0, 0.40)
        plt.savefig('STD'+str(j)+'.ps')
        plt.clf()
    plotSTD(STD0, 0)
    plotSTD(STD1, 1)
    plotSTD(STD2, 2)
    plotSTD(STD3, 3)