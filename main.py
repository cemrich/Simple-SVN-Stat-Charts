from chartGenerator import ChartGenerator
from distutils.dir_util import copy_tree
from os import path, makedirs
from svnLog import SvnLog
import json
import sys

'''
Created on 08.10.2012
@author: Christine Emrich
'''

def prepareDirectory(directory):
    if not path.exists(directory):
        makedirs(directory)
    
    copy_tree('htmlSource', directory)

def writeData(directory, users, dateData, hourData, dayData, nameData):
    jsFile = file(path.join(directory, 'js', 'data.js'), 'r+')
    js = jsFile.read()
    jsFile.seek(0, 0)
    js = js % {'users': json.dumps(users),
               'hourData': json.dumps(hourData),
               'dateData': json.dumps(dateData),
               'dayData': json.dumps(dayData),
               'nameData': json.dumps(nameData)}
    jsFile.write(js)
    jsFile.close()

def createStats(repoUrl):
    directory = repoUrl.strip('/\\').split('/')[-1]
    prepareDirectory(directory)
        
    log = SvnLog(repoUrl)
    generator = ChartGenerator(log)
    hourData = generator.commitsByHour()
    dateData = generator.commitsByDate()
    dayData = generator.commitsByWeekDay()
    nameData = generator.commitsByName()
    
    writeData(directory, log.getUserList(), dateData, hourData, dayData, nameData)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "please pass the full repository url as command line argument"
        exit(2)
        
    createStats(sys.argv[1])
    