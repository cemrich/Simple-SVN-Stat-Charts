'''
Created on 08.10.2012

@author: Tine
'''
   
def getListByUser(log, user):
    return filter(lambda entry: entry['name'] == user, log)

def countLogEntriesByFunc(log, func, user=None):
    dic = {}
    for entry in log:
        field = func(entry)
        dic.setdefault(field, 0)
        if not user or entry['name'] == user:  
            dic[field] += 1
    return dic