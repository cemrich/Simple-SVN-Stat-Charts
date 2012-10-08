import sys
from svnLog import SvnLog
from chartGenerator import ChartGenerator
from os import path, makedirs

'''
Created on 08.10.2012

@author: Tine
'''

template = "<html><head><meta charset='utf-8'><title>SVN Statistics</title><style type='text/css'>%s</style></head><body>%s</body></html>"
link = '<a href="%s" class="%s">%s</a>'
cssStyle = ''

def loadCss():
    global cssStyle
    style = file('css/style.css', 'r')
    cssStyle = style.read()
    style.close()

def writeChartsToFile(directory, charts, fileName=None, pageList=None):
    if not fileName:
        fileName = 'overview' 
        
    innerHtml = '<h1>' + fileName + '</h1>'
       
    if pageList:
        pageList.insert(0, 'overview')
        innerHtml += '<nav>'
        for page in pageList:
            cssClass = 'active' if page == fileName else ''
            innerHtml += link % (page + '.html', cssClass, page)
        innerHtml += '</nav>'
    
    for headline, chart in charts:
        innerHtml += '<h2>' + headline + '</h2>'
        innerHtml += chart.display.Img(800, 300)
        
       
    html = template % (cssStyle, innerHtml)
    
    if not path.exists(directory):
        makedirs(directory)

    htmlFile = file(path.join(directory, fileName) + '.html', 'w')
    htmlFile.write(html)
    htmlFile.close()

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print "please pass the full repository url as command line argument"
        exit(2)
        
    repoUrl = sys.argv[1]
    directory = repoUrl.strip('/\\').split('/')[-1]
    log = SvnLog(repoUrl)
    users = log.getUserList()
    generator = ChartGenerator(log)
    loadCss()
    
    charts = []
    charts.append(('commits by date', generator.commitsByDate()))
    charts.append(('commits by hour', generator.commitsByHour()))
    charts.append(('commits by weekday', generator.commitsByWeekDay()))
    charts.append(('commits by user', generator.commitsByName()))
    writeChartsToFile(directory, charts, pageList=list(users))
    
    for user in users:
        charts = []
        charts.append(('commits by date', generator.commitsByDate(user)))
        charts.append(('commits by hour', generator.commitsByHour(user)))
        charts.append(('commits by weekday', generator.commitsByWeekDay(user)))
        writeChartsToFile(directory, charts, user, list(users))