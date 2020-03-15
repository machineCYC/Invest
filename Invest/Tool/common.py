import datetime
from datetime import datetime as dt

def transform_JsonList2ListJson(JsonList):
    return [dict(zip(JsonList, r)) for r in zip(*JsonList.values())] if len(JsonList)!=0 else []

def transform_ListJson2JsonList(ListJson):
    return {k:[dic[k] for dic in ListJson] for k in ListJson[0]} if len(ListJson)!=0 else {}

def transform_Date2RecentWeekDays(date):
    assert isinstance(date, datetime.date), 'date 必須是 datetime 格式'

    weekday = date.weekday() + 1

    if (int(weekday) == 6) or (int(weekday) == 7):
        diff_date = int(weekday) - 5
    else:
        diff_date = 0
    recent_weekday = date - datetime.timedelta(days=diff_date)
    return recent_weekday.strftime("%Y-%m-%d")

def transform_TimeStamp2StringDate(timestamp):
    date = dt.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    return date

def transform_StringDate2TimeStamp(string_date):
    datetime_date = dt.strptime(string_date, "%Y-%m-%d")
    timestamp = dt.timestamp(datetime_date)
    return int(timestamp)

def get_Current_Date():
    stringDate = dt.now().strftime('%Y-%m-%d')
    return stringDate

def calculate_2stringDate_Datenbr(strindDate1, stringDate2):
    assert strindDate1 <= stringDate2, 'stringDate2 必須大於等於 strindDate1'

    dis_day = dt.strptime(stringDate2, '%Y-%m-%d') - dt.strptime(strindDate1, '%Y-%m-%d')
    return int(dis_day.days)

def add_DeltaDate2StringDate(stringDate, date_nbr):
    datetimeDate = dt.strptime(stringDate, '%Y-%m-%d')
    new_datetimeDate = datetimeDate + datetime.timedelta(days=date_nbr)
    return new_datetimeDate.strftime('%Y-%m-%d')

if __name__ =='__main__':
    print(transform_TimeStamp2StringDate(1350316800)=='2010-10-15') # 1581609600==2020-02-14
    print(transform_TimeStamp2StringDate(1350316800))
    print(transform_StringDate2TimeStamp('1970-01-01'))
    print('GG')


    # 1416326400 -->2014-11-19(2014-11-17)
    # 2014-11-17--> 1416153600