from django.db import models

# Create your models here.

class user_priv(models.Model):
    id = models.AutoField(primary_key=True)
    proj = models.CharField(max_length=50)
    user = models.CharField(max_length=20)
    priv = models.SmallIntegerField()
    
    def get_values(self):
        data = {}
        data['proj'] = self.proj
        data['user'] = self.user
        data['priv'] = self.priv
        return data
        
    def get_one_priv(self):
        return self.priv

class game_proj(models.Model):
    id = models.AutoField(primary_key=True)
    proj_name = models.CharField(max_length=50,unique=True)
    proj_ip = models.GenericIPAddressField()
    
    def fields(self):
        return ('proj_name','proj_ip')
        
    def get_values(self):
        data = {}
        data['proj_name'] = self.proj_name
        data['proj_ip'] = self.proj_ip
        return data

class proj_loginfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)
    proj = models.CharField(max_length=50)

    def fields(self):
        return ('user','proj')
        
    def get_values(self):
        data = {}
        data['user'] = self.user
        data['proj'] = self.proj
        return data

class proj_prvi(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20,unique=True)
    proj = models.CharField(max_length=100)

    def fields(self):
        return ('user','proj')
        
    def get_values(self):
        data = {}
        data['user'] = self.user
        data['proj'] = self.proj.split(',')
        return data
    
# not used.
class express_script(models.Model):
    id = models.AutoField(primary_key=True)
    script_name = models.CharField(max_length=50)
    creator = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_user = models.CharField(max_length=20,null=True)
    last_modify_time = models.CharField(max_length=50,null=True)
    run_count = models.SmallIntegerField(default=0)
    last_run_user = models.CharField(max_length=20,null=True)
    last_run_time = models.CharField(max_length=50,null=True)
    last_run_log = models.CharField(max_length=50,null=True)

# not used.
class express_create(models.Model):
    id = models.AutoField(primary_key=True)
    script_name = models.CharField(max_length=50,unique=True)
    creator = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
# not used.
class express_modify(models.Model):
    id = models.AutoField(primary_key=True)
    script_name = models.CharField(max_length=50)
    modify_user = models.CharField(max_length=20)
    modify_time = models.DateTimeField(auto_now_add=True)

class express_log(models.Model):
    id = models.AutoField(primary_key=True)
    script_name = models.CharField(max_length=50)
    modify_user = models.CharField(max_length=20)
    modify_time = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(max_length=20)
    project = models.CharField(max_length=50)

class express_run(models.Model):
    id = models.AutoField(primary_key=True)
    script_name = models.CharField(max_length=50)
    run_user = models.CharField(max_length=20)
    run_time = models.DateTimeField(auto_now_add=True)
    run_log = models.CharField(max_length=50)
    target = models.CharField(max_length=100)
    argments = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    project = models.CharField(max_length=50)

class job_log(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=50,unique=True)
    job_name = models.CharField(max_length=50)
    run_user = models.CharField(max_length=20)
    run_time = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=50)
    project = models.CharField(max_length=50)

class cron_log(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=50,unique=True)
    cron_name = models.CharField(max_length=200)
    run_time = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=50)
    project = models.CharField(max_length=50)

class timed_jobs(models.Model):
    id = models.AutoField(primary_key=True)
    timed_job = models.CharField(max_length=50,unique=True)
#    job_name = models.CharField(max_length=50) from PeriodicTask
#    time_data = models.CharField(max_length=20) from CrontabSchedule
    creater = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20)
    modified_time = models.DateTimeField(auto_now=True)
#    status = models.CharField(max_length=10) from PeriodicTask
    project = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.timed_job

class jobs(models.Model):
    id = models.AutoField(primary_key=True)
    job_id = models.CharField(max_length=20)
    job_name = models.CharField(max_length=50)
    job_user = models.CharField(max_length=20)
    step_id = models.CharField(max_length=20)
    step_name = models.CharField(max_length=50)
    script_id = models.CharField(max_length=20)
    script_name = models.CharField(max_length=50)
    script_user = models.CharField(max_length=20)
    server_group = models.CharField(max_length=50)
    arguments = models.CharField(max_length=50)
    project = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.id

class ip_group(models.Model):
    id = models.AutoField(primary_key=True)
    server_group = models.CharField(max_length=50)
    user = models.CharField(max_length=20)
    inter_ip = models.GenericIPAddressField()
    exter_ip = models.GenericIPAddressField()
    project = models.CharField(max_length=50)

    def __unicode__(self):
        return self.server_group

