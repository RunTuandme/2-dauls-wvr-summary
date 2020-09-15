import datetime
import subprocess
import os

def get_igs_spd(ista, iyear, imon, iday, inp_el, inp_az, idir):
    '''
    --- Function:
           Download SPD data and extract atomospheric delay for a given
           station, observing date, elevation and azimuth.

    --- Variables:
     -> Input:
           ista ----- sequence number of a given station
                      e.g., 185 for SESHAN25
           iyear ---- year of date
           imon ----- month of date
           iday ----- day of date
           inp_el --- sequence number of zenith (e.g., 1-16)
           inp_az --- sequence number of azimuth (e.g., 1-12)
           idir ----- directory which save downloaded data


     -> Output:
           tpd ------ total path delays in cm (8*1 float)
           wpd ------ wet path delays in cm (8*1 float)
           hours ---- hours (8*1 float)

    --- Invoked Functions
           None

    '''
    import os


    ###=== Input parameters
    #+++ Sequence number of a given station
    #ista=185 # SESHAN25
    #ista=187 # SHANGHAI
    #ista=197 # TIANMA65

    #+++ Date of data requested
    #iyear=2016
    #imon=9
    #iday=12

    #iyear=2005
    #imon=10
    #iday=11



    #idir='/Users/zb/Research/VLBI_phr_atm/SPD/data/'

    #+++ Which elevation and which azimuth?
    # Zenith:
    #      No.     (deg)
    # E     1   90.000003
    # E     2   31.447786
    # E     3   20.577806
    # E     4   15.295894
    # E     5   12.128834
    # E     6   10.002515
    # E     7    8.467969
    # E     8    7.303013
    # E     9    6.384756
    # E    10    5.639587
    # E    11    5.020680
    # E    12    4.496807
    # E    13    4.046338
    # E    14    3.653808
    # E    15    3.307868
    # E    16    2.999993
    #
    # Azimuth:
    #      No.     (deg)
    # A     1    0.000000
    # A     2   32.727271
    # A     3   65.454543
    # A     4   98.181818
    # A     5  130.909086
    # A     6  163.636361
    # A     7  196.363636
    # A     8  229.090910
    # A     9  261.818172
    # A    10  294.545460
    # A    11  327.272721
    # A    12  360.000010

    elvs=[90.000003,
     31.447786,
     20.577806,
     15.295894,
     12.128834,
     10.002515,
      8.467969,
      7.303013,
      6.384756,
      5.639587,
      5.020680,
      4.496807,
      4.046338,
      3.653808,
      3.307868,
      2.999993,
    ]

    azms=[0.000000,
     32.727271,
     65.454543,
     98.181818,
    130.909086,
    163.636361,
    196.363636,
    229.090910,
    261.818172,
    294.545460,
    327.272721,
    360.000010,
    ]





    #inp_el=1
    #inp_az=10





    ### MAIN PROGRAM

    #--- Check if input parameters are reasonable
    if inp_el > 16 or inp_el < 1:
        print('---> Please check inp_el, it is out of range of 1-16')
        raise SystemExit()

    if inp_az > 12 or inp_el < 1:
        print('---> Please check inp_az, it is out of range of 1-12')
        raise SystemExit()



    #--- For elevation E(1-16), E=1; azimuth A(1-12) A=1


    scale=299792458.0*1e2 # cm/s

    sta_dcode='D     %3d' % ista

    str_yr=str(iyear)

    buff=str(100+imon)
    str_mon=buff[1:]

    buff=str(100+iday)
    str_day=buff[1:]


    buff=str(1000+ista)
    str_sta=buff[1:]

    buff=str(100+inp_el)
    nel_str='el'+buff[1:]
    buff=str(100+inp_az)
    naz_str='az'+buff[1:]

    ofile=str_sta+'_'+str_yr+str_mon+str_day+'_spd'+'_'+nel_str+'_'+naz_str+'.txt'

    del_str='%6.1f' % elvs[inp_el-1]
    daz_str='%6.1f' % azms[inp_az-1]





    tpd=[]
    wpd=[]

    dt_str0=str_yr+str_mon+str_day
    print('---> Station #:'+str_sta)
    print('---> Obsevation date (YYYYMMDD:'+ dt_str0)
    print('---> Extract tropospheric delay for Zenith '+del_str+' and Azimuth '+daz_str)

    for ihour in range(0,24,3):
        buff=str(100+ihour)
        str_hour=buff[1:]+'00'

        dt_str=dt_str0+'_'+str_hour
        fname='spd_geosfpit_'+dt_str+'.spd'

        ifile=idir+fname

        if not os.path.exists(ifile):
            if not os.path.exists(idir):
                os.mkdir(idir)
            print('---> Download the data ...')
            weburl = 'http://pathdelay.net/spd/asc/geosfpit/'+fname
            powershell_cmd = './aria2c.exe \'' + weburl + '\' -d \'' + idir + '\''
            with subprocess.Popen([r'powershell.exe', powershell_cmd], 
                stdout=subprocess.PIPE) as p:
                p.wait()
                print(p.stdout.read())
        else:
            print('---> '+ifile+' exists! Skip downloading')


        with open(ifile) as ifid:

            for line in ifid:

                #print sta_dcode

                if sta_dcode in line:
                    #print line
                    line=line.replace('D-','E-')
                    buff=line.split()
                    ielv=int(buff[2])
                    iazm=int(buff[3])


                    if ielv==inp_el and iazm==inp_az:
                        #print line
                        tot=float(buff[4])*scale
                        wat=float(buff[5])*scale

                        tpd.append(tot)
                        wpd.append(wat)


        print('---> Done for hour = '+str_hour+'\n')


    hours=list(range(0,24,3))
    return hours, tpd, wpd

def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return dates

if __name__ == '__main__':
    
    path_data_save = '../RawDatas/spa_data/'
    path_data_anly = '../Estimate/spa_result/'

    date_start = '20150807'
    date_end = '20200310'

    from tqdm import tqdm
    import time

    for dt in dateRange(date_start, date_end):

        print('---> Now is dealing with: '+str(dt))

        dy = int(dt[:4])
        dm = int(dt[4:6])
        dd = int(dt[6:])

        res = get_igs_spd(415, dy, dm, dd, 1, 1, path_data_save+str(dt)+'/')
        
        with open(path_data_anly+dt+'.txt', 'w') as file_out:
            file_out.write('time(h)\ttpd\twpd')
            for i in list(zip(res[0], res[1], res[2])):
                file_out.write('\n'+str(i[0])+'\t'+str(i[1])+'\t'+str(i[2]))
        file_out.close()