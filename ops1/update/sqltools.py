#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
@version: Python2.7.5
@author:  Justinli
"""
from ops1.models import server, dbserver, domain, srv_role, jobs, wdqk_game, srv_port, ip_group, timed_jobs, job_log, cron_log, express_script, express_create, express_modify, express_run, express_log, game_proj, proj_loginfo, proj_prvi, user_priv
from djcelery.models import PeriodicTask as periodictask
from djcelery.models import CrontabSchedule as crontabschedule
from djcelery.models import IntervalSchedule as Intervalschedule
from djcelery.models import PeriodicTasks as periodictasks
from common import dbConfig, listToString
from django.contrib.auth.models import User as user

class SqlTools:

    def __init__(self, db_table):
        self.db_table = db_table
#        exec("self.db_server = %s.objects" % self.db_table)

# get_db_exact(字段,字段的值,排序字段)   get_db_exact() 默认全部
    def get_db_exact(self, *args, **kwargs):

        if len(args) == 2:
            db_filed = args[0]
            db_value = args[1]
            try:
                result = []
                #print self.db_table
                #print db_filed
                #print db_value
                exec("result_one = %s.objects.get(%s='%s')" % (self.db_table, db_filed, db_value))
                result.append(result_one)
#                result = self.db_server.filter("%s"=db_value) % db_filed
                #result = jobs.objects.filter(job_name__contains='job1')
                
            except Exception:
                result = []

        elif len(args) == 3:
            db_filed = args[0]
            db_value = args[1]
            db_order = args[2]
            try:
                exec("result = %s.objects.filter(%s='%s').order_by('%s')" % (self.db_table, db_filed, db_value, db_order))
            except Exception:
                result = []

        return result

# get_db(字段,字段的值,排序字段)   get_db() 默认全部
    def filter_db(self, *args, **kwargs):
        
        if len(args) == 2:
            db_filed = args[0]
            db_value = args[1]
            try:
                #print "result = %s.objects.filter(%s__contains='%s')" % (self.db_table, db_filed, db_value)
                exec("result = %s.objects.filter(%s='%s')" % (self.db_table, db_filed, db_value))
#                result = self.db_server.filter("%s"=db_value) % db_filed
                #result = jobs.objects.filter(job_name__contains='job1')
                
            except Exception:
                result = False
        elif len(args) == 3:
            db_filed = args[0]
            db_value = args[1]
            db_order = args[2]
            try:
                exec("result = %s.objects.filter(%s='%s').order_by('%s')" % (self.db_table, db_filed, db_value, db_order))
            except Exception:
                result = False
        elif len(args) == 0:
            #print self.db_table
            try:
                exec("result = %s.objects.all()" % self.db_table)
#                result = self.db_server.all()
            except Exception:
                result = False
        elif len(args) == 1:
            db_order = args[0]
            #print db_order
            try:
                exec("result = %s.objects.all().order_by('%s')" % (self.db_table,db_order))
            except Exception:
                result = False
        else:
            print "no args!"
            result = False
        return result
        
# get_db(字段,字段的值,排序字段)   get_db() 默认全部
    def get_db(self, *args, **kwargs):
        
        if len(args) == 2:
            db_filed = args[0]
            db_value = args[1]
            try:
                #print "result = %s.objects.filter(%s__contains='%s')" % (self.db_table, db_filed, db_value)
                exec("result = %s.objects.filter(%s__contains='%s')" % (self.db_table, db_filed, db_value))
#                result = self.db_server.filter("%s"=db_value) % db_filed
                #result = jobs.objects.filter(job_name__contains='job1')
                
            except Exception:
                result = False
        elif len(args) == 3:
            db_filed = args[0]
            db_value = args[1]
            db_order = args[2]
            try:
                exec("result = %s.objects.filter(%s__contains='%s').order_by('%s')" % (self.db_table, db_filed, db_value, db_order))
            except Exception:
                result = False
        elif len(args) == 0:
            #print self.db_table
            try:
                exec("result = %s.objects.all()" % self.db_table)
#                result = self.db_server.all()
            except Exception:
                result = False
        elif len(args) == 1:
            db_order = args[0]
            #print db_order
            try:
                exec("result = %s.objects.all().order_by('%s')" % (self.db_table,db_order))
            except Exception:
                result = False
        else:
            print "no args!"
            result = False
        return result

    def add_db(self, *args, **kwargs):
        db_name = self.db_table
        db_filed = dbConfig(db_name)
        db_value = []
        for i in range(0,len(args)):
            db_value.append(args[i])
        result_str = listToString(db_filed,db_value)
        if result_str:
            try:
                #print "result = %s.objects.create(%s)" % (db_name, result_str)
                exec("result = %s.objects.create(%s)" % (db_name, result_str))
            except Exception:
                result = False
        return result
        
# update_db(id, 其他字段)   传入的参数按照models数据库的顺序，第一个参数必须是 自增的id参数
    def update_db(self, *args, **kwargs):
        db_name = self.db_table
        db_filed = dbConfig(db_name)
        if db_filed:
            try:
                id = args[0]
                exec("id_objects = %s.objects.get(id = '%s')" % (db_name, id))
                #print id_objects.id
                for i in range(0, len(db_filed)):
                    try:
                        if type(args[i+1]) is int:
                            exec("id_objects.%s = %s" % (db_filed[i], args[i+1]))
                            #print "id_objects.%s = %s" % (db_filed[i], args[i+1])
                        else:
                            exec("id_objects.%s = '%s'" % (db_filed[i], args[i+1]))
                            #print "id_objects.%s = '%s'" % (db_filed[i], args[i+1])
                    except Exception:
                        #print "here 1"
                        result = False
                id_objects.save()
                result = True
            except Exception:
                result = False
        else:
            result = False
        return result

    # backup, not be used;
    def update_one_field(self, *args):
        assert len(args) == 4 # makesuer the lenght of arguments is 4;
        db_name = self.db_table
        get_db_field = args[0]
        get_db_field_value = args[1]
        set_db_field = args[2]
        set_db_field_value = args[3]
        # get
        try:
            exec("id_objects = %s.objects.get(%s = '%s')" % (db_name,get_db_field,get_db_field_value))
        except:
            return False
        # set
        try:
            exec("id_objects.%s = '%s'" % (set_db_field,set_db_field_value))
        except:
            return False
        id_objects.save()
        return True
        

# del_db(字段名，字段值)  删除某个特定的字段
    def del_db(self, *args, **kwargs):
        if len(args) == 2:
            db_filed = args[0]
            db_value = args[1]
            try:
                #exec("%s.objects.get(%s='%s').delete()" % (self.db_table, db_filed, db_value))
                #print "%s.objects.filter(%s='%s').delete()" % (self.db_table, db_filed, db_value)
                exec("%s.objects.filter(%s='%s').delete()" % (self.db_table, db_filed, db_value))
                result = True
            except Exception:
                result = False
        else:
            result = False
        return result
