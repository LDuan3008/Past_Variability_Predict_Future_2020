import os, numpy as np
class CMIP6_models:
    total_num = 0
    instances = []
    file_path = './'
    def __init__(self, Name, Res, Grids, CaseList, VarLab):
        self.__class__.instances.append(self)
        self.Name = Name
        self.Res = Res  
        self.Grids = Grids  
        self.CaseList = CaseList
        self.VarLab = VarLab
        CMIP6_models.total_num +=1
        
    def get_nc_name(self, case_name, VarLab):
        self_nc_name = 'tp_' + self.Name + '_' + case_name + '_' + VarLab + '.nc'
        return self_nc_name
    
    def get_timestamp(self, case_name):
        if not (case_name in self.CaseList):
            print  (self.Name, 'does not have',case_name)
            return [ ]
        else:
            data_path = CMIP6_models.file_path + self.Name + '/' + case_name + '/'
            filelist  = os.listdir(data_path)
            timestamp = []
            for file in filelist:
                if file[:3] == 'tas':
                    timestamp.append(file[-16:])
            timestamp_unique = np.unique(timestamp)
            timestamp_unique.sort()
            return timestamp_unique
        
######################################################################################################
# note that NESM3 does not have SSP370 results
def set_class_instance():
    bcc_csm2_mr     = CMIP6_models( 'BCC-CSM2-MR',     [160, 320], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  )
    bcc_esm1        = CMIP6_models( 'BCC-ESM1',        [ 64, 128], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical'          ],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  )
    cams_csm1_0     = CMIP6_models( 'CAMS-CSM1-0',     [160, 320], 'gn',  [                             'historical', 'ssp585'],  [['no cases'], ['r1i1p1f1'                        ]]  )
    canesm5         = CMIP6_models( 'CanESM5',         [ 64, 128], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    cesm2           = CMIP6_models( 'CESM2',           [192, 288], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    cesm2_waccm     = CMIP6_models( 'CESM2-WACCM',     [192, 288], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    cnrm_cm6_1      = CMIP6_models( 'CNRM-CM6-1',      [128, 256], 'gr',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f2'], ['r1i1p1f2', 'r2i1p1f2', 'r3i1p1f2']]  ) 
    cnrm_esm2_1     = CMIP6_models( 'CNRM-ESM2-1',     [128, 256], 'gr',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f2'], ['r1i1p1f2', 'r2i1p1f2', 'r3i1p1f2']]  ) 
    e3sm_1_0        = CMIP6_models( 'E3SM-1-0',        [180, 360], 'gr',  ['piControl', 'abrupt-4xCO2', 'historical'          ],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    ec_earth3       = CMIP6_models( 'EC-Earth3',       [256, 512], 'gr',  ['piControl',                 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r3i1p1f1', 'r4i1p1f1']]  )
    ec_earth3_veg   = CMIP6_models( 'EC-Earth3-Veg',   [256, 512], 'gr',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    fgoals_g3       = CMIP6_models( 'FGOALS-g3',       [ 80, 180], 'gn',  ['piControl',                 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    gfdl_esm4       = CMIP6_models( 'GFDL-ESM4',       [180, 288], 'gr1', [                             'historical', 'ssp585'],  [['no cases'], ['r1i1p1f1'                        ]]  )
    giss_e2_1_g     = CMIP6_models( 'GISS-E2-1-G',     [ 90, 144], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical'          ],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    giss_e1_1_h     = CMIP6_models( 'GISS-E2-1-H',     [ 90, 144], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical'          ],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    hadgem3_gc31_ll = CMIP6_models( 'HadGEM3-GC31-LL', [144, 192], 'gn',  [             'abrupt-4xCO2', 'historical'          ],  [['r1i1p1f3'], ['r1i1p1f3', 'r2i1p1f3', 'r3i1p1f3']]  ) 
    ipsl_cm6a_lr    = CMIP6_models( 'IPSL-CM6A-LR',    [143, 144], 'gr',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    miroc_es2l      = CMIP6_models( 'MIROC-ES2L',      [ 64, 128], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f2'], ['r1i1p1f2', 'r2i1p1f2', 'r3i1p1f2']]  ) 
    miroc6          = CMIP6_models( 'MIROC6',          [128, 256], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    mri_esm2_0      = CMIP6_models( 'MRI-ESM2-0',      [160, 320], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    nesm3           = CMIP6_models( 'NESM3',           [ 96, 192], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    norcpm1         = CMIP6_models( 'NorCPM1',         [ 96, 144], 'gn',  ['piControl',                 'historical'          ],  [['r1i1p1f1'], ['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']]  ) 
    noresm2_lm      = CMIP6_models( 'NorESM2-LM',      [ 96, 144], 'gn',  ['piControl', 'abrupt-4xCO2'                        ],  [['r1i1p1f1'], ['no cases'                        ]]  ) 
    sam0_unicon     = CMIP6_models( 'SAM0-UNICON',     [192, 288], 'gn',  ['piControl', 'abrupt-4xCO2'                        ],  [['r1i1p1f1'], ['no cases'                        ]]  ) 
    ukesm1_0_ll     = CMIP6_models( 'UKESM1-0-LL',     [144, 192], 'gn',  ['piControl', 'abrupt-4xCO2', 'historical', 'ssp585'],  [['r1i1p1f2'], ['r1i1p1f2', 'r2i1p1f2', 'r3i1p1f2']]  )
    print (CMIP6_models.total_num, 'CMIP6_models instances has been generated: ', 
           bcc_csm2_mr.Name, bcc_esm1.Name, cams_csm1_0.Name, canesm5.Name, cesm2.Name, cesm2_waccm.Name, cnrm_cm6_1.Name,
           cnrm_esm2_1.Name, e3sm_1_0.Name, ec_earth3.Name, ec_earth3_veg.Name, fgoals_g3.Name, gfdl_esm4.Name, giss_e2_1_g.Name,
           giss_e1_1_h.Name, hadgem3_gc31_ll.Name, ipsl_cm6a_lr.Name, miroc_es2l.Name, miroc6.Name, mri_esm2_0.Name, nesm3.Name, 
           norcpm1.Name, noresm2_lm.Name, sam0_unicon.Name, ukesm1_0_ll.Name)