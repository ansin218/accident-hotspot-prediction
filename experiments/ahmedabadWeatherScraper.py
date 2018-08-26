from time import time
from datetime import timedelta
import datetime
from urllib.request import urlopen
import re
import pandas as pd
from pandas import ExcelWriter

start_time = time()

def date_splitter(dateToSplit):
    dateToSplit = dateToSplit.split('-', 1)
    year = dateToSplit[0]
    dateToSplit = dateToSplit[1].split('-', 1)
    month = dateToSplit[0]
    day = dateToSplit[1]
    return year, month, day

def extractTime(s):
    time = re.findall('\d+:\d+', s)
    return time

def extractConditions(s):
    x = re.findall('"small",h:"', s)
    condList = []
    for i in range(len(x)):
        s = s.split('"small",h:"', 1)
        s = s[1].split('."},{s', 1)
        condList.append(s[0])
        s = s[1]
    return condList

def extractVisibility(s):
    s = s.replace('&nbsp;', '')
    re1 = '(\\d+)'
    re2 = ''
    re3 = 'km'
    visibilities = re.findall(re1 + re2 + re3, s)
    return visibilities

def extractTemperature(s):
    s = s.replace('°', '')
    s = s.replace('&nbsp;', '')
    re1='\d+'
    re2='[A-Z]'
    temperatures = re.findall(re1 + re2, s)
    tempList = list()
    for i in range(len(temperatures)):
        x = re.findall(re1, temperatures[i])[0]
        tempList.append(x)
    return tempList

finalRawDf = pd.DataFrame()

for i in range(12, 42):
    startDate = str(datetime.date.today() + timedelta(days = -i))
    d_year, d_month, d_day = date_splitter(startDate)
    finalDate = d_year + d_month + d_day
    if d_month == '07':
        link = 'https://www.timeanddate.com/scripts/cityajax.php?n=india/ahmedabad&mode=historic&hd=' + finalDate + '&month=7&year=2018&json=1'

    print('Scraping:', link)
    html = urlopen(link)
    s = html.read().decode('utf-8')

    times = extractTime(s)
    visibility = extractVisibility(s)
    temperature = extractTemperature(s)
    condition = extractConditions(s)

    if(len(visibility) < len(condition)):
        remLength = len(condition) - len(visibility)
        for i in range(remLength):
            if(len(visibility) == 0):
                visibility.append('7')
            else:
                visibility.append(visibility[0])

    tempDf = pd.DataFrame({
            'weatherDate': finalDate,
            'time': times,
            'temperature': temperature,
            'visibility': visibility,
            'condition': condition
            })

    finalRawDf = finalRawDf.append(tempDf)

writer = ExcelWriter('ahmedabad-weather.xlsx')
finalRawDf.to_excel(writer, index = False, sheet_name = 'Sheet1')
writer.save()

end_time = time()
time_taken = end_time - start_time

print("\nTotal time taken in seconds: ", time_taken)