import datetime

def transform_JsonList2ListJson(JsonList):
    return [dict(zip(JsonList, r)) for r in zip(*JsonList.values())] if len(JsonList)!=0 else []

def transform_ListJson2JsonList(ListJson):
    return {k:[dic[k] for dic in ListJson] for k in ListJson[0]} if len(ListJson)!=0 else {}

def transform_Data2RecentWeekDays(date):
    assert isinstance(date, datetime.date), 'date 必須是 datetime 格式'

    weekday = date.weekday() + 1
    if (int(weekday) == 6) or (int(weekday) == 7):
            diff_date = int(weekday) - 5
    recent_weekday = date - datetime.timedelta(days=diff_date)
    return recent_weekday.strftime("%Y-%m-%d")