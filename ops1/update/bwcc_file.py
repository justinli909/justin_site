#!/usr/bin/python
#coding = utf-8
import os
def find_pkg():
    dir_name = r'/data/version'
    file_list = os.listdir(dir_name)
    bwcc_files = []
    for i in file_list:
        if i.startswith('bwccz'):
            bwcc_files.append(i)
    bwcc_files.sort()
    count = len(bwcc_files)
    #print bwcc_files
    #print count
    return (bwcc_files,count)

if __name__ == '__main__':
    find_pkg()

#def write_filename(f_name):
#    f = open(file_name,'a+')
#    f.write(f_name)
#    f.close()


