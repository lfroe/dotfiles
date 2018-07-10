#!/usr/local/bin/python3
import os
from subprocess import call

path  = "/Users/lukas/Documents/EXT_single"

repos = ['api-gateway', 'auth-service', 'devopsservice', 'searchservice',
		 'documentservice', 'ext', 'extUtils', 'form-manager-service',
		 'frontend', 'reportingservice', 'eprocservice', 'notify-service',
		 'numbergenerator', 'templateengineservice', 'todo-service', 'workflowengine']
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
	print ("\n DONE CLONING {}! \n".format(repo))
