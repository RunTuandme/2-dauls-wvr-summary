from datetime import datetime

def get_gps_file(date: str)-> str:
    # date: 20170101

    year = date[:4]
    month = date[4:6]
    day = date[-2:]

    dd = datetime.strptime(date, '%Y%m%d')
    dstart = datetime.strptime(year, '%Y')
    doy = (dd - dstart).days + 1

    if doy < 10:
        doy_str = '00' + str(doy)
    elif doy < 100:
        doy_str = '0' + str(doy)
    else:
        doy_str = str(doy)

    f = '../RawDatas/IGS_ZPD_SHAO/' + 'SHAO' + doy_str + '0.' + year[-2:] + 'zpd'

    return f