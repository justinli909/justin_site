#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
@version: Python2.7.5
@author:  Justinli
@file: thread_demo3.py
@time: 2016/3/4  18:47

"""
import os.path

class DFile:

    def __init__(self, localpath="/data/salt/scripts/"):
        self.local_path = localpath

# 写入文件 第一个参数是文件名，第二个参数是文件内容
    def write_file(self, *args, **kwargs):
        file_name = self.local_path + args[0]
        file_content = args[1]
        try:
            with open(file_name, 'w+') as fd:
                fd.writelines(file_content)
                return True
        except Exception,e:
            return False

# 读取文件，第一个参数是文件名， 返回文件内容
    def read_file(self, *args, **kwargs):
        file_name = self.local_path + args[0]
        print file_name
        file_content = ""
        try:
            with open(file_name,'r+') as fd:
                for lines in fd.readlines():
                    file_content = file_content + lines
                return file_content
        except Exception,e:
            return False

# 第一个参数是要检查的文件名
    def check_name(self, *args, **kwargs):
        filename = args[0]
        all_file = os.listdir(self.local_path)
        for i in all_file:
            j = "%s%s" % (self.local_path,i)
            if os.path.isfile(j) and i == filename:
                return True
        return False
