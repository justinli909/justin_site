from celery import task
from ops1.update.sqltools import SqlTools
import os, commands, time, random, urllib, urllib2, json

@task()
def run_update(cmd_str):
    # !!! this code block is obsoleted and just for testing purpose. !!!
    #cmd_list = []
    #cmd_list.append(cmd_str)
    #print cmd_list
    for i in range(10):
        print i
        os.system("salt '*208*' cmd.run 'date >> 1.txt'")
    #salt_local.cmd('*208*','cmd.run',cmd_list)
    
@task
def start_one_job(job_name,cron_name,proj_ip,proj):
    #proj_ip = '10.10.30.208'
    jobs = SqlTools('jobs')
    job_list = jobs.get_db_exact('job_name',job_name,'job_id')
    scripts_dir = {}
    for i in job_list:
        one_job_list = []
        one_job_list.append(i.script_name)
        one_job_list.append(i.arguments)
        one_job_list.append(i.server_group)
        scripts_dir[i.job_id] = one_job_list
    scripts_list = sorted(scripts_dir.items(),key=lambda x:x[0])

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
            ip_get = ip_group.get_db_exact('server_group',group_one)
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
        
    # ### SAVE TO LOG FILE ###
    # log file name: 14 timestamp + 16 random string;
    time_str = time.strftime('%Y%m%d%H%M%S')
    r_rondom = ("%.16f" % random.random())[2:]
    log_name = time_str + r_rondom + ".log"
    # 'path' should be installed in installation scripts:
    file_path = '/var/opslog/cronlog/'
    log_file_str = file_path + log_name
    log_file = open(log_file_str,'w')
    log_file.write(result_str)
    log_file.close()
    
    # ### SAVE TO DB ###
    uuid = time_str + r_rondom
    cron_log = SqlTools('cron_log')
    cronlog_savedb = cron_log.add_db(uuid,cron_name,code,proj)
