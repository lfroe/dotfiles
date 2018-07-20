#!/usr/local/bin/python3
import os
import sys
from subprocess import call

path = "/Users/lukas/Documents/EXT_single"
i = 0
showhelp = False

def printhelp():
    print('arguments:')
    print('  --path\n\tSets the path where the repositories will be cloned to.\n\tDefaults to {}'.format(path))
while i < len(sys.argv):
    arg = sys.argv[i]
    if (arg.endswith('checkout-ext.py') == False):
        if (arg == '--path'):
            i += 1
            path = sys.argv[i]
        elif (arg == '--help'):
            showhelp = True
            printhelp()
    i += 1

repos = ['api-gateway', 'auth-service', 'devopsservice', 'searchservice', 'clearingservice',
         'documentservice', 'ext', 'extUtils', 'form-manager-service',
         'frontend', 'reportingservice', 'eprocservice', 'notify-service',
         'numbergenerator', 'templateengineservice', 'todo-service', 'workflowengine']
if (showhelp == False):
    if os.path.exists(path):
        call(["rm", "-rf", path])
        print("Successfully removed directory")
    for repo in repos:
        clone = "git clone ssh://git@repo.dig.at:5999/ext/{}.git".format(repo)
        print('clone is {}'.format(clone))
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        os.system(clone)
        print ("\nDONE CLONING {}! \n".format(repo))
