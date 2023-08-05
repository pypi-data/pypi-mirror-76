import pandas as pd
import os

def load_rlr(tgid):
    '''
    Read PSMSL RLR data files into a dataframe

    Args:
        * tgid  : tide guage id
    '''
    local_data = False
    if (local_data):
        DATA_DIR = os.path.join(os.path.dirname(__file__), '..')     
        tgfile = os.path.join(DATA_DIR,'./data/'+tgid+'.rlrdata')

    # we use the urllib to download the rlr files
    url = 'https://www.psmsl.org/data/obtaining/rlr.monthly.data/'+tgid+'.rlrdata'

    df = pd.read_csv(url, header=None, sep=";",na_values=-99999,
                   index_col='decyr', names=['decyr', 'msl', 'nmd', 'flag'])
    
    # remove missing data
    df = df.dropna()
    
    return df


