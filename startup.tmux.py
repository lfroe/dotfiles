#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import subprocess
import sys
import os
import signal

rmq_base_dir        ='/usr/local/sbin'
tomcat_base_dir     ='/Library/Tomcat/bin'
base_dir            ='~/Documents/EXT'
admin_mongo_base_dir='/Users/lukas/bin/adminMongo'
langdir             ='/data1/ext/lang'
gradle_task         ='bootRun'
session_name        ='ext'

setupService = {
    'mongo'     : {
        'cmd': 'sudo mongod --config /etc/mongod.conf',
        'name': 'mongo'
    },
    'rmq'       : {
        'cmd': '{}/rabbitmq-server'.format(rmq_base_dir),
        'name': 'rmq'
    },
    'elastic'   : {
        'cmd': 'elastic',
        'name': 'elastic'
    },
    'tomcat'    : {
        'cmd': '{}/startup.sh'.format(tomcat_base_dir),
        'name': 'tomcat'
    },
    'cerebro'   : {
        'cmd': 'cerebro',
        'name': 'cerebro'
    },
    'adminmongo': {
        'cmd': 'cd {0} && npm start'.format(admin_mongo_base_dir),
        'name': 'adminmongo'
    }
}
defaultServices = {
    'c', 'a', 't', 'w', 'f', 'd', 'v', 's', 'sr', 'e'
}
services = {
    'c'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'extBackend'),
        'name': 'extBackend'
    },
    'a'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'auth-service'),
        'name': 'auth-service'
    },
    'f'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'form-manager-service'),
        'name': 'form-manager-service'
    },
    'g'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'api-gateway'),
        'name': 'api-gateway'
    },
    'b'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'vendormanagement'),
        'name': 'vendormanagement'
    },
    'w'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'workflowengine'),
        'name': 'workflowengine'
    },
    't'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'todo-service'),
        'name': 'todoservice'
    },
    'n'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'numbergenerator'),
        'name': 'numbergenerator'
    },
    'd'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'documentservice'),
        'name': 'documentservice'
    },
    'e'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'eprocservice'),
        'name': 'eprocservice'
    },
    'o'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'devopsservice'),
        'name': 'devopsservice'
    },
    'v'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'templateengineservice'),
        'name': 'templateengineservice'
    },
    'r'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'reportingservice'),
        'name': 'reportingservice'
    },
    'm'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'catman-service'),
        'name': 'catmanservice'
    },
    's'         : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'clearingservice'),
        'name': 'clearingservice'
    },
    'sr'        : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'searchservice'),
        'name': 'searchservice'
    },
    'no'        : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'notify-service'),
        'name': 'notifyservice'
    },
    'ct'        : {
        'cmd': 'cd {0}/{1} && ./gradlew'.format(base_dir, 'codetabservice'),
        'name': 'codetabservice'
    },
    'mongo'     : {
        'cmd': 'sudo mongod --config /etc/mongod.conf',
        'name': 'mongo'
    },
    'rmq'       : {
        'cmd': '{}/rabbitmq-server'.format(rmq_base_dir),
        'name': 'rmq'
    },
    'elastic'   : {
        'cmd': 'elastic',
        'name': 'elastic'
    },
    'tomcat'    : {
        'cmd': '{}/startup.sh'.format(tomcat_base_dir),
        'name': 'tomcat'
    },
    'cerebro'   : {
        'cmd': 'cerebro',
        'name': 'cerebro'
    },
    'adminmongo': {
        'cmd': 'cd {0} && npm start'.format(admin_mongo_base_dir),
        'name': 'adminmongo'
    }
}
def new_tab(cmd, tabname):
    finalcmd = 'tmux new-window -a -t {2} -n {0} && tmux send-keys -t {2}:{0} \'{1}\' Enter'.format(tabname, cmd, session_name)
    return finalcmd
