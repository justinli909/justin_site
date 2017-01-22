#coding=utf-8
#!/usr/bin/env python

import os

def cut_list(list_content,page_num):
    list_length = len(list_content)
    int_page_num = int(page_num)
    view_length = 8
    cuts = list_length / view_length
    cuts_remainder = list_length % view_length
    pages = 0
    if cuts_remainder > 0:
        pages = cuts + 1
    else:
        pages = cuts
    if int_page_num < pages:
        list_piece = list_content[(int_page_num-1)*view_length:int_page_num*view_length]
    elif int_page_num == pages:
        list_piece = list_content[(int_page_num-1)*view_length:]
    else:
        return False
    #print (pages,list_piece)
    return (pages,list_piece)

def cut_list2(list_content,page_num,view_length):
    #view_length = 8
    if len(list_content) == 0:
        return (0,[])
    list_length = len(list_content)
    int_page_num = int(page_num)
    cuts = list_length / view_length
    cuts_remainder = list_length % view_length
    pages = 0
    if cuts_remainder > 0:
        pages = cuts + 1
    else:
        pages = cuts
    if int_page_num < pages:
        list_piece = list_content[(int_page_num-1)*view_length:int_page_num*view_length]
    elif int_page_num == pages:
        list_piece = list_content[(int_page_num-1)*view_length:]
    else:
        return False
    #print (pages,list_piece)
    return (pages,list_piece)
    
# ##########################
#      下面两个函数备用
# ##########################

# 合服时调用此函数初始化端口池, 并把退还的端口存入srv_port库中;
def init_port(uuid,field,port):
    '''
    新的方案, 合服函数直接把uuid, 字段名和port传过来即可;
    '''
    try:
        # 追加
        get_uuid = srv_port.objects.get(uuid=uuid)
        exec("ports = get_uuid.%s" % field)
        ports = "%s,%s" % (ports,port)
        exec("get_uuid.%s=ports)" % field)
        get_uuid.save()
    except:
        # 新建
        exec("new_uuid = srv_port(uuid=uuid,%s=port)" % field)
        new_uuid.save()
    '''
    这个方案太复杂;
    all_port = srv_port.objects.all()
    all_port_uuid = []
    for i in all_port:
        all_port_uuid.append(i.uuid)
    all_server = server.objects.all()
    all_server_uuid = []
    for i in all_server:
        all_server_uuid.append(i.uuid)
    none_in_port = list(set(all_server_uuid) - set(all_port_uuid))
    # if语句用于规避长度为0的异常:
    if len(none_in_port) == 0:
        return 0
    for i in none_in_port:
        srv_port1 = srv_port(uuid=i)
        srv_port1.save()
    return len(none_in_port)
    '''
    
def dir_test(dir_name,dir_list):
    '''
    递归目录生成html, 用于显示目录结构;
    格式:
    <ul>
        <li>
            <span><i>folder_name</i></span>
            <ul>
                <li><span><i>file_name</i></span></li>
                <li><span><i>file_name</i></span></li>
            </ul>
        </li>
        <li><span><i>file_name</i></span></li>
    </ul>
    '''
    assert os.path.exists(dir_name)
    #print dir_name
    dir_html = ''
    dir_basename = os.path.basename(dir_name)
    dir_list = "%s.%s" % (dir_list,dir_basename)
    if os.path.isdir(dir_name):
        dir_html = '%s\n<li>\n\t<span><i class="glyphicon glyphicon-folder-open">%s</i></span>\n\t<ul>' % (dir_html,dir_basename)
        file_list = os.listdir(dir_name)
        for i in file_list:
            new_name = "%s/%s" % (dir_name,i)
            new_html = dir_test(new_name,dir_list)
            dir_html = "%s%s" % (dir_html,new_html)
        dir_html = "%s\n\t\t</ul>\n</li>" % dir_html
    else:
        dir_html = '%s\n\t<li><span><i onmousedown="show_path(event)" value="%s" class="glyphicon glyphicon-file">%s</i></span></li>' % (dir_html,dir_list,dir_basename)
    return dir_html
    