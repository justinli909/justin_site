from kombu import Queue, Exchange

BROKER_URL = 'amqp://rabbit1226:A7+:VYl7kS^pOE5Qc@10.10.30.207:5672/myvhost'
#BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'redis://:A7+:VYl7kS^pOE5Qc@10.10.30.207:6379/0'
#CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#CELERY_RESULT_BACKEND = 'db+mysql://root:l0ck@CC@10.10.30.111/django1'

#CELERY_QUEUES = (
#    Queue('s171',exchange=Exchange('s171task',type='direct'),routing_key='tasks.test1'),
#    Queue('s208',exchange=Exchange('s208task',type='direct'),routing_key='tasks.test2'),
#    Queue('s207',exchange=Exchange('s207task',type='direct'),routing_key='s207'),
#)
#CELERY_ROUTES = {
#    'ops1.tasks.test1':{
#        'queue':'s171',
##        'routing_key':'ops1.tasks.test1',
#    },
#    'ops1.tasks.test2':{
#        'queue':'s208',
##        'routing_key':'ops1.tasks.test2',
#    },
#    'ops1.tasks.test3':{
#        'queue':'s207',
#        'routing_key':'s207',
#    },
#    'ops1.tasks.test4':{
#        'queue':'s207',
#        'routing_key':'s207',
#    },
#    'ops1.tasks.run_cmd_101030207':{
#        'queue':'s207',
#        'routing_key':'s207',
#    },
#    'ops1.tasks.start_one_job':{
#        'queue':'s207',
#        'routing_key':'s207',
#    },
#    'ops1.tasks.express_save_101030207':{
#        'queue':'s207',
#        'routing_key':'s207',
#    },
#    'ops1.tasks.express_check_101030207':{
#        'queue':'s207',
#        'routing_key':'s207',
#    },
#}
