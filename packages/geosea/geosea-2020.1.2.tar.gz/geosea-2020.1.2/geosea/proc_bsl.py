#-------------------------------------------------------------------------------
#       Complete processing
#-------------------------------------------------------------------------------

from .read import *
from .vert_bsl import *
from .hori_bsl import *

from .sw import *

def proc_bsl (SAL,phi,pathname=None,starttime=None, endtime=None,outlier_flag=None,writefile=True):
    """ Complete Baseline processing of GeoSEA Raw data.

    It needs:
    SAL ...    constant salinity value in PSU
    phi ...    Latitude for Leroy formular in XX.X
    pathname   Pathname of raw CSV Data files;

    It returns:
    bsl ... list of pandas.DataFrame with calculated Baselines

    """
    
    if pathname is None:
        pathname = ''
    
    ID,st_series,bsl_series = read(starttime=starttime, endtime=endtime,pathname=pathname,writefile=writefile)
    
    st_series_leroy = []
    result = []
    for i, id in enumerate(ID):
        st_series_leroy.append(sv_leroy(st_series[i],SAL,phi))
    
    bsl_horizonal = hori_bsl(ID,bsl_series,st_series_leroy,outlier_flag,writefile)
    
    bsl_vertical = vert_bsl(ID)
    m=0
    
    
    #for i, id1 in range(len(bsl_horizonal)):
    for i, id1 in enumerate(ID):
        for j, id2 in enumerate(ID):
            if id1 != id2:
                print(m)
                print(len(bsl_horizonal))
                print(len(bsl_vertical))
                bsl_all = bsl_horizonal[m].join([bsl_vertical[m]], how='outer').sort_index()
            
                bsl_all.to_csv('../DATA/'+ str(ID[i]) + '-' + str(ID[j]) + '-ALL.dat', header=False, date_format='%Y-%m-%dT%H:%M')
            
                result.append(bsl_all)
            
                m=m+1
        
    return(result)
