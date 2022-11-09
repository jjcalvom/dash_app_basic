#!/usr/bin/env python
'''
INTEL CONFIDENTIAL.  Copyright (c) 2021 Intel Corporation.

All rights reserved.
----------------------------------------------------------------------------

Brief:
    cf_manager.py - Script to manage Cloud Foundry App Deployment

----------------------------------------------------------------------------
2020.11.12        padillar - Initial Creation
2021.11.02        padillar - Simplify script for use of WANDA project
'''

import cf_env

import os
import subprocess
import sys
from sys import exit
from sys import version_info
from re import search
import argparse
import time
import getpass

DEBUG = False
CF_CLI = 'cf'
MIN_PYTHON_VERSION = {"major": 3, "minor": 6}

def verify_python_version():
    print("Python version detected: %s" % str(version_info.major) + "." + str(version_info.minor), flush=True)
    if version_info.major < MIN_PYTHON_VERSION["major"]:
        exit("Python %s.%s or later is required.\n" % (MIN_PYTHON_VERSION["major"], MIN_PYTHON_VERSION["minor"]))
    elif (version_info.major == MIN_PYTHON_VERSION["major"]) and (version_info.minor < MIN_PYTHON_VERSION["minor"]):
        exit("Python %s.%s or later is required.\n" % (MIN_PYTHON_VERSION["major"], MIN_PYTHON_VERSION["minor"]))

def cf_login(cf_space):
    print("Enter cf_login")
    # Run cf command to get CLI version info
    cmd = '--version'
    run_cf_cmd(cmd)
    ucred = input("Enter your Intel email address: ")
    pcred = getpass.getpass()
    # Run cf command to login
    cmd = 'login -a ' + cf_env.CF_ENTRYPOINT + ' -u ' + ucred + ' -p ' + pcred + ' -o ' + cf_env.CF_ORG + ' -s ' + cf_space
    run_cf_cmd(cmd)

def cf_logout():
    cmd = 'logout'
    run_cf_cmd(cmd)

def cf_push(app_name, mem=cf_env.CF_PROD_MEM, disk=cf_env.CF_PROD_DISK):
    # Note: CLI parameters take precedence over manifest
    cmd = 'push ' + app_name + ' --no-start -m ' + mem + ' -k ' + disk + ' -f ' + cf_env.CF_MANIFEST
    run_cf_cmd(cmd)
    cmd = 'set-env ' + app_name + ' CF_APPNAME ' + app_name
    run_cf_cmd(cmd)
    cmd = 'set-env ' + app_name + ' CF_USERNAME ' + str(cf_env.CF_USERNAME)
    run_cf_cmd(cmd)
    cmd = 'set-env ' + app_name + ' CF_PASSWORD ' + str(cf_env.CF_PASSWORD)
    run_cf_cmd(cmd)

def cf_start(app_name, check_err=True):
    cmd = 'start ' + app_name
    run_cf_cmd(cmd)

def cf_stop(app_name, check_err=True):
    cmd = 'stop ' + app_name
    run_cf_cmd(cmd, check_err)

def cf_delete(app_name, check_err=True):
    cmd = 'delete -f -r ' + app_name
    run_cf_cmd(cmd, check_err)

def cf_create_smb_service(app_name, check_err=True):
    print("skip create smb service")
    #cmd = 'create-service smb Existing ' + cf_env.CF_SMB_NAME + ' -c ' + cf_env.CF_SMB_SHARE
    #run_cf_cmd(cmd, check_err)

def cf_delete_smb_service(app_name, check_err=True):
    print("skip delete smb service")
    #cmd = 'delete-service ' + cf_env.CF_SMB_NAME + ' -f'
    #run_cf_cmd(cmd, check_err)

