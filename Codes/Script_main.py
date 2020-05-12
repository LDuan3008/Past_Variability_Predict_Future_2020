from SUB_Class_Main                                                            import Results_cluster
from SUB_Class_CMIP6                                                           import CMIP6_models
# Plots from here
from Fig1_new                                                                  import fig_EOFs
from Fig1_new                                                                  import fig_STDloadings
from Fig2_new                                                                  import cal_MEMEX
from Fig2_new                                                                  import fig_LOOprediction
from Fig2_new                                                                  import fig_LOObox
from Fig3_new                                                                  import fig_Tpredict
from Fig3_new                                                                  import fig_ECS_prediction
# SOM
from FigSX_STDonly                                                             import fig_StdGMSATonly
from FigSX_LFO                                                                 import fig_cross_validation3
from FigSX_Contrib                                                             import fig_contributions
from FigSX_PCs                                                                 import plot_PCs
from FigSX_SRwithT                                                             import SRwithT
from FigSX_REA                                                                 import CheckREA
from FigSX_TOAflux                                                             import TOAswcs
if __name__=='__main__':
    model_name = []
    for instance2 in CMIP6_models.instances:
        if 'historical' in instance2.CaseList and 'ssp585' in instance2.CaseList:
            model_name.append(instance2.Name)    
    num_eof, length1, length2, comb = 3, 110, 110, 'HISSSP'
    HisRea3EOFs110Yr = Results_cluster('HIS_REA_1', num_eof, length1, length2, comb, '')        
    # Figure 1, done locally 
    fig_EOFs(HisRea3EOFs110Yr)
    fig_STDloadings(HisRea3EOFs110Yr, model_name)
    # Figure 2 Calculate on HPC first
    cal_MEMEX(HisRea3EOFs110Yr)
    fig_LOOprediction(HisRea3EOFs110Yr)
    fig_LOObox()
    # Figure 3, Use only one reanalysis
    fig_Tpredict(HisRea3EOFs110Yr)
    fig_ECS_prediction(HisRea3EOFs110Yr)
    # SOM
    fig_StdGMSATonly(HisRea3EOFs110Yr)
    fig_cross_validation3(HisRea3EOFs110Yr)
    fig_contributions(HisRea3EOFs110Yr)
    plot_PCs(HisRea3EOFs110Yr, model_name)
    SRwithT()
    CheckREA(HisRea3EOFs110Yr, model_name)
    TOAswcs(HisRea3EOFs110Yr, model_name)