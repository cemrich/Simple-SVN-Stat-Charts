import os
from datetime import datetime

'''
Created on 08.10.2012
@author: Christine Emrich
'''

class SvnLog(object):
    '''
    classdocs
    '''
    
    def getUserList(self):
        return sorted(set([entry['name'] for entry in self]))
    
    def _logEntryToDict(self, entryList):
        dic = {}
        dic['revision'] = entryList[0][1:]
        dic['name'] = entryList[1]
        date = entryList[2][:19]
        dic['date'] = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        dic['lines'] = entryList[3].split()[1]
        return dic

    def _getLog(self):
        p = os.popen('svn log ' + self.repoUrl)
        log = p.readlines()
        log = [self._logEntryToDict(entry.strip().split(" | "))
        for entry in log
            if entry[0] == 'r' and 
            (entry.endswith("line\n") or entry.endswith("lines\n"))]
        p.close()
        return log

    def __init__(self, repoUrl):
        '''
        Constructor
        '''
        self.repoUrl = repoUrl
        self.log = self._getLog()
        
    def __str__(self):
        return str(self.log)
    
    def __iter__(self):
        return self.log.__iter__()
