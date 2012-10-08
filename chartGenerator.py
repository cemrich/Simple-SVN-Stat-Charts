from graphy.backends import google_chart_api
from svnLogHelper import countLogEntriesByFunc
from datetime import date
from datetime import timedelta

'''
Created on 08.10.2012

@author: Tine
'''
        
def getPercentageStr(label, total, part):
    percent = float(part)/total*100
    percent = round(percent * 10) / 10.0
    return "%s (%s / %s%%)" % (label, part, percent)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
class ChartGenerator(object):
    '''
    classdocs
    '''

    chartColors = ['8DD3C7', 'EECCB3', 'BEBADA', 'FB8072', 
                   '80B1D3', 'FDB462', 'B3DE69', 'FCCDE5', 
                   'D9D9D9', 'BC80BD', 'CCEBC5', 'FFED6F']
    
    def _colorChart(self, chart):
        index = -1
        for series in chart.data:
            if series.style.color is None:
                index += 1
                if index >= len(self.chartColors): 
                    index = 0
            series.style.color = self.chartColors[index]
    
    def _getCommitBarChart(self, userDic, maxCommits):
        chart = google_chart_api.BarChart()
        chart.stacked = True
        for name, values in userDic.items():
            chart.AddBars(values, label=name)
        self._colorChart(chart)
        
        # labeling on left axis
        chart.left.min = 0
        chart.left.max = maxCommits
        chart.left.labels = range(0, chart.left.max + 2, 5)
        chart.left.label_positions = chart.left.labels
        chart.left.label_gridlines = True
        
        return chart
    
    def commitsByHour(self, user=None):
        userDic = {}
        byHourFunc = lambda entry: int(entry['date'].strftime("%H"))
        maxCommits = max(countLogEntriesByFunc(self.log, byHourFunc).values())
        users = [user] if user else self.users
        for user in users:
            byHour = countLogEntriesByFunc(self.log, byHourFunc, user)
            byHourArr = [byHour[hour] if byHour.has_key(hour) else None for hour in range(24)]
            userDic[user] = byHourArr
        
        chart = self._getCommitBarChart(userDic, maxCommits)
        chart.bottom.labels = range(24)
        return chart
    
    def commitsByDate(self, user=None):
        byDateFunc = lambda entry: date(entry['date'].year, entry['date'].month, entry['date'].day)
        byDay = countLogEntriesByFunc(self.log, byDateFunc)
        minDate = min(byDay)
        maxDate = max(byDay)
        maxCommits = max(byDay.values())
        keys = [day.strftime("%a, %d.%m") for day in daterange(minDate, maxDate)]
        
        userDic = {}
        users = [user] if user else self.users
        for user in users:
            byUserDay = countLogEntriesByFunc(self.log, byDateFunc, user)
            days = [byUserDay[day] if byUserDay.has_key(day) else None for day in daterange(minDate, maxDate)]
            userDic[user] = days
        
        chart = self._getCommitBarChart(userDic, maxCommits)
        
        chart.bottom.label_gridlines = True
        chart.bottom.min = 0
        chart.bottom.max = len(keys)
        chart.bottom.labels = keys[::7]
        chart.bottom.label_positions = range(0, len(keys), 7)
        return chart
    
    def commitsByName(self):
        byName = countLogEntriesByFunc(self.log, lambda entry: entry['name'])
        names, commits = zip(*byName.items())
        totalCommits = sum(commits)
        names = [getPercentageStr(name, totalCommits, byName[name]) for name in names]
        chart = google_chart_api.PieChart(commits, names)
        return chart
    
    def commitsByWeekDay(self, user=None):
        byDay = countLogEntriesByFunc(self.log, lambda entry: int(entry['date'].strftime("%w")), user)
        dayNumber, commits = zip(*byDay.items())
        days = 'Sonntag Montag Dienstag Mittwoch Donnerstag Freitag Samstag'.split()
        
        if user:
            chart = self._getCommitBarChart({'commits': commits[1:] + commits[:1]}, max(commits))
            chart.bottom.labels = days[1:] + days[:1]
            return chart
        else:
            totalCommits = sum(commits)
            labels = [getPercentageStr(days[dayNum], totalCommits, byDay[dayNum]) for dayNum in dayNumber]
            chart = google_chart_api.PieChart(commits, labels)
            return chart

    def __init__(self, log):
        '''
        Constructor
        '''
        self.log = log
        self.users = log.getUserList()
