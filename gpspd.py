# 建立读取的gps pandas dataframe对象

import pandas as pd

def gpsfile_to_df(gpsfile: str):

    with open(gpsfile, 'r') as gf:
        for i, line in enumerate(gf, start = 1):
            if '+TROP/SOLUTION' in line:
                header_line = i
            if '-TROP/SOLUTION' in line:
                tailer_line = i
                break

    df = pd.read_csv(gpsfile, delim_whitespace = True, 
                    header = header_line, engine = 'c',skip_blank_lines = False, 
                    skiprows = [tailer_line - 1, tailer_line])
    
    return df