def cf_bind_smb_service(app_name, check_err=True):
    print("skip bind smb service")
    #ucred = cf_env.CF_USR
    #pcred = cf_pwd.fetch_password(cf_env.CF_PWD_FILE)
    #bind_json = '\"{\\\"username\\\":\\\"' + ucred + '\\\",' + '\\\"password\\\":\\\"' + pcred + '\\\",' + '\\\"mount\\\":\\\"' + "/var/vcap/sod-data" + '\\\"}\"'
    #cmd = 'bind-service ' + app_name + ' ' + cf_env.CF_SMB_NAME + ' -c ' + bind_json
    #run_cf_cmd(cmd)

def cf_unbind_smb_service(app_name, check_err=True):
    print("skip unbind smb service")
    #cmd = 'unbind-service ' + app_name + ' ' + cf_env.CF_SMB_NAME
    #run_cf_cmd(cmd, check_err)

def cf_running_apps():
    apps_list = []
    cf_cmd = CF_CLI + ' apps'
    if(DEBUG): print('cmd >>> ' + cf_cmd, flush=True)
    cmd_pipe = subprocess.Popen(cf_cmd, shell = True, stdin = None, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    t_out, error = cmd_pipe.communicate()
    output = t_out.decode("utf-8")
    print(output, flush=True)
    if cmd_pipe.returncode != 0:
        print("\nCF command failed: " + str(error), flush=True)
        exit(4)
    for line in output.splitlines():
        if(DEBUG): print(line.rstrip())
        if search(cf_env.CF_DOMAIN, line):
            app = line.split(' ')[0]
            if(DEBUG): print("Found running app: " + app, flush=True)
            apps_list.append(app)
    time.sleep(3)
    return apps_list

def cf_deploy_prod_blue_green():
    # https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html
    print("Pushing app to Production space using blue-green deployment", flush=True)
    cf_login(cf_env.CF_SPACE_PROD)
    apps_list = cf_running_apps()
    # Check a production app is already running, otherwise abort
    blue_app_name = cf_env.CF_APP_NAME
    if blue_app_name not in apps_list:
        print("\nDid not find a production app running!", flush=True)
        exit(5)
    cf_create_smb_service(blue_app_name)
    # Delete any old Green app and push new Green app
    green_app_name = cf_env.CF_APP_NAME + '-Green'
    check_err = False
    if green_app_name in apps_list:
        cf_stop(green_app_name, check_err)
        cf_delete(green_app_name)
    cf_push(green_app_name, cf_env.CF_PROD_MEM, cf_env.CF_PROD_DISK)
    cf_bind_smb_service(green_app_name)
    cf_start(green_app_name)
    # Map production route to Green app
    cmd = 'map-route ' + green_app_name + ' ' + cf_env.CF_DOMAIN + ' -n ' + blue_app_name
    run_cf_cmd(cmd)
    # Unmap production route to Blue
    cmd = 'unmap-route ' + blue_app_name + ' ' + cf_env.CF_DOMAIN + ' -n ' + blue_app_name
    run_cf_cmd(cmd)
    # Remove temporary route to Green
    cmd = 'unmap-route ' + green_app_name + ' ' + cf_env.CF_DOMAIN + ' -n ' + green_app_name
    run_cf_cmd(cmd)
    # Stop and delete Blue app
    cf_stop(blue_app_name)
    cf_delete(blue_app_name)
    # Rename Green to Blue
    cmd = 'rename ' + green_app_name + ' ' + blue_app_name
    run_cf_cmd(cmd)
    # Increase instances for new app
    cmd = 'scale ' + blue_app_name + ' -i ' + str(cf_env.CF_INSTANCES_PROD)
    run_cf_cmd(cmd)
    # Remove orphaned routes in Production space
    cmd = 'delete-orphaned-routes -f'
    run_cf_cmd(cmd)
    # Print status of apps in Production space
    cmd = 'apps'
    run_cf_cmd(cmd)
    # Print routes of apps in Production space
    cmd = 'routes'
    run_cf_cmd(cmd)

def cf_deploy_prod():
    print("Pushing app to Production space", flush=True)
    cf_login(cf_env.CF_SPACE_PROD)
    app_name = cf_env.CF_APP_NAME
    cf_create_smb_service(app_name)
    apps_list = cf_running_apps()
    check_err = False
    for run_app in apps_list:
        cf_stop(run_app, check_err)
        cf_delete(run_app)
    cf_push(app_name, cf_env.CF_PROD_MEM, cf_env.CF_PROD_DISK)
    cf_bind_smb_service(app_name)
    cf_start(app_name)
    # Increase instances for new app
    cmd = 'scale ' + cf_env.CF_APP_NAME + ' -i ' + str(cf_env.CF_INSTANCES_PROD)
    run_cf_cmd(cmd)
    # Print status of apps in Production space
    cmd = 'apps'
    run_cf_cmd(cmd)
    # Print routes of apps in Production space
    cmd = 'routes'
    run_cf_cmd(cmd)

def cf_deploy_dev():
    print("Pushing app to Development space", flush=True)
    cf_login(cf_env.CF_SPACE_DEV)
    app_name = cf_env.CF_APP_NAME + '-Dev'
    cf_create_smb_service(app_name)
    apps_list = cf_running_apps()
    check_err = False
    for run_app in apps_list:
        cf_stop(run_app, check_err)
        cf_delete(run_app)
    cf_push(app_name, cf_env.CF_NON_PROD_MEM, cf_env.CF_NON_PROD_DISK)
    cf_bind_smb_service(app_name)
    cf_start(app_name)

def cf_deploy_test():
    print("Pushing app to Test space", flush=True)
    cf_login(cf_env.CF_SPACE_TEST)
    app_name = cf_env.CF_APP_NAME + '-Test'
    cf_create_smb_service(app_name)
    apps_list = cf_running_apps()
    check_err = False
    for run_app in apps_list:
        cf_stop(run_app, check_err)
        cf_delete(run_app)
    cf_push(app_name, cf_env.CF_NON_PROD_MEM, cf_env.CF_NON_PROD_DISK)
    cf_bind_smb_service(app_name)
    cf_start(app_name)

def run_cf_cmd(cmd, check_err=True):
    # Run cf command to logout
    cf_cmd = CF_CLI + ' ' + cmd
    if(DEBUG): print('cmd >>> ' + cf_cmd, flush=True)
    cmd_pipe = subprocess.Popen(cf_cmd, shell = True, stdin = None, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    t_out, error = cmd_pipe.communicate()
    output = t_out.decode("utf-8")
    print(output, flush=True)
    if check_err:
        if cmd_pipe.returncode != 0:
            print("\nCF command failed: " + str(error), flush=True)
            exit(2)
    # Add small time delay after CLI commands
    time.sleep(3)


if __name__ == '__main__':
    verify_python_version()
    parser = argparse.ArgumentParser(description='Wrapper to manage CF app')
    parser.add_argument('--prod', '-p', action='store_true', default=False, help='Production deployment of app')
    parser.add_argument('--bluegreen', '-bg', action='store_true', default=False, help='Blue-Green deployment of app for Production only')
    parser.add_argument('--dev', '-d', action='store_true', default=False, help='Development deployment of app')
    parser.add_argument('--test', '-t', action='store_true', default=False, help='Test deployment of app')
    args = parser.parse_args()

    start_time = time.time()
    
    
    if args.prod:
        # Simple deployment to production which incurres a downtime
        cf_deploy_prod()
    if args.bluegreen:
        # Blue-Green deployment allows deployment of new app without any downtime
        cf_deploy_prod_blue_green()
    elif args.dev:
        cf_deploy_dev()
    elif args.test:
        cf_deploy_test()
    else:
        print("Invalid input...", flush=True)
        parser.print_help()
        exit(1)

    cf_logout()

    end_time = time.time()
    timer_minutes = round(((end_time - start_time) / 60), 2)
    print("CF Manager Time: " + str(timer_minutes) + " minutes\n", flush=True)

    exit(0)
