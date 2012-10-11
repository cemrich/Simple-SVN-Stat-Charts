from datetime import date, timedelta
from svnLogHelper import countLogEntriesByFunc
from time import mktime

'''
Created on 08.10.2012
@author: Christine Emrich
'''

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
class ChartGenerator(object):
    '''
    classdocs
    '''
    
    def getSeries(self, label, data):
        return {'data': data, 'label': label, 'hoverable': True}
    
    def commitsByHour(self):
        seriesArr = []
        byHourFunc = lambda entry: int(entry['date'].strftime("%H"))
        for user in self.log.getUserList():
            byHour = countLogEntriesByFunc(self.log, byHourFunc, user)
            for hour in range(24):
                if not byHour.has_key(hour):
                    byHour[hour] = 0
            series = self.getSeries(user, byHour.items())
            seriesArr.append(series)
        
        return seriesArr
    
    def commitsByDate(self):
        seriesArr = []
        byDateFunc = lambda entry: entry['date'].date()
        
        for user in self.log.getUserList():
            byDate = countLogEntriesByFunc(self.log, byDateFunc, user)
            data = [(int(mktime(date.timetuple())) * 1000, count) for date, count in byDate.items()]
            series = self.getSeries(user, data)
            seriesArr.append(series)
        
        return seriesArr
        
    def commitsByWeekDay(self):
        byDayFunc = lambda entry: int(entry['date'].strftime("%w"))
        
        seriesArr = []
        for user in self.log.getUserList():
            byDay = countLogEntriesByFunc(self.log, byDayFunc, user)
            for day in range(7):
                if not byDay.has_key(day):
                    byDay[day] = 0
            byDay = [(day-1 if day != 0 else 6, value) for day, value in byDay.items()]
            series = self.getSeries(user, byDay)
            seriesArr.append(series)
        
        return seriesArr
    
    def commitsByName(self):
        nameFunc= lambda entry: entry['name']
        seriesArr = []
        for user in self.log.getUserList():
            byName = countLogEntriesByFunc(self.log, nameFunc, user)
            series = self.getSeries(user, byName[user])
            seriesArr.append(series)
        
        return seriesArr

    def __init__(self, log):
        '''
        Constructor
        '''
        self.log = log
        self.users = log.getUserList()