def printhelp():
    print('arguments:')
    print('  --info\n\tLists all available services')
    print('  --setup\n\t Starts all setup services')
    print('  --kill-them-all\n\t Kills all running microservice (non-setup) processes')
    print('  --base-dir <<dir>>\n\tSet the directory where the services are located.\n\tDefaults to {}'.format(base_dir))
    print('  --tomcat-base-dir <<dir>>\n\tSet the directory where tomcat startup script is located.\n\tDefaults to {}'.format(tomcat_base_dir))
    print('  --rmq-base-dir <<dir>>\n\tSet the directory where the rabbitmq startup script is located.\n\tDefaults to {}'.format(rmq_base_dir))
    print('  --adminmongo-base-dir <<dir>>\n\tSet the directory where the adminMongo startup script is located.\n\tDefaults to {}'.format(admin_mongo_base_dir))
    print('  --lang-dig <<dir>>\n\tSet the directory where the language files are located.\n\tDefaults to {}'.format(langdir))
    print('  --test\n\tSets the script to test-mode. It will then execute the gradle task \'test\''.format(langdir))
i = 0
args = []
while i < len(sys.argv):
    arg = sys.argv[i]
    if (arg.endswith('startup.tmux.py') == False):
        if (arg.startswith('--session-name')):
            session_name_arr = arg.split('=')
            if len(session_name_arr) == 2:
                session_name = session_name_arr[1]
        elif (arg == '--stop'):
            i += 1
            session_name = sys.argv[i]
    i += 1
try:
    print('checking if session {} already exists'.format(session_name))
    subprocess.check_call('tmux has-session -t {}'.format(session_name), shell=True)
    print("found session. nothing to do here...")
except:
    print("session {} not found. creating...".format(session_name))
    subprocess.check_call('tmux new -s {} -d'.format(session_name), shell=True)

i = 0
while i < len(sys.argv):
    arg = sys.argv[i]
    if (arg.endswith('startup.tmux.py') != True):
        if (arg == '--info'):
            for service, cmd in services.items():
                print('{0: <12}: {1}'.format(service, cmd['name']))
        elif (arg == '--test'):
            gradle_task = 'test'
        elif (arg == '--setup'):
            for key, val in setupService.items():
                cmd = new_tab(val['cmd'], val['name'])
                subprocess.check_call(cmd, shell=True)
        elif (arg == '--default'):
            for servicename in defaultServices:
                for key, val in services.items():
                    if (servicename == key):
                        cmd = services.get(servicename)['cmd']
                        subprocess.check_call(cmd, shell=True)
        elif (arg == '--help'):
            printhelp()
        elif (arg == '--base-dir'):
            i += 1
            base_dir = sys.argv[i]
        elif (arg == '--tomcat-base-dir'):
            i += 1
            tomcat_base_dir = sys.argv[i]
        elif (arg == '--rmq-base-dir'):
            i += 1
            rmq_base_dir = sys.argv[i]
        elif (arg == '--adminmongo-base-dir'):
            i += 1
            admin_mongo_base_dir = sys.argv[i]
        elif (arg == '--lang-dir'):
            i += 1
            langdir = sys.argv[i]
        elif (arg == '--stop'):
            i += 1
            session_name = sys.argv[i]
            windows = subprocess.check_output('tmux ls | grep {} | cut -d \':\' -f 2 | cut -f 2 -d \' \''.format(session_name), shell=True)
            windows = str(windows).replace('b\'', '').replace('\\n\'', '')
            j=1
            while j < int(windows):
                try:
                    subprocess.check_call('tmux send-keys -t {}:{} C-c'.format(session_name, j), shell=True)
                except:
                    print('Couldn\'t find window#{}'.format(j))
                j += 1
            subprocess.check_call('tmux kill-session -t {}'.format(session_name), shell=True)
        elif (arg.startswith('--session-name') == False):
            if (arg == 'c'):
                if not os.path.exists(langdir):
                    os.makedirs(langdir)
            val = services.get(arg)
            cmd = new_tab('{} {}'.format(val['cmd'], gradle_task), val['name'])
            subprocess.check_call(cmd, shell=True)
    i += 1
