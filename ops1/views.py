#coding=utf-8
# Create your views here.
#from ops1.models import server, dbserver, domain, srv_role, jobs, wdqk_game, srv_port
#from ops1.models import jobs
#from ops1.models import game_proj,proj_loginfo,proj_prvi
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.core.paginator import Paginator
from ops1.tasks import run_update, start_one_job
from ops1.update.sqltools import SqlTools
from ops1.update.DFile import DFile
from ops1.update.function import cut_list2,cut_list
from ops1.update.jobcron import Job, Cron
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import sys, re, time, random, os, commands, json, urllib2, urllib

@login_required
def changepasswd(request):
    user_name = request.POST['user_name']
    old_passwd = request.POST['old_passwd']
    new_passwd = request.POST['new_passwd']
    new_passwd_r = request.POST['new_passwd_r']
    user_name2 = request.user.username
    if user_name2 != user_name:
        return HttpResponse(False)
    user = auth.authenticate(username=user_name, password=old_passwd)
    if user is None:
        return HttpResponse('wrong_old_passwd')
    if new_passwd != new_passwd_r:
        return HttpResponse('invalid_new_passwd')
    user.set_password(new_passwd)
    user.save()
    logout(request)
    return HttpResponse(True)
    
@login_required
def change_passwd(request):
    user_name = request.user.username
    return render_to_response('change_passwd.html',{'user_name':user_name})

