from svnLog import SvnLog
from svnLogHelper import countLogEntriesByFunc

'''
Created on 08.10.2012
@author: Christine Emrich
'''

if __name__ == '__main__':
    repoUrl = 'https://scm.mi.hs-rm.de/svn/2011db/2011db02/'
    log = SvnLog(repoUrl)
    print log.getUserList()
        
    func = lambda entry: int(entry['date'].strftime("%w"))
    print countLogEntriesByFunc(log, func)
    print countLogEntriesByFunc(log, func, 'cemri001')