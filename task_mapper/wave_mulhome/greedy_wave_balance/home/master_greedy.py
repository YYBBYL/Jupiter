"""
.. note:: This is the main script to run in home node for greedy WAVE.
"""
__author__ = "Quynh Nguyen, Pranav Sakulkar, Jiatong Wang, Pradipta Ghosh, Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2019, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "3.0"

import re
import threading
import os
import urllib
import json
import sys
import _thread
import time
from flask import Flask, request
import configparser
from os import path
import multiprocessing
from multiprocessing import Process, Manager
import paho.mqtt.client as mqtt
from heapq import nsmallest
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

MAX_TASK_ALLOWED = 10

def demo_help(server,port,topic,msg):
    username = 'anrgusc'
    password = 'anrgusc'
    client = mqtt.Client()
    client.username_pw_set(username,password)
    client.connect(server, port,300)
    client.publish(topic, msg,qos=1)
    client.disconnect()


def read_file(file_name):
    """
    Get all lines in a file
    
    Args:
        file_name (str): file path
    
    Returns:
        str: file_contents - all lines in a file
    """
    
    #lock.acquire()
    file_contents = []
    file = open(file_name)
    line = file.readline()
    while line:
        file_contents.append(line)
        line = file.readline()
    file.close()
    #lock.release()
    return file_contents

def define_cluster(all_node_geo,num):
    #num: select k neighbors near the node based on shorted distance
    distance = {}
    distance[('lon','tor')] = 8
    distance[('lon','fra')] = 1.5
    distance[('lon','sgp')] = 13
    distance[('lon','blr')] = 10
    distance[('lon','ams')] = 1
    distance[('lon','sfo')] = 11
    distance[('lon','nyc')] = 8
    distance[('tor','fra')] = 8.5
    distance[('tor','sgp')] = 20.5
    distance[('tor','blr')] = 19.5 
    distance[('tor','ams')] = 7
    distance[('tor','sfo')] = 5
    distance[('tor','nyc')] = 1.5
    distance[('fra','sgp')] = 12.5
    distance[('fra','blr')] = 9.5
    distance[('fra','ams')] = 1
    distance[('fra','sfo')] = 11
    distance[('fra','nyc')] = 8.5
    distance[('sgp','blr')] = 4.5 
    distance[('sgp','ams')] = 13
    distance[('sgp','sfo')] = 16.5
    distance[('sgp','nyc')] = 18.5
    distance[('blr','ams')] = 12
    distance[('blr','sfo')] = 22
    distance[('blr','nyc')] = 19.5
    distance[('ams','sfo')] = 10.5
    distance[('ams','nyc')] = 8
    distance[('nyc','sfo')] = 5.5

    # reg = ['lon','tor','fra','sgp','blr','ams','sfo','nyc']
    reg = all_node_geo.keys()
    # print(reg)
    # print(type(reg))
    connected = {}
    for city in reg:
        pairs = [k for k,v in distance.items() if k[0]==city or k[1]==city]
        nb = dict((k, distance[k]) for k in pairs)
        neigbors = nsmallest(num, nb, key = nb.get)
        for item in neigbors:
            connected[item] = 1
            connected[(item[1],item[0])] = 1

    # print(all_node_geo)

    cluster = {}
    for geo in all_node_geo:
        cluster[geo] = all_node_geo[geo]
        # print(cluster)
        # print(connected)
        nbs = [k[1] for k,v in connected.items() if v==1 and (k[0]==geo)]
        # print(nbs)
        for nb in nbs:
            if nb in all_node_geo:
                cluster[geo].extend(all_node_geo[nb])
    return cluster