@login_required
def delete_user(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    del_user_name = request.POST['del_user_name']
    try:
        user_db = User.objects.get(username=del_user_name)
        user_db.delete()
        return HttpResponse(True)
    except:
        return HttpResponse(False)

@login_required
def start_user(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    del_user_name = request.POST['del_user_name']
    try:
        user_db = User.objects.get(username=del_user_name)
        user_db.is_active = 1
        user_db.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)

@login_required
def stop_user(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    del_user_name = request.POST['del_user_name']
    try:
        user_db = User.objects.get(username=del_user_name)
        user_db.is_active = 0
        user_db.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)

@login_required
def create_user(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    user_name = request.POST['user_name']
    user_passwd = request.POST['user_passwd']
    user_passwd_r = request.POST['user_passwd_r']
    if user_passwd != user_passwd_r:
        return HttpResponse(False)
    try:
        user1 = User.objects.create_user(user_name,'',user_passwd)
        user1.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)

@login_required
def priv_del(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    priv_proj = request.POST['priv_proj']
    priv_user = request.POST['priv_user']
    user_priv = SqlTools('user_priv')
    db_data = user_priv.filter_db('proj',priv_proj).filter(user=priv_user)
    #print db_data
    assert len(db_data) == 1
    db_data.delete()
    return HttpResponse(True)

@login_required
def update_priv(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    priv_proj = request.POST['priv_proj']
    priv_user = request.POST['priv_user']
    priv_n = int(request.POST['priv_n'])
    user_priv = SqlTools('user_priv')
    priv_data = user_priv.filter_db('proj',priv_proj)
    #print priv_data
    if len(priv_data) == 0:
        user_priv.add_db(priv_proj,priv_user,priv_n)
        return HttpResponse(True)
    user_priv_data = priv_data.filter(user=priv_user)
    #print user_priv_data
    if len(user_priv_data) == 0:
        user_priv.add_db(priv_proj,priv_user,priv_n)
    else:
        assert len(user_priv_data) == 1
        user_priv_data[0].priv = priv_n
        user_priv_data[0].save()
    return HttpResponse(True)
    
@login_required
def del_game_proj(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    proj_name = request.POST['proj_name']
    game_proj = SqlTools('game_proj')
    proj_data = game_proj.get_db_exact('proj_name',proj_name)[0]
    proj_data.delete()
    return HttpResponse(True)

@login_required
def get_script_names(request):
    proj_ip = request.session['proj_ip']
    url = 'http://%s:8082/script_names/' % proj_ip
    url_return = urllib2.urlopen(url)
    return HttpResponse(url_return)
    
@login_required
def update_proj(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    proj_name = request.POST['proj_name']
    proj_ip = request.POST['proj_ip']
    game_proj = SqlTools('game_proj')
    proj_data = game_proj.get_db_exact('proj_name',proj_name)[0]
    proj_data.proj_ip = proj_ip
    proj_data.save()
    return HttpResponse(True)

#@login_required
def get_proj_name(request):
    table_name = request.POST['table_name']
    table_db = SqlTools(table_name)
    db_data = table_db.get_db()
    data = []
    for i in db_data:
        data.append(i.get_values()['proj_name'])
    return HttpResponse(json.dumps(data))

@login_required
def get_proj_priv(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    table_name = request.POST['table_name']
    table_db = SqlTools(table_name)
    db_data = table_db.get_db()
    data = []
    for i in db_data:
        data.append(i.get_values())
    #print data
    return HttpResponse(json.dumps(data))

@login_required
def del_prvi(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    proj_user = request.POST['proj_user']
    proj_names = request.POST['proj_names']
    proj_prvi = SqlTools('proj_prvi')
    proj_prvi_db = proj_prvi.get_db_exact('user',proj_user)
    proj_prvi_old = proj_prvi_db[0].proj.split(',')
    proj_name_list = []
    proj_name_list.append(proj_names)
    proj_prvi_new_list = list(set(proj_prvi_old)^set(proj_name_list))
    if len(proj_prvi_new_list) == 0:
        proj_prvi_db[0].delete()
        return HttpResponse(True)
    proj_prvi_new = ','.join(proj_prvi_new_list)
    #print proj_prvi_new
    proj_prvi_db[0].proj = proj_prvi_new
    #print proj_prvi_db[0].proj
    proj_prvi_db[0].save()
    return HttpResponse(True)

#@login_required
#def check_proj_del(request):
#    if request.user.username != 'root':
#        return HttpResponse(False)
#    current_user = request.POST['current_user']
#    proj_prvi = SqlTools('proj_prvi')
#    proj_prvi_db = proj_prvi.get_db_exact('user',current_user)
#    proj_prvi_list = []
#    if len(proj_prvi_db) !=0:
#        proj_prvi_list = proj_prvi_db[0].proj.split(',')
#    return HttpResponse(json.dumps(proj_prvi_list))

#@login_required
#def check_proj(request):
#    if request.user.username != 'root':
#        return HttpResponse(False)
#    current_user = request.POST['current_user']
#    game_proj = SqlTools('game_proj')
#    proj_prvi = SqlTools('proj_prvi')
#    game_proj_db = game_proj.get_db()
#    proj_prvi_db = proj_prvi.get_db_exact('user',current_user)
#    game_proj_list = []
#    proj_prvi_list = []
#    if len(game_proj_db) != 0:
#        for i in game_proj_db:
#            game_proj_list.append(i.proj_name)
#    if len(proj_prvi_db) !=0:
#        proj_prvi_list = proj_prvi_db[0].proj.split(',')
#    diff_proj = list(set(game_proj_list)^set(proj_prvi_list))
#    #print diff_proj
#    return HttpResponse(json.dumps(diff_proj))

@login_required
def assign_user_proj(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    proj_user = request.POST['proj_user']
    proj_names = request.POST['proj_names']
    proj_prvi = SqlTools('proj_prvi')
    priv_get = proj_prvi.get_db_exact('user',proj_user)
    if len(priv_get) == 0:
        proj_prvi.add_db(proj_user,proj_names)
    else:
        proj_names_old = priv_get[0].proj
        if proj_names not in proj_names_old.split(','):
            proj_names_new = '%s,%s' % (proj_names_old,proj_names)
            priv_get[0].proj = proj_names_new
            priv_get[0].save()
        else:
            return HttpResponse("False")
    return HttpResponse("True")

@login_required
def create_proj(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    proj_name = request.POST['proj_name']
    proj_ip = request.POST['proj_ip']
    game_proj = SqlTools('game_proj')
    add_result = game_proj.add_db(proj_name,proj_ip)
    if add_result != False:
        add_result = True
    #print type(add_result)
    return HttpResponse(add_result)

@login_required
def get_proj_data(request):
    if request.user.username != 'root':
        return HttpResponse(False)
    proj_db = SqlTools('game_proj')
    user_db = SqlTools('user')
    proj_data = proj_db.get_db()
    user_data = user_db.get_db()
    proj_list = []
    #proj_ips = {}
    if proj_data != False:
        for i in proj_data:
            proj_list.append(i.proj_name)
            #proj_ips[i.proj_name] = i.proj_ip
    else:
        proj_list.append('none')
    user_list = []
    if user_data != False:
        for i in user_data:
            if i.username != 'root':
                user_list.append(i.username)
    else:
        user_list.append('none')
    result = {}
    #result['ip'] = proj_ips
    result['proj'] = proj_list
    result['user'] = user_list
    #print result
    return HttpResponse(json.dumps(result))

@login_required
def proj_admin(request):
    user = request.user
    if user.username != 'root':
        return HttpResponse('Forbidden!')
    return render_to_response('proj_admin.html',{'user':user})

def r_success(request):
    return render_to_response('registration/r_success.html')
    
def invalid(request):
    return render_to_response('registration/invalid.html')

def success(request):
    return render_to_response('registration/success.html',{'user':request.user})
    
# should be closed;
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return Redirect("/r_success/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })
    
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    proj = request.POST.get('projname', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        proj_db = SqlTools('game_proj')
        try:
            proj_ip = proj_db.get_db_exact('proj_name',proj)[0].proj_ip
        except:
            proj_ip = 'none'
        #print proj_ip
        if username != 'root':
            proj_prvi = SqlTools('proj_prvi')
            proj_db = proj_prvi.get_db_exact('user',username)
            print proj_db
            #proj_name_list = proj_db[0].get_values()['proj'].split(',')
            assert len(proj_db) == 1
            proj_name_list = proj_db[0].get_values()['proj']
            if proj in proj_name_list:
                request.session["proj"] = proj
                request.session["proj_ip"] = proj_ip
            else:
                return HttpResponse('无项目权限!')
            user_priv = SqlTools('user_priv')
            try:
                data_priv = user_priv.filter_db('proj',proj).filter(user=username)[0].priv
                request.session["priv"] = data_priv
            except:
                return HttpResponse('无操作权限!')
        else:
            request.session["proj"] = 'none'
            request.session["proj_ip"] = proj_ip
            request.session["priv"] = 3
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        r_url = request.POST['next']
        if r_url != "":
            return HttpResponseRedirect(r_url)
        else:
            return HttpResponseRedirect("/")
    else:
        # Show an error page
        return HttpResponseRedirect("/invalid/")
    
def success(request):
    return render_to_response('registration/success.html',{'user':request.user})
    
@login_required
def change_status(request):
    priv = request.session['priv']
    if priv < 3:
        return HttpResponse('error')
    timed_job_name = request.POST['timed_job_name']
    timed_job_name1 = Cron(timed_job_name)
    result = timed_job_name1.change_status()
    return HttpResponse(result)

@login_required
def query_jobs(request):
    proj = request.session['proj']
    current_page = request.POST['current_page']
    query_timed_job = request.POST['query_timed_job']
    query_creator = request.POST['query_creator']
    query_status = request.POST['query_status']
    timed_jobs = SqlTools('timed_jobs')
    periodictask = SqlTools('periodictask')
    crontabschedule = SqlTools('crontabschedule')
    if request.user.username != 'root':
        return_data = timed_jobs.get_db('timed_job',query_timed_job).filter(project=proj) # search timed_job_name;
    else:
        return_data = timed_jobs.get_db('timed_job',query_timed_job)
    return_data = return_data.filter(creater__contains=query_creator) # search creator;
    query_list = []
    if len(return_data) != 0:
        for i in return_data:
            query_dir_one = {}
            periodictask_data = periodictask.get_db_exact('name',i.timed_job)
            enabled = periodictask_data[0].enabled
            getted_status = ''
            if enabled:
                getted_status = 'Started'
            else:
                getted_status = 'Paused'
            if query_status != 'all' and getted_status != query_status:
                continue
            query_dir_one['status'] = getted_status
            query_dir_one['timed_job']=i.timed_job
            query_dir_one['job_name'] = periodictask_data[0].args.split('"')[1]
            crontab_id = periodictask_data[0].crontab_id
            query_dir_one['time_data'] = crontabschedule.get_db_exact('id',crontab_id)[0].__str__()[:-14]
            query_dir_one['creater']=i.creater
            query_dir_one['create_time']=i.create_time.isoformat(' ').split('+')[0]
            query_dir_one['modified_by']=i.modified_by
            query_dir_one['modified_time']=i.modified_time.isoformat(' ').split('+')[0]
            query_list.append(query_dir_one)
        cut_list_return = cut_list(query_list,current_page)
        query_list_cutted = cut_list_return[1]
        pages = cut_list_return[0]
    else:
        query_list_cutted=[]
        pages = 0
    query_dir = {}
    query_dir['data'] = query_list_cutted
    query_dir['pages'] = pages
    return HttpResponse(json.dumps(query_dir))

@login_required
def del_timed_job(request):
    priv = request.session['priv']
    if priv < 3:
        return HttpResponse('error')
    timed_job_name = request.POST['timed_job']
    timed_jobs = SqlTools('timed_jobs')
    periodictask = SqlTools('periodictask')
    crontabschedule = SqlTools('crontabschedule')
    crontab_id = periodictask.get_db_exact('name',timed_job_name)[0].crontab_id
    timed_del_return = timed_jobs.del_db('timed_job',timed_job_name)
    if timed_del_return:
        periodictask_del_return = periodictask.del_db('name',timed_job_name)
    if periodictask_del_return:
        crontab_del_return = crontabschedule.del_db('id',crontab_id)
    return HttpResponse(crontab_del_return)

@login_required
def get_cron_log(request):
    uuid = request.GET['uuid']
    filename = '/var/opslog/cronlog/' + uuid + '.log'
    log_file = open(filename,'r')
    data = log_file.readlines()
    return HttpResponse(data)

#@login_required
def get_jog_log(request):
    uuid = request.GET['uuid']
    filename = '/var/opslog/joblog/' + uuid + '.log'
    log_file = open(filename,'r')
    data = log_file.readlines()
    return HttpResponse(data)

@login_required
def get_cron_history(request):
    cron_name = request.GET['cron_name']
    page_num = request.GET['page_num']
    cron_log = SqlTools('cron_log')
    result_get = cron_log.get_db_exact('cron_name',cron_name,'-run_time')
    data = []
    for i in result_get:
        data_one = {}
        data_one['run_time'] = i.run_time.isoformat(' ').split('+')[0]
        data_one['uuid'] = i.uuid
        data_one['code'] = i.code
        data.append(data_one)
    page_view_length = 15
    job_cut_result = cut_list2(data,page_num,page_view_length)
    db_data = {}
    db_data['pages'] = job_cut_result[0]
    db_data['data'] = job_cut_result[1]
    return HttpResponse(json.dumps(db_data))

@login_required
def get_job_history(request):
    job_name = request.GET['job_name']
    page_num = request.GET['page_num']
    job_log = SqlTools('job_log')
    result_get = job_log.get_db_exact('job_name',job_name,'-run_time')
    data = []
    for i in result_get:
        data_one = {}
        data_one['run_time'] = i.run_time.isoformat(' ').split('+')[0]
        data_one['uuid'] = i.uuid
        data_one['run_user'] = i.run_user
        data_one['code'] = i.code
        data.append(data_one)
    page_view_length = 10
    job_cut_result = cut_list2(data,page_num,page_view_length)
    db_data = {}
    db_data['pages'] = job_cut_result[0]
    db_data['data'] = job_cut_result[1]
    return HttpResponse(json.dumps(db_data))

@login_required
def save_timed_jobs(request):
    if request.session['priv'] <3:
        return HttpResponse('error')
    proj = request.session['proj']
    proj_ip = request.session['proj_ip']
    result = {}
    timed_job_name = request.POST['timed_job_name']
    job_name = request.POST['job_name']
    cron_args = '["%s","%s","%s","%s"]' % (job_name,timed_job_name,proj_ip,proj)
    start_time = request.POST['start_time']
    cron_data = start_time.split(' ')
    modified_by = request.user.username
    status = "Started"
    timed_jobs = SqlTools('timed_jobs')
    periodictask = SqlTools('periodictask')
    crontabschedule = SqlTools('crontabschedule')
    update_flag = request.POST['del_flag']
    if update_flag == '1':
        # ### UPDATE code block; ###
        get_data = timed_jobs.get_db_exact('timed_job',timed_job_name)[0]
        get_periodictask_data = periodictask.get_db_exact('name',timed_job_name)[0]
        get_crontab_id = get_periodictask_data.crontab_id
        enable_task = get_periodictask_data.enabled
        if enable_task:
            enable_task = 1
        else:
            enable_task = 0
        update_periodictask_id = get_periodictask_data.id
        update_crontab_return = crontabschedule.update_db(get_crontab_id,cron_data[0],cron_data[1],cron_data[2],cron_data[3],cron_data[4])
        if update_crontab_return:
            update_periodictask_return = periodictask.update_db(update_periodictask_id,timed_job_name,'ops1.tasks.start_one_job',get_crontab_id,cron_args,'{}',enable_task)
        if update_periodictask_return:
            try:
                get_data.modified_by = modified_by
                get_data.save()
            except:
                result['return'] = False
                return HttpResponse(json.dumps(result))
    else:
        # ### ADD code block; ###
        creater = request.user.username
        cron_add = crontabschedule.add_db(cron_data[0],cron_data[1],cron_data[2],cron_data[3],cron_data[4])
        cron_add_id = int(cron_add.id)
        enable_task = 1
        if cron_add:
            periodic_task_add = periodictask.add_db(timed_job_name,'ops1.tasks.start_one_job',cron_add_id,cron_args,'{}',enable_task)
        if periodic_task_add:
            add_result = timed_jobs.add_db(timed_job_name,creater,modified_by,proj)
        else:
            cron_add.delete()
            add_result = False
        if not add_result:
            result['return'] = False
            return HttpResponse(json.dumps(result))
    
    # Query the updated or added data;
    periodic_task_final = periodictask.get_db_exact('name',timed_job_name)[0]
    crontab_id = periodic_task_final.crontab_id
    crontab_final = crontabschedule.get_db_exact('id',crontab_id)[0]
    timed_job_final = timed_jobs.get_db_exact('timed_job',timed_job_name)[0]
    result['return'] = True
    result['timed_job'] = timed_job_final.timed_job
    result['job_name'] = periodic_task_final.args.split('"')[1]
    result['time_data'] = crontab_final.__str__()[:-14]
    result['creater'] = timed_job_final.creater
    result['create_time'] = timed_job_final.create_time.isoformat(' ').split('+')[0]
    result['modified_by'] = timed_job_final.modified_by
    result['modified_time'] = timed_job_final.modified_time.isoformat(' ').split('+')[0]
    if periodic_task_final.enabled == 1:
        status = 'Started'
    elif periodic_task_final.enabled == 0:
        status = 'Paused'
    else:
        status = 'Disabled'
    result['status'] = status
    return HttpResponse(json.dumps(result))

@login_required
def timing_job(request):
    priv = request.session['priv']
    user = request.user
    proj = request.session['proj']
    return render_to_response('timing_job.html',{'user':user,'proj':proj,'priv':priv})

@login_required
def interactive_shell(request):
    return render_to_response('interactive_shell.html',{})

@login_required
def get_job(request):
    proj = request.session['proj']
    priv = request.session['priv']
    job_name = request.GET['job_name']
    user_name = request.GET['user_name']
    page_num = request.GET['page_num']
    jobs1 = SqlTools('jobs')
    jobs_id_jobname = jobs1.get_db('job_name',job_name,'job_name').filter(project=proj)
    jobs_id_jobname_username = jobs_id_jobname.filter(job_user__contains=user_name)
    job_name_list = []
    job_dir = {}
    job_dir_list = []
    if len(jobs_id_jobname_username) != 0:
        for i in jobs_id_jobname_username:
            job_name_tmp = i.job_name
            user_name_tmp = i.job_user
            if job_name_tmp not in job_name_list:
                job_one = {}
                job_one['job_user'] = user_name_tmp
                job_one['job_name'] = job_name_tmp
                job_name_list.append(job_name_tmp)
                jobs_filter_job_name = jobs_id_jobname_username.filter(job_name=job_name_tmp)
                step_list = []
                script_list = []
                for j in jobs_filter_job_name:
                    if j.step_name not in step_list:
                        step_list.append(j.step_name)
                    if j.script_name not in script_list:
                        script_list.append(j.script_name)
                step_str = ",".join(step_list)
                job_one['steps'] = step_str
                script_str = ",".join(script_list)
                job_one['scripts'] = script_str
                job_dir_list.append(job_one)
        cut_list_return = cut_list(job_dir_list,page_num)
        job_dir_list = cut_list_return[1]
        pages = cut_list_return[0]
    else:
        job_dir_list = []
        pages = 0
    job_dir['list'] = job_dir_list
    job_dir['pages'] = pages
    job_dir['priv'] = priv
    return HttpResponse(json.dumps(job_dir))
    
@login_required
def job_list(request):
    user = request.user
    proj = request.session['proj']
    return render_to_response('job_list.html',{'user':user,'proj':proj})

@login_required
def delete_job(request):
    job_name = request.GET['job_name']
    jobs1 = SqlTools('jobs')
    result = jobs1.del_db('job_name',job_name)
    return HttpResponse(result)

@login_required
def update_jobs(request):
    priv = request.session['priv']
    if priv < 3:
        return HttpResponse('error')
    proj = request.session['proj']
    job_id = request.POST['job_id']
    job_name = request.POST['job_name']
    job_user = request.user.username
    step_id = request.POST['step_id']
    step_name = request.POST['step_name']
    script_id = request.POST['script_id']
    script_name = request.POST['script_name']
    script_user = request.POST['script_user']
    server_group = request.POST['server_group']
    scr_arguments = request.POST['scr_arguments']
    jobs1 = SqlTools('jobs')
    result = jobs1.add_db(job_id,job_name,job_user,step_id,step_name,script_id,script_name,script_user,server_group,scr_arguments,proj)
    if result != False:
        result = True
    return HttpResponse(result)

@login_required
def get_job_names(request):
    proj = request.session['proj']
    jobs1 = SqlTools('jobs')
    job_names = jobs1.get_db('job_name').filter(project=proj)
    name_list = []
    for i in job_names:
        name_list.append(i.job_name)
    name_list = list(set(name_list))
    name_list.sort()
    result = {}
    result['data'] = name_list
    return HttpResponse(json.dumps(result))

@login_required
def get_job_name(request):
    proj = request.session['proj']
    job_name = request.POST['job_name']
    jobs1 = SqlTools('jobs')
    try:
        delflag = request.POST['delflag']
        if delflag == "1":
            #del_result = jobs1.del_db('job_name',job_name)
            del_result = jobs1.get_db('job_name',job_name).filter(project=proj).delete()
    except:
        pass
    result = jobs1.get_db_exact('job_name',job_name)
    if len(result) == 0:
        result = False
    else:
        result = True
    return HttpResponse(result)

@login_required
def update_group(request):
    priv = request.session['priv']
    if priv < 3:
        return HttpResponse('error')
    proj = request.session['proj']
    newgroupname = request.POST['newgroupname']
    ip_check_list = request.POST['ip_check_list']
    ip_list = ip_check_list.split(",")[1:]
    ip_group = SqlTools('ip_group')
    tmp_data = ip_group.get_db_exact('server_group',newgroupname)
    if len(tmp_data) != 0:
        return HttpResponse(False)
    server = SqlTools('server')
    for i in ip_list:
        server_uuid = server.get_db('inter_ip',i)
        #print "1"
        if len(server_uuid) != 1:
            return HttpResponse(False)
        #print "2"
        exter_ip = server_uuid[0].exter_ip
        result = ip_group.add_db(newgroupname,'root_tmp',i,exter_ip,proj)
        if result == False:
            return HttpResponse(False)
    return HttpResponse(True)

@login_required
def get_servers_ip(request):
    result = {}
    proj = request.session['proj']
    try:
        ss_key = request.POST['ss_key']
        ss_word = request.POST['ss_word']
        server_id = SqlTools('server').get_db(ss_key,ss_word,'inter_ip').filter(project=proj)
    except:
        server_id = SqlTools('server').get_db('inter_ip').filter(project=proj)
    server_group = SqlTools('ip_group').get_db('server_group').filter(project=proj)
    server_ip = ''
    for i in server_id:
        server_ip = "%s,%s" % (server_ip,i.inter_ip)
    server_ip = server_ip[1:]
    server_group_ip = []
    for i in server_group:
        group_name = i.server_group
        if re.match(r'^\d',group_name) == None:
            server_group_ip.append(i.server_group)
    server_group_ip = list(set(server_group_ip))
    server_group_ip = ",".join(server_group_ip)
    result['ips'] = server_ip
    result['group'] = server_group_ip
    return HttpResponse(json.dumps(result))

def testpage(request):
    user = request.user
    test_var = "hello world!"
    return render_to_response('testpage.html',{"test_var":test_var,'user':user})

@login_required
def start_job(request):
    #proj_ip = '10.10.30.208'
    priv = request.session['priv']
    if priv < 2:
        return HttpResponse('error')
    proj_ip = request.session['proj_ip']
    proj = request.session['proj']
    job_name = request.GET['job_name']
    jobs = SqlTools('jobs')
    job_list = jobs.filter_db('job_name',job_name,'job_id').filter(project=proj)
    scripts_dir = {}
    for i in job_list:
        one_job_list = []
        one_job_list.append(i.script_name)
        one_job_list.append(i.arguments)
        one_job_list.append(i.server_group)
        scripts_dir[i.job_id] = one_job_list
    scripts_list = sorted(scripts_dir.items(),key=lambda x:x[0])

    result = {}
    code = ''
    ip_group = SqlTools('ip_group')
    rsync_return = commands.getstatusoutput("salt '*' state.sls rsync2")
    scripts_all = []
    for i in scripts_list:
        script_one = {}
        script = i[1][0]
        script_full = '/data/salt/scripts/%s' % script
        script_arg = i[1][1]
        group = i[1][2]
        group_list = group.split(',')
        ip_all = []
        ip_match = ''
        for group_one in group_list:
            ip_get = ip_group.filter_db('server_group',group_one).filter(project=proj)
            for j in ip_get:
                ip_all.append('*%s*' % j.inter_ip)
        ip_all = list(set(ip_all))
        ip_match = " or ".join(ip_all)
        cmd_str = ''
        if script.endswith('.sh'):
            cmd_str = 'sh %s %s' % (script_full,script_arg)
        else:
            cmd_str = 'python %s %s' % (script_full,script_arg)
        cmd = "salt -C '%s' cmd.run '%s'" % (ip_match,cmd_str)
        script_one[script] = cmd
        scripts_all.append(script_one)
    data = {'scripts_list':scripts_all}
    url = 'http://%s:8082/run_scripts/' % proj_ip
    data = urllib.urlencode(data)
    script_result = urllib2.urlopen(url,data)
    scripts_all_return = json.load(script_result)
    result_str = ''
    code_list = []
    for i in scripts_all_return:
        result_cmd = '**%s**\n' % i['script']
        result_cmd = '%ssalt return code: %s \nsalt result: \n%s\n\n' % (result_cmd,i['code'],i['txt'])
        result_str = '%s%s' % (result_str,result_cmd)
        code_list.append(i['code'])
    code = ' '.join(code_list)
    result['result'] = result_str
    
    # ### SAVE TO LOG FILE ###
    # log文件名组成: 14位时间戳 + 16位随机字符
    time_str = time.strftime('%Y%m%d%H%M%S')
    r_rondom = ("%.16f" % random.random())[2:]
    log_name = time_str + r_rondom + ".log"
    file_path = '/var/opslog/joblog/'
    log_file_str = file_path + log_name
    log_file = open(log_file_str,'w')
    log_file.write(result_str)
    log_file.close()
    # ### SAVE TO DB ###
    uuid = time_str + r_rondom
    run_user = request.user.username
    job_log = SqlTools('job_log')
    joblog_savedb = job_log.add_db(uuid,job_name,run_user,code,proj)
    result['ok'] = 'ok'
    return HttpResponse(json.dumps(result))
    
@login_required
def run_job(request):
    priv = request.session['priv']
    if priv == 1:
        return HttpResponse('error')
    user = request.user
    proj = request.session['proj']
    try:
        job_name_get = request.GET['job_name_get']
        jobs = SqlTools('jobs')
        job_list = jobs.get_db_exact('job_name',job_name_get,'job_id')
        job_dir = {}
        step_id = []
        for i in job_list:
            step_id_one = i.step_id
            if step_id_one not in step_id:
                step_id.append(step_id_one)
        step_id.sort()
        job_dir = {}
        step_id_list = []
        for i in step_id:
            step_id_query = job_list.filter(step_id=i)
            step_script_list = []
            for j in step_id_query:
                script_dir = {}
                script_dir['script_name'] = j.script_name
                script_dir['script_user'] = j.script_user
                script_dir['server_group'] = j.server_group
                script_dir['arguments'] = j.arguments
                step_script_list.append(script_dir)
            step_dir = {}
            step_dir['step_name'] = step_id_query[0].step_name
            step_dir['script_id'] = step_script_list
            step_id_list.append(step_dir)
        job_dir['job_name'] = job_name_get
        job_dir['step_id'] = step_id_list
        return render_to_response('run_job.html',{'job_dir':job_dir,'user':user,'proj':proj})
    except:
        return render_to_response('run_job.html',{'user':user,'proj':proj})

@login_required
def run_script(request):
    #proj_ip = '10.10.30.208'
    priv = request.session['priv']
    if priv < 3:
        return HttpResponse('error')
    proj_ip = request.session['proj_ip']
    proj = request.session['proj']
    group_name = request.GET['group_name']
    group_list = group_name.split(',')
    file_name = request.GET['file_name']
    script_name = file_name
    user_name = request.GET['user_name']
    script_arg = request.GET['script_arg']
    file_type = request.GET['file_type']
    file_name = file_name + '.' + file_type
    # file path should be installed and be configed in rsync sls file.
    file_path = '/data/salt/scripts/'
    script_full_name = file_path + file_name
    script_all = []
    script_one = {}
    ip_group = SqlTools('ip_group')
    ip_all = []
    for group_one in group_list:
        ip_get = ip_group.get_db_exact('server_group',group_one)
        for j in ip_get:
            ip_all.append('*%s*' % j.inter_ip)
    ip_all = list(set(ip_all))
    ip_match = " or ".join(ip_all)
    cmd_str = ''
    if file_name.endswith('.sh'):
        cmd_str = 'sh %s %s' % (script_full_name,script_arg)
    else:
        cmd_str = 'python %s %s' % (script_full_name,script_arg)
    script_one['file_name'] = "salt -C '%s' cmd.run '%s'" % (ip_match,cmd_str)
    script_all.append(script_one)
    data = {'scripts_list':script_all}
    url = 'http://%s:8082/run_scripts/' % proj_ip
    data = urllib.urlencode(data)
    script_result = urllib2.urlopen(url,data)
    scripts_all_return = json.load(script_result)
    result_cmd = ''
    code_list = []
    for i in scripts_all_return:
        result_cmd = '**%s**\n' % i['script']
        result_cmd = '%ssalt return code: %s \nsalt result: \n%s' % (result_cmd,i['code'],i['txt'])
        code_list.append(i['code'])
    code = ' '.join(code_list)
    result = {}
    result['result'] = result_cmd
    express_run = SqlTools('express_run')
    time_str = time.strftime('%Y%m%d%H%M%S')
    r_rondom = ("%.16f" % random.random())[2:]
    run_log = time_str + r_rondom
    return_data = express_run.add_db(script_name,user_name,run_log,group_name,script_arg,code,proj)
    result['run_time'] = return_data.run_time.isoformat(' ').split('.')[0]
    result['script_name'] = return_data.script_name
    result['run_user'] = return_data.run_user
    result['run_log'] = str(return_data.run_log)
    result['target'] = return_data.target
    result['argments'] = return_data.argments
    result['status'] = return_data.status
    log_filename = '/var/opslog/joblog/%s%s.log' % (time_str,r_rondom)
    with open(log_filename,'w') as f1:
        f1.write(result_cmd)
    return HttpResponse(json.dumps(result))

@login_required
def get_run_log(request):
    run_log = request.GET['run_log']
    #print run_log
    log_filename = '/var/opslog/joblog/%s.log' % run_log
    log_data = ''
    with open(log_filename,'r') as f1:
        log_data = f1.readlines()
    result = {}
    result['log_data'] = log_data
    return HttpResponse(json.dumps(result))

@login_required
def script_check(request):
    #proj_ip = '10.10.30.208'
    proj_ip = request.session["proj_ip"]
    if proj_ip == 'none':
        return HttpResponse(json.dumps("none"))
    file_name = request.POST.get('file_name', None)
    file_type = request.POST['file_type']
    file_name = "%s.%s" % (file_name,file_type)
    check_result = urllib2.urlopen('http://%s:8082/check_name/?file_name=%s' % (proj_ip,file_name))
    return HttpResponse(check_result)
    #result={}
    #try:
    #    file_name = request.POST.get('file_name', None)
    #    file_type = request.POST['file_type']
    #    file_name = "%s.%s" % (file_name,file_type)
    #    dfile1 = DFile()
    #    res = dfile1.check_name(file_name)
    #    if res == True:
    #        content = dfile1.read_file(file_name)
    #    result["content"] = content
    #    result['status'] = 2
    #except:
    #    result["content"] = "Null"
    #    result['status'] = 1
    #return HttpResponse(json.dumps(result))

@login_required
def get_run_data(request):
    run_data_page = request.GET['run_data_page']
    express_run = SqlTools('express_run')
    proj = request.session['proj']
    if request.user.username == 'root':
        run_data = express_run.get_db('-run_time')
    else:
        run_data = express_run.get_db('project',proj,'-run_time')
    result = {}
    run_list = []
    for i in run_data:
        run_one = {}
        run_one['run_time'] = i.run_time.isoformat(' ').split('+')[0]
        run_one['script_name'] = i.script_name
        run_one['run_user'] = i.run_user
        run_one['run_log'] = i.run_log
        run_one['target'] = i.target
        run_one['argments'] = i.argments
        run_one['status'] = i.status
        run_list.append(run_one)
    run_view_length = 20
    run_result = cut_list2(run_list,run_data_page,run_view_length)
    result['run_data'] = run_result[1]
    result['run_pages'] = run_result[0]
    
    return HttpResponse(json.dumps(result))

@login_required
def get_modify_data(request):
    modify_data_page = request.GET['modify_data_page']
    express_log = SqlTools('express_log')
    proj = request.session['proj']
    if request.user.username == 'root':
        log_data = express_log.get_db('-modify_time')
    else:
        log_data = express_log.get_db('project',proj,'-modify_time')
    result = {}
    log_list = []
    for i in log_data:
        log_one = {}
        log_one['modify_time'] = i.modify_time.isoformat(' ').split('+')[0]
        log_one['script_name'] = i.script_name
        log_one['modify_user'] = i.modify_user
        log_one['flag'] = i.flag
        log_list.append(log_one)
    modify_view_length = 20
    modify_result = cut_list2(log_list,modify_data_page,modify_view_length)
    result['log_data'] = modify_result[1]
    result['log_pages'] = modify_result[0]
    
    return HttpResponse(json.dumps(result))

@login_required
def get_script_history(request):
    result = {}
    run_data_page = request.GET['run_data_page']
    modify_data_page = request.GET['modify_data_page']
    express_log = SqlTools('express_log')
    express_run = SqlTools('express_run')
    
    run_data = express_run.get_db('-run_time')
    log_data = express_log.get_db('-modify_time')
    
    log_list = []
    for i in log_data:
        log_one = {}
        log_one['modify_time'] = i.modify_time.isoformat(' ').split('+')[0]
        log_one['script_name'] = i.script_name
        log_one['modify_user'] = i.modify_user
        log_one['flag'] = i.flag
        log_list.append(log_one)
    modify_view_length = 20
    modify_result = cut_list2(log_list,modify_data_page,modify_view_length)
    result['log_data'] = modify_result[1]
    result['log_pages'] = modify_result[0]
        
    run_list = []
    for i in run_data:
        run_one = {}
        run_one['run_time'] = i.run_time.isoformat(' ').split('+')[0]
        run_one['script_name'] = i.script_name
        run_one['run_user'] = i.run_user
        run_one['run_log'] = i.run_log
        run_one['target'] = i.target
        run_one['argments'] = i.argments
        run_one['status'] = i.status
        run_list.append(run_one)
    run_view_length = 10
    run_result = cut_list2(run_list,run_data_page,run_view_length)
    result['run_data'] = run_result[1]
    result['run_pages'] = run_result[0]
    
    return HttpResponse(json.dumps(result))

@login_required
def script_save(request):
    #proj_ip = '10.10.30.208'
    priv = request.session['priv']
    if priv < 3:
        return HttpResponse(json.dumps('error!'))
    proj_ip = request.session['proj_ip']
    proj = request.session['proj']
    user_name = request.POST['user_name']
    file_name = request.POST.get('file_name', None)
    file_type = request.POST['file_type']
    file_name = "%s.%s" % (file_name,file_type)
    script_txt = request.POST['script_txt']
    data = {'file_name':file_name,'script_txt':script_txt}
    #print 'http://%s:8082/save_script/?file_name=%s&script_txt=%s' % (proj_ip,file_name,script_txt)
    url = 'http://%s:8082/save_script/' % proj_ip
    data = urllib.urlencode(data)
    save_result = urllib2.urlopen(url,data)
    result={}
    if save_result:
        result['status'] = 2
        express_log = SqlTools('express_log')
        db_data = express_log.get_db('script_name',file_name).filter(project=proj)
        if len(db_data) == 0:
            flag = 'create'
        else:
            flag = 'modify'
        log_data = express_log.add_db(file_name,user_name,flag,proj)
        result['modify_time'] = log_data.modify_time.isoformat(' ').split('.')[0]
        result['script_name'] = log_data.script_name
        result['modify_user'] = log_data.modify_user
        result['flag'] = log_data.flag
        #result['project'] = log_data.proj
    else:
        result['status'] = 1
    return HttpResponse(json.dumps(result))
    
    #result={}
    #try:
    #    file_name = request.POST.get('file_name', None)
    #    user_name = request.POST['user_name']
    #    file_type = request.POST['file_type']
    #    script_txt = request.POST['script_txt']
    #    file_name = "%s.%s" % (file_name,file_type)
    #    dfile1 = DFile()
    #    res = dfile1.write_file(file_name,script_txt)
    #    result['status'] = 2
    #    express_log = SqlTools('express_log')
    #    db_data = express_log.get_db_exact('script_name',file_name)
    #    if len(db_data) == 0:
    #        flag = 'create'
    #    else:
    #        flag = 'modify'
    #    log_data = express_log.add_db(file_name,user_name,flag)
    #    result['modify_time'] = log_data.modify_time.isoformat(' ').split('.')[0]
    #    result['script_name'] = log_data.script_name
    #    result['modify_user'] = log_data.modify_user
    #    result['flag'] = log_data.flag
    #except:
    #    result['status'] = 1
    #return HttpResponse(json.dumps(result))

@login_required
def script_file(request):
    user = request.user
    proj = request.session['proj']
    return render_to_response('script_file.html',{'user':user,'proj':proj})

@login_required
def rvs(request):
    user = request.user
    action = request.POST['action']
    table = request.POST["table"]
    db_table = SqlTools(table)
    proj = request.session['proj']
    priv = request.session['priv']
    if priv < 3 and action != "search":
        return HttpResponse('无操作权限!')
    add_proj = request.POST.get('project','')
    
    if user.username == 'root':
        result = db_table.get_db()
    else:
        result = db_table.get_db('project',proj)
        
    if proj != add_proj and user.username != 'root' and action != "search":
        return HttpResponse('禁止的操作;')
    if action == "search":
        ss_key = request.POST["ss_key"]
        ss_word = request.POST["ss_word"]
        #result = db_table.get_db(ss_key,ss_word)
        exec('result = result.filter(%s__contains="%s")' % (ss_key,ss_word))
    
    if action == "update" or action == "add":
        string_tmp = ""
        for k,v in request.POST.items():
            if k != 'update_time' and k != 'enter_time' and k != 'pagel' and k != 'pagen' and k != 'id' and k != 'action' and k != 'table' and k != "ins_id_bak" and k!= "used_times":
                string_tmp = "%s,'%s'" % (string_tmp,v)
        string_tmp = string_tmp[1:]
        #print string_tmp
        try:
            id = request.POST['id']
        except:
            pass
        if action == "update":
            exec("result_tf = db_table.update_db(id,%s)" % string_tmp)
            error_hint = "uuid/instance_id冲突或不存在..."
        if action == "add":
            exec("result_tf = db_table.add_db(%s)" % string_tmp)
            error_hint = "添加失败..."
        if not result_tf:
        #    result = db_table.get_db()
        #else:
            return HttpResponse(error_hint)
       
    if action == "delete":
        id = request.POST['id']
        result_tf = db_table.del_db("id",id)
        #print result_tf
        if not result_tf:
        #    result = db_table.get_db()
        #else:
            return HttpResponse("删除失败...")
    
    if result:
        # 分页Paginator 
        paginator = Paginator(result, 25)
        page = request.GET.get('page')
        try:
            server_data = paginator.page(page)
        except:
            server_data = paginator.page(1)
    
    if table == "server":
        return render_to_response('showserver.html',{"server_data":result,'user':user})
    if table == "dbserver":
        return render_to_response('showdb.html',{"db_all_data":result,'user':user})

@login_required
def showserver(request):
    user = request.user
    db_server = SqlTools("server")
    proj = request.session['proj']
    priv = request.session['priv']
    if user.username != 'root':
        result = db_server.get_db('project',proj)
    else:
        result = db_server.get_db()
    if result:
        
        # 分页Paginator 
        paginator = Paginator(result, 25)
        page = request.GET.get('page')
        try:
            server_data = paginator.page(page)
        except:
            server_data = paginator.page(1)
        
    return render_to_response('showserver.html',{"server_data":result,'user':user,'proj':proj,'priv':priv})

@login_required
def showdb(request):
    '''
    输出数据库信息;
    '''
    user = request.user
    db_dbserver = SqlTools("dbserver")
    proj = request.session['proj']
    priv = request.session['priv']
    if user.username != 'root':
        result = db_dbserver.get_db('project',proj)
    else:
        result = db_dbserver.get_db()
    
    if result:
        # Paginator
        paginator = Paginator(result, 25)
        page = request.GET.get('page')
        try:
            db_p_data = paginator.page(page)
        except:
            db_p_data = paginator.page(1)
    return render_to_response('showdb.html',{"db_all_data":result,'user':user,'proj':proj,'priv':priv})

@login_required
def nav(request):
    user = request.user
    priv = request.session['priv']
    return render_to_response('nav.html',{'user':user,'priv':priv})

@login_required
def index(request):
    user = request.user
    proj = request.session["proj"]
    if user.username == 'root':
        root_flag = '1'
    else:
        root_flag = '0'
    return render_to_response('index.html',{'user':user,'proj':proj,'root_flag':root_flag})

@login_required
def addform(request):
    user = request.user
    proj = request.session['proj']
    priv = request.session['priv']
    return render_to_response('addform.html',{'user':user,'proj':proj,'priv':priv})

@login_required
def homepage(request):
    return render_to_response('homepage.html',{})