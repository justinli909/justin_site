#coding=utf-8

from ops1.update.sqltools import SqlTools

class Job:

    _job_db = SqlTools('jobs')
    _job_log = SqlTools('job_log')
    _crontabschedule = SqlTools('crontabschedule')
    _periodictask = SqlTools('periodictask')
    _timed_jobs = SqlTools('timed_jobs')
    
    def __init__(self,job_name):
        self.job_name = job_name
        
    def save_to_db(self,job_id,job_user,step_id,step_name,script_id,script_name,script_user,server_group,arguments):
        result = _job_db.add_db(job_id,self.job_name,job_user,step_id,step_name,script_id,script_name,script_user,server_group,scr_arguments)
        if result != False:
            result = True
        return result
        
    def del_from_db(self):
        result = _job_db.del_db('job_name',self.job_name)
        return result
    
    def start(self,run_user):
        job_name = self.job_name
        
        job_list = _job_db.get_db_exact('job_name',job_name,'job_id')
        scripts_dir = {}
        for i in job_list:
            one_job_list = []
            one_job_list.append(i.script_name)
            one_job_list.append(i.arguments)
            one_job_list.append(i.server_group)
            scripts_dir[i.job_id] = one_job_list
        scripts_list = sorted(scripts_dir.items(),key=lambda x:x[0])
    
        result = {}
        result_str = ''
        code = ''
        ip_group = SqlTools('ip_group')
        rsync_return = commands.getstatusoutput("salt '*' state.sls rsync")
        for i in scripts_list:
            script = i[1][0]
            result_cmd = '**%s**\n' % script
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
            cmd_return = commands.getstatusoutput("salt -C '%s' cmd.run '%s'" % (ip_match,cmd_str))
            result_cmd = '%ssalt return code: %s \nsalt result: \n%s\n\n' % (result_cmd,cmd_return[0],cmd_return[1])
            code = code + str(cmd_return[0]) + ' '
            result_str = '%s%s' % (result_str,result_cmd)
            
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
        joblog_savedb = _job_log.add_db(uuid,job_name,run_user,code)
        result['ok'] = 'ok'
        
        return result
    
    def history(self):
        job_name = self.job_name
        result_get = _job_log.get_db_exact('job_name',job_name,'-run_time')
        data = []
        for i in result_get:
            data_one = {}
            data_one['run_time'] = i.run_time.isoformat(' ').split('+')[0]
            data_one['uuid'] = i.uuid
            data_one['run_user'] = i.run_user
            data_one['code'] = i.code
            data.append(data_one)
        return data
        
    def make_cron(self,creater,cron_data,timed_job_name,mdy_username):
        assert type(cron_data) is list
        job_name = self.job_name
        cron_args = '["%s","%s"]' % (job_name,timed_job_name)
        cron_add = self._crontabschedule.add_db(cron_data[0],cron_data[1],cron_data[2],cron_data[3],cron_data[4])
        cron_add_id = int(cron_add.id)
        enable_task = 1
        if cron_add:
            periodic_task_add = self._periodictask.add_db(timed_job_name,'ops1.tasks.start_one_job',cron_add_id,cron_args,'{}',enable_task)
        if periodic_task_add:
            add_result = _timed_jobs.add_db(timed_job_name,creater,mdy_username)
        if not add_result:
            result['return'] = False
        return result
        
class Cron:

    _crontabschedule = SqlTools('crontabschedule')
    _periodictask = SqlTools('periodictask')
    _timed_jobs = SqlTools('timed_jobs')
    _cron_log = SqlTools('cron_log')
    
    def __init__(self,cron_name):
        self.cron_name = cron_name

    def update(self,cron_data,job_name,mdy_username):
        assert type(cron_data) is list
        timed_job_name = self.cron_name
        cron_args = '["%s","%s"]' % (job_name,timed_job_name)
        get_data = _timed_jobs.get_db_exact('timed_job',timed_job_name)[0]
        get_periodictask_data = self._periodictask.get_db_exact('name',timed_job_name)[0]
        get_crontab_id = get_periodictask_data.crontab_id
        enable_task = get_periodictask_data.enabled
        if enable_task:
            enable_task = 1
        else:
            enable_task = 0
        update_periodictask_id = get_periodictask_data.id
        update_crontab_return = self._crontabschedule.update_db(get_crontab_id,cron_data[0],cron_data[1],cron_data[2],cron_data[3],cron_data[4])
        if update_crontab_return:
            update_periodictask_return = self._periodictask.update_db(update_periodictask_id,timed_job_name,'ops1.tasks.start_one_job',get_crontab_id,cron_args,'{}',enable_task)
        if update_periodictask_return:
            try:
                get_data.modified_by = mdy_username
                get_data.save()
            except:
                result['return'] = False
        return result
        
    def query(self):
        timed_job_name = self.cron_name
        periodic_task_final = self._periodictask.get_db_exact('name',timed_job_name)[0]
        crontab_id = periodic_task_final.crontab_id
        crontab_final = self._crontabschedule.get_db_exact('id',crontab_id)[0]
        timed_job_final = _timed_jobs.get_db_exact('timed_job',timed_job_name)[0]
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
        return result
    
    def change_status(self):
        timed_job_name = self.cron_name
        periodictask_data = self._periodictask.get_db_exact('name',timed_job_name)[0]
        timed_job_status = periodictask_data.enabled
        if timed_job_status:
            try:
                periodictask_data.enabled = 0
                periodictask_data.save()
            except:
                return False
        else:
            try:
                periodictask_data.enabled = 1
                periodictask_data.save()
            except:
                return False
        return True
        
    def delete(self):
        timed_job_name = self.cron_name
        crontab_id = self._periodictask.get_db_exact('name',timed_job_name)[0].crontab_id
        timed_del_return = _timed_jobs.del_db('timed_job',timed_job_name)
        if timed_del_return:
            periodictask_del_return = self._periodictask.del_db('name',timed_job_name)
        if periodictask_del_return:
            crontab_del_return = self._crontabschedule.del_db('id',crontab_id)
        return crontab_del_return
    
    def history(self):
        cron_name = self.cron_name
        result_get = _cron_log.get_db_exact('cron_name',cron_name,'-run_time')
        data = []
        for i in result_get:
            data_one = {}
            data_one['run_time'] = i.run_time.isoformat(' ').split('+')[0]
            data_one['uuid'] = i.uuid
            data_one['code'] = i.code
            data.append(data_one)
        return data