def prepare_global():
    """
    Prepare global information (Node info, relations between tasks, initial task)
    """

    INI_PATH = '/jupiter_config.ini'

    config = configparser.ConfigParser()
    config.read(INI_PATH)

    global FLASK_PORT, FLASK_SVC, MONGO_SVC, nodes, node_count, master_host

    FLASK_PORT = int(config['PORT']['FLASK_DOCKER'])
    FLASK_SVC  = int(config['PORT']['FLASK_SVC'])
    MONGO_SVC  = int(config['PORT']['MONGO_SVC'])

    print("starting the main thread on port")

    
    global task_assign_summary, docker_ip2node_name
    # Get ALL node info
    node_count = 0
    nodes = {}
    docker_ip2node_name = {}
    task_assign_summary = []

    for node_name, node_ip in zip(os.environ['ALL_NODES'].split(':'), os.environ['ALL_NODES_IPS'].split(':')):
        if node_name == "":
            continue
        nodes[node_name] = node_ip + ":" + str(FLASK_SVC)
        node_count += 1
    master_host = os.environ['HOME_IP'] + ":" + str(FLASK_SVC)
    print("Nodes", nodes)

    global node_id, debug
    # global node_name
    # node_name = ""
    node_id = -1
    
    debug = True

    global control_relation, children, parents, init_tasks, local_children, local_mapping, local_responsibility

    # control relations between tasks
    control_relation = {}
    # task's children tasks
    children = {}
    # task's parent tasks
    parents = {}
    # running tasks in node in at the beginning
    init_tasks = {}

    local_children = "local/local_children.txt"
    local_mapping = "local/local_mapping.txt"
    local_responsibility = "local/task_responsibility"

    global lock, assigned_tasks, application, MAX_TASK_NUMBER,assignments, manager,total_assign_child
    manager = Manager()
    assignments = manager.dict()
    assigned_tasks = manager.dict()
    total_assign_child = manager.dict()
    for node in nodes:
        total_assign_child[node] = 0

    application = read_file("DAG/DAG_application.txt")
    MAX_TASK_NUMBER = int(application[0])  # Total number of tasks in the DAG 
    print("Max task number ", MAX_TASK_NUMBER)
    del application[0]

    assignments = {}

    global all_node_geo, cluster
    all_node_geo_info = os.environ['ALL_NODES_GEO']
    info = all_node_geo_info.split('$')
    all_node_geo = dict()
    for geo in info:
        g = geo.split(':')[0]
        all_node_geo[g] = []
        tmp = geo.split(':')[1].split('#')
        for t in tmp:
            all_node_geo[g].append(t)

    cluster = define_cluster(all_node_geo,3)

    global BOKEH_SERVER, BOKEH_PORT, BOKEH
    BOKEH_SERVER = config['OTHER']['BOKEH_SERVER']
    BOKEH_PORT = int(config['OTHER']['BOKEH_PORT'])
    BOKEH = int(config['OTHER']['BOKEH'])

    # print('Bokeh information')
    # print(BOKEH_SERVER)
    # print(BOKEH_PORT)
    # print(BOKEH)
        


# def recv_task_assign_info():
#     """
#         Receive task assignment information from the workers
#     """
#     assign = request.args.get('assign')
#     task_assign_summary.append(assign)
#     print("Task assign summary: " + json.dumps(task_assign_summary))
    

#     return 'ok'
# app.add_url_rule('/recv_task_assign_info', 'recv_task_assign_info', recv_task_assign_info)


def recv_mapping():
    """
    From each droplet, the master receive the local mapping of the assigned task for that droplet, combine all of the information
    Write the global mapping to ``assignments`` variable and ``local/input_to_CIRCE.txt``
    
    Returns:
        str: ``ok`` if mapping is ready, ``not ok`` otherwise 

    Raises:
        Exception:   when mapping is not ready
    """

    try:
        print('Receive mapping from the workers')
        node = request.args.get('node')
        mapping = request.args.get("mapping")
        total_assign_child[node] = total_assign_child[node]+1
        announce_count_assigned()

        if BOKEH==3:
            msg = 'overhead wavehome taskassign 1 %s %s \n'%(node,mapping)
            demo_help(BOKEH_SERVER,BOKEH_PORT,"overhead_home",msg)

        to_be_write = []
        items = re.split(r'#', mapping)
        for _, p in enumerate(items):
            p = p.strip()
            assigned_tasks[p] = 1
            assignments[p] = node
            to_be_write.append(p + '\t' + node)

        # print('-------------------')
        # print(assignments)
        # print('-------------------')
        if not os.path.exists("./local"):
            os.mkdir("./local")

        write_file("local/input_to_CIRCE.txt", to_be_write, "a+")
    except Exception as e:
        print(e)
        return "not ok"
    return "ok"
app.add_url_rule('/recv_mapping', 'recv_mapping', recv_mapping)

def announce_count_assigned():
    print('Announce assigned counting information to the worker')
    for node in nodes:
        try:
            # print(nodes[node])
            
            url = "http://" + nodes[node] + "/recv_count"
            count_info = '#'.join('{}:{}'.format(key, value) for key, value in total_assign_child.items())
            # print(count_info)
            params = {"count_info": count_info}
            params = urllib.parse.urlencode(params)
            req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
            res = urllib.request.urlopen(req)
            res = res.read()
            res = res.decode('utf-8')

        except Exception as e:
            print(e)
            print("Failed to announce the count assign info to the worker")

def return_assignment():
    """
    Return mapping assignments which have been finished at the current time of request.
    
    Returns:
        json: mapping assignments
    """
    print("Recieved request for current mapping. Current mappings done:", len(assignments))
    print(assignments)
    if len(assignments) == MAX_TASK_NUMBER:
        print(assignments)
        return json.dumps(assignments)
    else:
        return json.dumps(dict())
