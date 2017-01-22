# Create your views here.
import os,json,commands
from django.http import HttpResponse
#from django.shortcuts import render, render_to_response, HttpResponseRedirect

def script_names(request):
    filelist = os.listdir('/data/salt/scripts/')
    return HttpResponse(json.dumps(filelist))

def check_name(request):
    file_name = request.GET['file_name']
    file_path = '/data/salt/scripts/'
    full_name = file_path + file_name
    bl_exist = os.path.isfile(full_name)
    result = {}
    if bl_exist:
        with open(full_name,'r') as f:
            content = f.readlines()
        content = ''.join(content)
        result["content"] = content
        result['status'] = 2
    else:
        result["content"] = "Null"
        result['status'] = 1
    #print result
    return HttpResponse(json.dumps(result))
        
def save_script(request):
    #print "1"
    file_name = request.POST['file_name']
    script_txt = request.POST['script_txt']
    file_path = '/data/salt/scripts/'
    full_name = file_path + file_name
    try:
        with open(full_name,'w') as f:
            f.write(script_txt)
        return HttpResponse(True)
    except:
        return HttpResponse(False)

def run_scripts(request):
    #print "start"
    scripts_list = request.POST['scripts_list']
    exec('scripts_list = %s' % scripts_list)
    #assert type(scripts_list) is list
    async_return = commands.getstatusoutput('salt "*" state.sls rsync2')
    result = []
    if async_return[0] != 0:
        result['code'] = async_return[0]
        result['txt'] = async_return[1]
        return HttpResponse(json.dumps(result))
    for i in scripts_list:
        script_one = {}
        for k in i:
            cmd_output = commands.getstatusoutput(i[k])
            script_one['script'] = k
            script_one['code'] = str(cmd_output[0])
            script_one['txt'] = cmd_output[1]
        result.append(script_one)
    return HttpResponse(json.dumps(result))

