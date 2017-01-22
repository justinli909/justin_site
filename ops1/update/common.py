#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
@version: Python2.7.5
@author:  Justinli
"""

import ConfigParser

def dbConfig(dbname):
    print dbname
    dbconf = ConfigParser.ConfigParser()
    dbconf.read('/root/django/devops/ops1/update/db.conf')
    try:
        key_string = dbconf.get(dbname,dbname)
        result = key_string.split(',')
    except Exception:
        result = False
    return result
    
def listToString(list1, list2):
    list_one = list1
    list_two = list2
    new_str = ""
    for i in range(0,len(list_one)):
        if type(list_two[i]) is int:
            new_str = new_str + list_one[i] + "=" + str(list_two[i]) + ","
        elif list_two[i] == 'NULL':
            new_str = new_str + list_one[i] + "=" + str(list_two[i]) + ","
        else:
            try:
                int(list_two[i])
                new_str = new_str + list_one[i] + "=" + list_two[i] + ","
            except:
                new_str = new_str + list_one[i] + "=" + "\'" + list_two[i] + "\',"
    return new_str[:-1]