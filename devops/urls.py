from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, logout_then_login
from ops1.views import index, addform, nav, showserver, showdb, testpage, rvs, script_file, script_save, script_check, run_job, get_servers_ip, update_group, get_job_name, update_jobs, job_list, get_job, interactive_shell, timing_job, save_timed_jobs, query_jobs, del_timed_job, get_job_names, start_job, change_status, delete_job, get_job_history, get_jog_log, get_cron_history, get_cron_log, run_script, get_script_history, get_run_log, get_run_data, get_modify_data, login_view, success, register, invalid, r_success, proj_admin, get_proj_data, create_proj, assign_user_proj, del_prvi, get_proj_priv, get_proj_name, get_script_names, update_proj, del_game_proj,update_priv, priv_del, homepage, create_user, stop_user, start_user, delete_user, change_passwd, changepasswd

#from s208_2.ops.views import check_name,save_script,run_scripts
# s208 is from 208 server nfs, this make 207 as a remote server;

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'devops.views.home', name='home'),
    # url(r'^devops/', include('devops.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    #(r'^admin/', include(admin.site.urls)),
    (r'^$',index),
    (r'^homepage/$',homepage),
    (r'^testpage/$',testpage),
    (r'^addform/$',addform),
    (r'^nav/$',nav),
    (r'^showserver/$',showserver),
    (r'^showdb/$',showdb),
    (r'^rvs/$',rvs),
    (r'^script_file/$',script_file),
    (r'^script_save/$',script_save),
    (r'^script_check/$',script_check),
    (r'^run_job/$',run_job),
    (r'^get_servers_ip/$',get_servers_ip),
    (r'^update_group/$',update_group),
    (r'^get_job_name/$',get_job_name),
    (r'^update_jobs/$',update_jobs),
    (r'^job_list/$',job_list),
    (r'^get_job/$',get_job),
    #(r'^interactive_shell/$',interactive_shell),
    (r'^timing_job/$',timing_job),
    (r'^save_timed_jobs/$',save_timed_jobs),
    (r'^query_jobs/$',query_jobs),
    (r'^del_timed_job/$',del_timed_job),
    (r'^get_job_names/$',get_job_names),
    (r'^start_job/$',start_job),
    (r'^change_status/$',change_status),
    (r'^delete_job/$',delete_job),
    (r'^get_job_history/$',get_job_history),
    (r'^get_jog_log/$',get_jog_log),
    (r'^get_cron_history/$',get_cron_history),
    (r'^get_cron_log/$',get_cron_log),
    (r'^run_script/$',run_script),
    #(r'^get_script_history/$',get_script_history),
    (r'^get_run_log/$',get_run_log),
    (r'^get_run_data/$',get_run_data),
    (r'^get_modify_data/$',get_modify_data),
    (r'^login/$',login),
    (r'^accounts/login/$',login),
    (r'^login_view/$',login_view),
    (r'^success/$',success),
    #(r'^register/$',register),
    (r'^invalid/$',invalid),
    (r'^r_success/$',r_success),
    (r'^logout/$', logout_then_login),
    (r'^logout_then_login/$', logout_then_login),
    (r'^proj_admin/$', proj_admin),
    (r'^get_proj_data/$', get_proj_data),
    (r'^create_proj/$', create_proj),
    (r'^assign_user_proj/$', assign_user_proj),
    #(r'^check_proj/$', check_proj),
    #(r'^check_proj_del/$', check_proj_del),
    (r'^del_prvi/$', del_prvi),
    (r'^get_proj_priv/$', get_proj_priv),
    (r'^get_proj_name/$', get_proj_name),
    # distribute url:
    #(r'^check_name/$', check_name),
    #(r'^save_script/$', save_script),
    #(r'run_scripts', run_scripts),
    (r'^get_script_names/$', get_script_names),
    (r'^update_proj/$', update_proj),
    (r'^del_game_proj/$', del_game_proj),
    (r'^update_priv/$', update_priv),
    (r'^priv_del/$', priv_del),
    (r'^create_user/$', create_user),
    (r'^stop_user/$', stop_user),
    (r'^start_user/$', start_user),
    (r'^delete_user/$', delete_user),
    (r'^change_passwd/$', change_passwd),
    (r'^changepasswd/$', changepasswd),
)