app.add_url_rule('/', 'return_assignment', return_assignment)



def assign_task_to_remote(assigned_node, task_name):
    """
    A function that used for intermediate data transfer. Assign initial task mapping to corresponding node, used in `init_thread()`
    
    Args:
        - assigned_node (str): node which is assigned to the task
        - task_name (str): name of the task
    
    Returns:
        str: request if sucessful, ``not ok`` otherwise
    """
    try:
        print('Assign the first task based on the input file')
        url = "http://" + nodes[assigned_node] + "/assign_task"
        # print(url)
        # print(task_name)
        # print(nodes)
        # print(nodes[assigned_node])
        params = {'task_name': task_name}
        params = urllib.parse.urlencode(params)
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
        if BOKEH==3:
            msg = 'overhead wavehome assignfirst 1 \n'
            demo_help(BOKEH_SERVER,BOKEH_PORT,"overhead_home",msg)
    except Exception as e:
        print(e)
        return "not ok"
    return res


def init_thread():
    """
    Assign the first task
    """
    time.sleep(60)
    print('--------------- Init thread')
    for key in init_tasks:
        # print(key)
        tasks = init_tasks[key]
        for _, task in enumerate(tasks):
            res = assign_task_to_remote(key, task)
            if res == "ok":
                output("Assign task %s to node %s" % (task, key))
            else:
                output("Assign task %s to node %s failed" % (task, key))


def monitor_task_status():
    """
    Monitor task allocation status and print notification if all task allocations are done
    """

    print('Waiting for task assignments')

    killed = 0
    while True:
        # print(len(assigned_tasks))
        if len(assigned_tasks) == MAX_TASK_NUMBER:
            print("All task allocations are done! Great News!")
            print(assignments)
            break
        time.sleep(60)



def write_file(file_name, content, mode):
    """
    Write the content to file
    
    Args:
        - file_name (str): file path
        - content (str): content to be written
        - mode (str): write mode 
    """

    #lock.acquire()
    file = open(file_name, mode)
    for line in content:
        file.write(line + "\n")
    file.close()
    #lock.release()


def init_task_topology():
    """
        - Read ``DAG/input_node.txt``, get inital task information for each node
        - Read ``DAG/DAG_application.txt``, get parent list of child tasks
        - Create the DAG
        - Write control relations to ``DAG/parent_controller.txt``
    """

    input_nodes = read_file("DAG/input_node.txt")
    del input_nodes[0]
    for line in input_nodes:
        line = line.strip()
        items = line.split()
        task = items[0]

        for node in items[1:]:
            if node in init_tasks.keys():
                init_tasks[node].append(task)
            else:
                init_tasks[node] = [task]

    print('------- Init tasks')
    print("init_tasks" ,init_tasks)

    for line in application:
        line = line.strip()
        items = line.split()

        parent = items[0]
        if parent == items[3] or items[3] == "home":
            continue

        children[parent] = items[3:]
        for child in items[3:]:
            if child in parents.keys():
                parents[child].append(parent)
            else:
                parents[child] = [parent]

    # print(parents)
    # print(child)

    for key, value in sorted(parents.items()):
    # for key in parents:
        # parent = parents[key]
        parent = value
        if len(parent) == 1:
            if parent[0] in control_relation:
                control_relation[parent[0]].append(key)
            else:
                control_relation[parent[0]] = [key]
        if len(parent) > 1:
            flag = False
            for p in parent:
                if p in control_relation:
                    control_relation[p].append(key)
                    flag = True
                    break
            if not flag:
                control_relation[parent[0]] = [key]
    print('----------- Control relation')
    print("control_relation" ,control_relation)


def output(msg):
    """
    if debug is True, print the msg
    
    Args:
        msg (str): message to be printed
    """
    if debug:
        print(msg)

def main():
    """
        - Prepare global information
        - Start the main thread: get inital task information for each node, get parent list of child tasks, Update control relations between tasks in the system
        - Start thread to watch directory: ``local/task_responsibility``
        - Start thread to monitor task mapping status
    """
    prepare_global()

    print("starting the main thread on port", FLASK_PORT)

    init_task_topology()
    _thread.start_new_thread(init_thread, ())
    _thread.start_new_thread(monitor_task_status, ())

    # sched = BackgroundScheduler()
    # sched.add_job(announce_count_assigned,'interval',id='announcement', seconds=1, replace_existing=True)

    

    app.run(host='0.0.0.0', port=int(FLASK_PORT))

if __name__ == '__main__':
    main()
