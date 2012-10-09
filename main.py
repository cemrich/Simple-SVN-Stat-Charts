import sys
from svnLog import SvnLog
from chartGenerator import ChartGenerator
from os import path, makedirs

'''
Created on 08.10.2012
@author: Christine Emrich
'''

template = "<html><head><meta charset='utf-8'><title>SVN Statistics</title><style type='text/css'>%s</style></head><body><h1>%s</h1>%s</body></html>"
link = '<a href="%s" class="%s">%s</a>'
cssStyle = ''

def loadCss():
    global cssStyle
    style = file('css/style.css', 'r')
    cssStyle = style.read()
    style.close()

def writeChartsToFile(directory, charts, pageList, fileName=None):
    if not fileName:
        fileName = 'overview' 
     
    pageList.insert(0, 'overview')
    innerHtml = '<nav>'
    for page in pageList:
        cssClass = 'active' if page == fileName else ''
        innerHtml += link % (page + '.html', cssClass, page)
    innerHtml += '</nav>'
    
    for headline, chart in charts:
        innerHtml += '<h2>' + headline + '</h2>'
        innerHtml += chart.display.Img(800, 300)
       
    html = template % (cssStyle, fileName, innerHtml)

    htmlFile = file(path.join(directory, fileName) + '.html', 'w')
    htmlFile.write(html)
    htmlFile.close()

def getOverviewCharts(chartGenerator):
    charts = []
    charts.append(('commits by date', chartGenerator.commitsByDate()))
    charts.append(('commits by hour', chartGenerator.commitsByHour()))
    charts.append(('commits by weekday', chartGenerator.commitsByWeekDay()))
    charts.append(('commits by user', chartGenerator.commitsByName()))
    return charts

def getUserCharts(chartGenerator, userName):
    charts = []
    charts.append(('commits by date', chartGenerator.commitsByDate(userName)))
    charts.append(('commits by hour', chartGenerator.commitsByHour(userName)))
    charts.append(('commits by weekday', chartGenerator.commitsByWeekDay(userName)))
    return charts

def createSats(repoUrl):
    directory = repoUrl.strip('/\\').split('/')[-1]
    
    if not path.exists(directory):
        makedirs(directory)
        
    log = SvnLog(repoUrl)
    users = log.getUserList()
    generator = ChartGenerator(log)
    loadCss()
    
    overViewCharts = getOverviewCharts(generator)
    writeChartsToFile(directory, overViewCharts, list(users))
    
    for user in users:
        charts = getUserCharts(generator, user)
        writeChartsToFile(directory, charts, list(users), user)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "please pass the full repository url as command line argument"
        exit(2)
        
    createSats(sys.argv[1])
    