class server(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=50,unique=True)
    project = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    inter_ip = models.GenericIPAddressField()
    exter_ip = models.GenericIPAddressField()
    srv_type = models.CharField(max_length=20)
    cpu = models.SmallIntegerField()
    memory = models.SmallIntegerField()
    disk_size = models.SmallIntegerField()
    os_type = models.CharField(max_length=20)
    used_times = models.SmallIntegerField(default=0)
    enter_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    subnet = models.CharField(max_length=20)
    
    #def get_model_fields(self):
    #    return self._meta.fields
    
    def __unicode__(self):
        return self.uuid

# backend port pool;
class srv_port(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=50,unique=True)
    game_pt = models.CharField(max_length=50,blank=True)
    game_adm_pt = models.CharField(max_length=50,blank=True)
    battle_pt = models.CharField(max_length=50,blank=True)
    battle_ht_pt = models.CharField(max_length=50,blank=True)
    cache_pt = models.CharField(max_length=50,blank=True)
    cache_ht_pt = models.CharField(max_length=50,blank=True)
    log_pt = models.CharField(max_length=50,blank=True)
    
    def __unicode__(self):
        return self.uuid

class dbserver(models.Model):
    id = models.AutoField(primary_key=True)
    instance_id = models.CharField(max_length=50,unique=True)
    project = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    inter_ip = models.GenericIPAddressField()
    hardware_info = models.CharField(max_length=50)
    port = models.SmallIntegerField()
    db_type = models.CharField(max_length=20)
    used_times = models.SmallIntegerField(default=0)
    enter_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.instance_id

class domain(models.Model):
    id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=100,unique=True)
    project = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    entrance_type = models.CharField(max_length=20)
    entrance_value = models.GenericIPAddressField()
    enter_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.domain_name

class srv_role(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20)
    salt_id = models.CharField(max_length=50)
    srv_name = models.CharField(max_length=20,unique=True)
    sip = models.GenericIPAddressField()
    sid = models.SmallIntegerField()
    sdir = models.CharField(max_length=50)
    sport = models.SmallIntegerField()
    sbattle_port = models.SmallIntegerField()
    sbattle_http_port = models.SmallIntegerField()
    scache_port = models.SmallIntegerField()
    scache_http_port = models.SmallIntegerField()
    slog_port = models.SmallIntegerField()
    slog_archive_time = models.CharField(max_length=20)
    sdb_host = models.GenericIPAddressField()
    sdb_port = models.SmallIntegerField()
    sdb_slave_host = models.GenericIPAddressField()
    sdb_slave_port = models.SmallIntegerField()
    sredis_port = models.SmallIntegerField()
    sopen_time = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.srv_name

#class jobs(models.Model):
#    id = models.AutoField(primary_key=True)
#    job_id = models.CharField(max_length=50, unique=True)
#    catelog = models.CharField(max_length=50)
#    user_id = models.CharField(max_length=20)
#    add_date = models.DateTimeField(auto_now_add=True)
#    action = models.CharField(max_length=20)
#    target = models.CharField(max_length=50)
#    jids = models.CharField(max_length=800)
#    
#    def __unicode__(self):
#        return self.job_id
#
class wdqk_game(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.CharField(max_length=20,unique=True)
    game_ip = models.GenericIPAddressField()
    group = models.CharField(max_length=20)
    game_port = models.SmallIntegerField()
    qu = models.SmallIntegerField()
    fu = models.SmallIntegerField()
    start_time = models.CharField(max_length=20)
    redis_port = models.SmallIntegerField()
    redis_ip = models.GenericIPAddressField()
    db_ip = models.GenericIPAddressField()
    db_user = models.CharField(max_length=20)
    db_passwd = models.CharField(max_length=50)
    battle_port = models.SmallIntegerField()
    battle_http_port = models.SmallIntegerField()
    cache_port = models.SmallIntegerField()
    cache_http_port = models.SmallIntegerField()
    log_port = models.SmallIntegerField()
    redis_key = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.game_id


#class db_list(models.Model):
#    id = models.AutoField(primary_key=True)
#    uuid = models.BigIntegerField()
#    ip = models.GenericIPAddressField()
#    type = models.CharField(max_length=20)
#    port = models.SmallIntegerField()
#    times = models.SmallIntegerField(default=0)
#
#    def __unicode__(self):
#        return self.uuid
