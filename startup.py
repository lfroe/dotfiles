#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import subprocess
import sys
import os

rmq_base_dir        ='/usr/local/sbin'
tomcat_base_dir     ='/Library/Tomcat/bin'
base_dir            ='~/projects/ext'
admin_mongo_base_dir='/Users/lukas/bin/adminMongo'
langdir             ='/data1/ext/lang'

setupService = {
    'mongo'     : {
        'cmd': 'ttab -t \'mongo\' sudo mongod --config /etc/mongod.conf',
        'name': 'mongo'
    },
    'rmq'       : {
        'cmd': 'tab -t \'rabbitmq\' {}/rabbitmq-server'.format(rmq_base_dir),
        'name': 'rmq'
    },
    'elastic'   : {
        'cmd': 'tab -t \'elastic\' elastic',
        'name': 'elastic'
    },
    'tomcat'    : {
        'cmd': 'tab -t \'tomcat\' {}/startup.sh'.format(tomcat_base_dir),
        'name': 'tomcat'
    },
    'cerebro'   : {
        'cmd': 'tab -t \'cerebro\' cerebro',
        'name': 'cerebro'
    },
    'adminmongo': {
        'cmd': 'tab -t \'adminMongo\' \'cd {0} && npm start\''.format(admin_mongo_base_dir),
        'name': 'adminmongo'
    }
}
services = {
    'c'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'ext'),
        'name': 'extBackend'
    },
    'a'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'auth-service'),
        'name': 'auth-service'
    },
    'f'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'form-manager-service'),
        'name': 'form-manager-service'
    },
    'g'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'api-gateway'),
        'name': 'api-gateway'
    },
    'b'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'vendormanagement'),
        'name': 'vendormanagement'
    },
    'w'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'workflowengine'),
        'name': 'workflowengine'
    },
    't'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'todo-service'),
        'name': 'todoservice'
    },
    'n'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'numbergenerator'),
        'name': 'numbergenerator'
    },
    'd'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'documentservice'),
        'name': 'documentservice'
    },
    'e'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'eprocservice'),
        'name': 'eprocservice'
    },
    'o'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'devopsservice'),
        'name': 'devopsservice'
    },
    'v'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'templateengineservice'),
        'name': 'templateengineservice'
    },
    'r'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'reportingservice'),
        'name': 'reportingservice'
    },
    'm'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'catman-service'),
        'name': 'catmanservice'
    },
    's'         : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'clearingservice'),
        'name': 'clearingservice'
    },
    'sr'        : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'searchservice'),
        'name': 'searchservice'
    },
    'no'        : {
        'cmd': 'ttab -t \'{1}\' \'cd {0}/{1} && ./gradlew bootRun\''.format(base_dir, 'notify-service'),
        'name': 'notifyservice'
    },
    'mongo'     : {
        'cmd': 'ttab -t \'mongo\' sudo mongod --config /etc/mongod.conf',
        'name': 'mongo'
    },
    'rmq'       : {
        'cmd': 'tab -t \'rabbitmq\' {}/rabbitmq-server'.format(rmq_base_dir),
        'name': 'rmq'
    },
    'elastic'   : {
        'cmd': 'tab -t \'elastic\' elastic',
        'name': 'elastic'
    },
    'tomcat'    : {
        'cmd': 'tab -t \'tomcat\' {}/startup.sh'.format(tomcat_base_dir),
        'name': 'tomcat'
    },
    'cerebro'   : {
        'cmd': 'tab -t \'cerebro\' cerebro',
        'name': 'cerebro'
    },
    'adminmongo': {
        'cmd': 'tab -t \'adminMongo\' \'cd {0} && npm start\''.format(admin_mongo_base_dir),
        'name': 'adminmongo'
    }
}
def printhelp():
    print('arguments:')
    print('  --info\n\tLists all available services')
    print('  --setup\n\t Starts all setup services')
    print('  --base-dir <<dir>>\n\tSet the directory where the services are located.\n\tDefaults to {}'.format(base_dir))
    print('  --tomcat-base-dir <<dir>>\n\tSet the directory where tomcat startup script is located.\n\tDefaults to {}'.format(tomcat_base_dir))
    print('  --rmq-base-dir <<dir>>\n\tSet the directory where the rabbitmq startup script is located.\n\tDefaults to {}'.format(rmq_base_dir))
    print('  --adminmongo-base-dir <<dir>>\n\tSet the directory where the adminMongo startup script is located.\n\tDefaults to {}'.format(admin_mongo_base_dir))
    print('  --lang-dig <<dir>>\n\tSet the directory where the language files are located.\n\tDefaults to {}'.format(langdir))
i = 0
while i < len(sys.argv):
    arg = sys.argv[i]
    if (arg.endswith('startup.py') != True):
        if (arg == '--info'):
            for service, cmd in services.items():
                print('{0: <12}: {1}'.format(service, cmd['name']))
        elif (arg == '--setup'):
            for service, cmd in setupService.items():
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
        else:
            if (arg == 'c'):
                if not os.path.exists(langdir):
                    os.makedirs(langdir)
            cmd = services.get(arg)['cmd']
            subprocess.check_call(cmd, shell=True)
    i += 1
