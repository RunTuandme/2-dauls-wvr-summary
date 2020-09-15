from datetime import datetime, timedelta

def datelist(start: str,end: str) -> list:

    date_list = [] 
    begin_date = datetime.strptime(start, r"%Y%m%d") 
    end_date = datetime.strptime(end,r"%Y%m%d") 

    while begin_date <= end_date: 
        date_str = begin_date.strftime(r"%Y%m%d") 
        date_list.append(date_str) 
        # 日期加法days=1 months=1等等
        begin_date += timedelta(days=1) 

    return date_list