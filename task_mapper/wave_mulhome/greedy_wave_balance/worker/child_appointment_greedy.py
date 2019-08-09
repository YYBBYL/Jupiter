"""
.. note:: This is the main script to run in every worker node for greedy WAVE.
"""
__author__ = "Quynh Nguyen, Pranav Sakulkar,  Jiatong Wang, Pradipta Ghosh,  Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2019, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "3.0"

import json
import re
import threading
import time
import os
import sys
import urllib
import shutil
import _thread
from flask import Flask, request
import requests
from pymongo import MongoClient
import configparser
from os import path
from functools import wraps
import multiprocessing
from multiprocessing import Process, Manager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import paho.mqtt.client as mqtt
import socket
from heapq import nsmallest
import collections
import random

MAX_TASK_ALLOWED = 60

app = Flask(__name__)

def demo_help(server,port,topic,msg):
    print('Sending demo')
    username = 'anrgusc'
    password = 'anrgusc'
    client = mqtt.Client()
    client.username_pw_set(username,password)
    client.connect(server, port,300)
    client.publish(topic, msg,qos=1)
    client.disconnect()

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
    connected = {}
    for city in reg:
        pairs = [k for k,v in distance.items() if k[0]==city or k[1]==city]
        nb = dict((k, distance[k]) for k in pairs)
        neigbors = nsmallest(num, nb, key = nb.get)
        for item in neigbors:
            connected[item] = 1
            connected[(item[1],item[0])] = 1

    cluster = {}
    for geo in all_node_geo:
        cluster[geo] = all_node_geo[geo]
        nbs = [k[1] for k,v in connected.items() if v==1 and (k[0]==geo)]
        for nb in nbs:
            if nb in all_node_geo:
                cluster[geo].extend(all_node_geo[nb])
    return cluster


def prepare_global():
    """Prepare global information (Node info, relations between tasks)
    """

    INI_PATH = '/jupiter_config.ini'

    config = configparser.ConfigParser()
    config.read(INI_PATH)

    global network_map, FLASK_PORT, FLASK_SVC, MONGO_SVC_PORT, nodes, node_count, master_host, debug

    FLASK_PORT = int(config['PORT']['FLASK_DOCKER'])
    FLASK_SVC  = int(config['PORT']['FLASK_SVC'])
    MONGO_SVC_PORT  = config['PORT']['MONGO_SVC']

    global my_profiler_ip, PROFILER
    PROFILER = int(config['CONFIG']['PROFILER'])
    my_profiler_ip = os.environ['PROFILER']


    # Get ALL node info
    node_count = 0
    nodes = {}
    tmp_nodes_for_convert={}
    network_map = {}

    #Get nodes to self_ip mapping
    for name, node_ip in zip(os.environ['ALL_NODES'].split(":"), os.environ['ALL_NODES_IPS'].split(":")):
        if name == "":
            continue
        nodes[name] = node_ip + ":" + str(FLASK_SVC)
        node_count += 1

    #Get nodes to profiler_ip mapping
    for name, node_ip in zip(os.environ['ALL_NODES'].split(":"), os.environ['ALL_PROFILERS'].split(":")):
        if name == "":
            continue
        #First get mapping like {node: profiler_ip}, and later convert it to {profiler_ip: node}
        tmp_nodes_for_convert[name] = node_ip

    # network_map is a dict that contains node names and profiler ips mapping
    network_map = {v: k for k, v in tmp_nodes_for_convert.items()}

    master_host = os.environ['HOME_IP'] + ":" + str(FLASK_SVC)
    # print("Nodes", nodes)
    # print(network_map)



    global threshold, resource_data, is_resource_data_ready, network_profile_data, is_network_profile_data_ready, application

    
    threshold = 15
    resource_data = {}
    is_resource_data_ready = False
    network_profile_data = {}
    is_network_profile_data_ready = False
    debug = True

    global control_relation, children, parents

    # control relations between tasks
    control_relation = {}
    children = {}
    parents = {}

    global application
    application = read_file("DAG/DAG_application.txt")
    del application[0]

    global BOKEH_SERVER, BOKEH_PORT, BOKEH
    BOKEH_SERVER = config['OTHER']['BOKEH_SERVER']
    BOKEH_PORT = int(config['OTHER']['BOKEH_PORT'])
    BOKEH = int(config['OTHER']['BOKEH'])

    print('Bokeh information')
    print(BOKEH_SERVER)
    print(BOKEH_PORT)
    print(BOKEH)


    # for line in application:
    #     line = line.strip()
    #     items = line.split()

    #     parent = items[0]
    #     if parent == items[3] or items[3] == "home":
    #         continue

    #     children[parent] = items[3:]
    #     for child in items[3:]:
    #         if child in parents.keys():
    #             parents[child].append(parent)
    #         else:
    #             parents[child] = [parent]

    # print("application",application)
    # print("children",children)
    # print("parents" ,parents)
    # for key in parents:
    #     parent = parents[key]
    #     if len(parent) == 1:
    #         if parent[0] in control_relation:
    #             control_relation[parent[0]].append(key)
    #         else:
    #             control_relation[parent[0]] = [key]
    #     if len(parent) > 1:
    #         flag = False
    #         for p in parent:
    #             if p in control_relation:
    #                 control_relation[p].append(key)
    #                 flag = True
    #                 break
    #         if not flag:
    #             control_relation[parent[0]] = [key]

    # print("control_relation" ,control_relation)

def init_task_topology():
    """
        - Read ``DAG/input_node.txt``, get inital task information for each node
        - Read ``DAG/DAG_application.txt``, get parent list of child tasks
        - Create the DAG
        - Write control relations to ``DAG/parent_controller.txt``
    """

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
    # for key in parents:
    #     parent = parents[key]
    for key, value in sorted(parents.items()):
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

def assign_task():
    """Request assigned node for a specific task, write task assignment in local file at ``local_responsibility/task_name``.
    
    Raises:
        Exception: ``ok`` if successful, ``not ok`` if either the request or the writing is failed
    """
    try:

        task_name = request.args.get('task_name')
        # print('---------------')
        print('I am assigned the task '+task_name)
        local_mapping[task_name] = False
        res = call_send_mapping(task_name, node_name)
        # print(res)
        # print('---------------')
        # print('All my current tasks')
        # print(local_mapping)
        # print('---------------')
        
        # print('*******************')
        # print(control_relation)
        # print(local_children)
        if (task_name in control_relation) and len(control_relation[task_name])>0:
            print('I am responsible for the next children tasks')
            print(control_relation[task_name])
            # print(local_children)
            # print('1')
            for task in control_relation[task_name]:
                # print('----- my children')
                # print('2')
                # print(task)
                if task not in local_children.keys():
                    # print('3')
                    # print(task)
                    local_children[task] = 'None'
                    write_file(local_responsibility + "/" + task, 'TODO', "w+")
        else:
            print('No children tasks for this task')
        
        
        print('I am assigned the task successfully '+task_name)
        return 'ok'
    except Exception as e:
        print('I am assigned the task but not successfully '+task_name)
        print(e)
        return 'not ok'
app.add_url_rule('/assign_task', 'assign_task', assign_task)

def assign_task_to_remote(assigned_node, task_name):
    """Assign task to remote node
    
    Args:
        - assigned_node (str): Node to be assigned
        - task_name (str): task name 
    
    Raises:
        Exception: request if successful, ``not ok`` if failed
    """
    try:
        print('Assign children task '+ task_name+'to the remote node '+assigned_node)
        url = "http://" + nodes[assigned_node] + "/assign_task"
        params = {'task_name': task_name}
        params = urllib.parse.urlencode(params)
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
        # print('------&&&&')
        # print(res)
        #

        if BOKEH==3:
            topic = 'overhead_%s'%(node_name)
            msg = 'overhead %s assignremote 1 %s %s \n' %(node_name,task_name,assigned_node)
            demo_help(BOKEH_SERVER,BOKEH_PORT,topic,msg)

        return 'ok'

    except Exception as e:
        print('Failed assign children task to the remote node')
        print(e)
        return 'not ok'

def write_file(file_name, content, mode):
    """Write the content to file
    
    Args:
        - file_name (str): file path
        - content (str): content to be written
        - mode (str): write mode 
    """
    file = open(file_name, mode)
    for line in content:
        file.write(line + "\n")
    file.close()


def recv_count():
    try:
        print('Update count assign information')
        count_info = request.args.get("count_info")
        info = count_info.split('#')
        for cin in info:
            total_assign_child[cin.split(':')[0]] = int(cin.split(':')[1])
        print(total_assign_child)
    except Exception as e:
        print(e)
        print('Error update count assign information')
        
    return "ok"
app.add_url_rule('/recv_count', 'recv_count', recv_count)

def call_send_mapping(mapping, node):
    """
    - A function that used for intermediate data transfer.
    - Return mapping information for specific node.
    
    Args:
        - mapping (dict): mapping information (task-assigned node)
        - node (str): node name
    
    Raises:
        Exception: request if successful, ``not ok`` if failed
    """
    try:
        print('Announce the mapping to the master host')
        url = "http://" + master_host + "/recv_mapping"
        params = {'mapping': mapping, "node": node}
        params = urllib.parse.urlencode(params)
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
        local_mapping[mapping] = True

        if BOKEH==3:
            topic = 'overhead_%s'%(node_name)
            msg = 'overhead %s announcehome 1 %s %s \n' %(node_name,node,mapping)
            demo_help(BOKEH_SERVER,BOKEH_PORT,topic,msg)

    except Exception as e:
        return "Announce the mapping to the master host failed"
    return res

class Watcher:
    DIRECTORY_TO_WATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'task_responsibility')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        """
        Monitoring ``INPUT`` folder for the incoming files.
        
        At the moment you have to manually place input files into the ``INPUT`` folder (which is under ``centralized_scheduler_with_task_profiler``):
        
            .. code-block:: bash
        
                mv 1botnet.ipsum input/
        
        Once the file is there, it sends the file to the node performing the first task.
        """

        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()

class Handler(FileSystemEventHandler):
    """
        Handling the event when there is a new file generated in ``INPUT`` folder
    """

    @staticmethod
    def on_any_event(event):
        """
        Whenever there is a new input file in ``INPUT`` folder, the function:

        - Log the time the file is created

        - Start the connection to the first scheduled node

        - Copy the newly created file to the ``INPUT`` folder of the first scheduled node
        
        Args:
            event (FileSystemEventHandler): monitored event
        """

        if event.is_directory:
            return None

        elif event.event_type == 'created':

            print("Received file as input - %s." % event.src_path)
            new_task = os.path.split(event.src_path)[-1]
            # print(new_task)
            _thread.start_new_thread(assign_children_task,(new_task,))


def assign_children_task(children_task):
    tmp = random.randint(0, 30)
    time.sleep(tmp)
    print('Starting assigning process for the children task '+children_task)
    global myneighbors
    while True:
        if is_network_profile_data_ready and is_resource_data_ready:
            break
        else:
            print("Waiting for the profiler data")
            time.sleep(60)

    
    while True:
        # print(myneighbors)
        if len(myneighbors) == 0:
            print("Waiting for neighboring data")
            time.sleep(60)
        else:
            break
    

    res = False
    if 'app' in children_task:
        appname = children_task.split('-')[0]
        sample_file = '/'+appname+'-1botnet.ipsum'
    else:
        sample_file = '/1botnet.ipsum'
    sample_size = cal_file_size(sample_file)
    assign_to_node_list = get_most_suitable_node(sample_size)
    print(assign_to_node_list)
    for assign_to_node in assign_to_node_list:
        print('---')
        print(assign_to_node)
        if total_assign_child[assign_to_node]>= (MAX_TASK_ALLOWED-1):
            print(assign_to_node+' overloaded node already. Must reassign '+children_task)
            print(assign_to_node)
            print(total_assign_child[assign_to_node])
            # continue
        else:
            print("Trying to assign", children_task, "to", assign_to_node)
            status = assign_task_to_remote(assign_to_node, children_task)

            if status == "ok":
                print('Successfully assign ', children_task, "to", assign_to_node)
                local_children[children_task] = assign_to_node
                break
            else:
                print('Failed assign ', children_task, "to", assign_to_node)
        print('---')
def get_most_suitable_node_original(file_size):
    valid_nodes = []
    
    for tmp_node_name in network_profile_data:
        data = network_profile_data[tmp_node_name]
        delay = data['a'] * file_size * file_size + data['b'] * file_size + data['c']
        network_profile_data[tmp_node_name]['delay'] = delay
        if delay < min_value:
            min_value = delay

    # get all the nodes that satisfy: time < tmin * threshold
    for _, item in enumerate(network_profile_data):
        if network_profile_data[item]['delay'] < min_value * threshold:
            valid_nodes.append(item)

    min_value = sys.maxsize
    result_node_name = ''
    for item in valid_nodes:
        # print(item)
        tmp_value = network_profile_data[item]['delay']

        # tmp_cpu = 10000
        # tmp_memory = 10000
        tmp_cpu = sys.maxsize
        tmp_memory = sys.maxsize
        if item in resource_data.keys():
            # print(resource_data[item])
            tmp_cpu = resource_data[item]['cpu']
            tmp_memory = resource_data[item]['memory']

        tmp_cost = weight_network*tmp_value + weight_cpu*tmp_cpu + weight_memory*tmp_memory
        if  tmp_cost < min_value:
            min_value = tmp_cost
            result_node_name = item

    # print('------------- Resource')
    # print(resource_data)
    

    if not result_node_name:
        min_value = sys.maxsize
        for item in resource_data:
            tmp_cpu = resource_data[item]['cpu']
            tmp_memory = resource_data[item]['memory']
            tmp_cost = weight_cpu*tmp_cpu + weight_memory*tmp_memory
            if  tmp_cost < min_value:
                min_value = tmp_cost
                result_node_name = item

    if result_node_name:
        network_profile_data[result_node_name]['c'] = 100000

def get_most_suitable_node(file_size):
    """Calculate network delay + resource delay
    
    Args:
        file_size (int): file_size
    
    Returns:
        str: result_node_name - assigned node for the current task
    """
    global myneighbors
    # print('Trying to get the most suitable node')
    # print('My neighbor information:')
    # print(myneighbors)
    # print('Network info')
    # print(network_profile_data)
    # print('Resource info')
    # print(resource_data)


    
    weight_network = 1
    weight_cpu = 1
    weight_memory = 1
    
    cost = dict()

    for nodeid,node in enumerate(myneighbors):
        data = network_profile_data[node]
        cost_net = data['a'] * file_size * file_size + data['b'] * file_size + data['c']
        cost_cpu = resource_data[node]['cpu']
        cost_mem = resource_data[node]['memory']
        cost[node] = weight_network*cost_net + weight_cpu*cost_cpu + weight_memory*cost_mem

    # print('------------------cost')
    # print(cost)
    
    sorted_cost = sorted(cost, key=cost.get)
    # print(sorted_cost)
    return sorted_cost

    


def read_file(file_name):
    """get all lines in a file
    
    Args:
        file_name (str): file path
    
    Returns:
        str: file_contents - all lines in a file
    """
    file_contents = []
    file = open(file_name)
    line = file.readline()
    while line:
        file_contents.append(line)
        line = file.readline()
    file.close()
    return file_contents


def output(msg):
    """if debug is True, print the msg
    
    Args:
        msg (str): message to be printed
    """
    if debug:
        print(msg)


def get_resource_data_drupe():
    """Collect resource profiling information
    """
    print("Starting resource profile collection thread")
    # Requsting resource profiler data using flask for its corresponding profiler node
    try_resource_times = 0
    while True:
        time.sleep(60)
        try:
            if try_resource_times >= 10:
                print("Exceeded maximum try times, break.")
                break
            r = requests.get("http://" + os.environ['PROFILER'] + ":" + str(FLASK_SVC) + "/all")
            result = r.json()
            # print(result)
            if len(result) != 0:
                break
            else:
                try_resource_times += 1
        except Exception as e:
            print("Resource request failed. Will try again, details: " + str(e))
            try_resource_times += 1
    global resource_data
    resource_data = result

    global is_resource_data_ready
    is_resource_data_ready = True

    print("Got profiler data from http://" + os.environ['PROFILER'] + ":" + str(FLASK_SVC))
    # print("Resource profiles: ", json.dumps(result))
    if BOKEH==3:
        topic = 'overhead_%s'%(node_name)
        msg = 'overhead %s resource %d \n' %(node_name,len(myneighbors))
        demo_help(BOKEH_SERVER,BOKEH_PORT,topic,msg)


def get_network_data_drupe(my_profiler_ip, MONGO_SVC_PORT, network_map):
    """Collect the network profile from local MongoDB peer
    """
    print('Check My Network Profiler IP: '+my_profiler_ip)
    client_mongo = MongoClient('mongodb://'+my_profiler_ip+':'+MONGO_SVC_PORT+'/')
    db = client_mongo.droplet_network_profiler
    collection = db.collection_names(include_system_collections=False)
    num_nb = len(collection)-1
    while num_nb==-1:
        print('--- Network profiler mongoDB not yet prepared')
        time.sleep(60)
        collection = db.collection_names(include_system_collections=False)
        num_nb = len(collection)-1
    print('--- Number of neighbors: '+str(num_nb))
    num_rows = db[my_profiler_ip].count()
    while num_rows < num_nb:
        print('--- Network profiler regression info not yet loaded into MongoDB!')
        time.sleep(60)
        num_rows = db[my_profiler_ip].count()
    logging =db[my_profiler_ip].find().limit(num_nb)
    for record in logging:
        # Destination ID -> Parameters(a,b,c) , Destination IP
        if record['Destination[IP]'] in home_profiler_ip: continue
        params = re.split(r'\s+', record['Parameters'])
        network_profile_data[network_map[record['Destination[IP]']]] = {'a': float(params[0]), 'b': float(params[1]),
                                                            'c': float(params[2]), 'ip': record['Destination[IP]']}
    print('Network information has already been provided')
    # print(network_profile_data)

    global is_network_profile_data_ready
    is_network_profile_data_ready = True

    if BOKEH==3:
        topic = 'overhead_%s'%(node_name)
        msg = 'overhead %s network %d \n' %(node_name,len(myneighbors))
        demo_help(BOKEH_SERVER,BOKEH_PORT,topic,msg)
    




def profilers_mapping_decorator(f):
    """General Mapping decorator function
    """
    @wraps(f)
    def profiler_mapping(*args, **kwargs):
      return f(*args, **kwargs)
    return profiler_mapping

def get_network_data_mapping():
    """Mapping the chosen TA2 module (network monitor) based on ``jupiter_config.PROFILER`` in ``jupiter_config.ini``
    
    Args:
        PROFILER (str): specified from ``jupiter_config.ini``
    
    Returns:
        TYPE: corresponding network function
    """
    if PROFILER==0: 
        return profilers_mapping_decorator(get_network_data_drupe)
    return profilers_mapping_decorator(get_network_data_drupe)

def get_resource_data_mapping():
    """Mapping the chosen TA2 module (resource monitor) based on ``jupiter_config.PROFILER`` in ``jupiter_config.ini``
    
    Args:
        PROFILER (str): specified from ``jupiter_config.ini``
    
    Returns:
        TYPE: corresponding resource function
    """
    if PROFILER==0: 
        return profilers_mapping_decorator(get_resource_data_drupe)
    return profilers_mapping_decorator(get_resource_data_drupe)

def cal_file_size(file_path):
    """Return the file size in bytes
    
    Args:
        file_path (str): The file path
    
    Returns:
        float: file size in bytes
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size * 0.008

def main():
    """
        - Prepare global information
        - Initialize folders ``local`` and ``local_responsibility``, prepare ``local_children`` and ``local_mapping`` file.
        - Start thread to get resource profiling data
        - Start thread to get network profiling data
        - Start thread to watch directory: ``local/task_responsibility``
        - Start thread to thread to assign todo task to nodes
    """
    
    prepare_global()
    # print(control_relation)

    global node_name, node_id, FLASK_PORT, home_profiler_ip, home_profiler_nodes

    node_name = os.environ['SELF_NAME']
    node_id = int(node_name.split("e")[-1])

    home_profiler = os.environ['HOME_PROFILER_IP'].split(' ')
    home_profiler_nodes = [x.split(':')[0] for x in home_profiler]
    home_profiler_ip = [x.split(':')[1] for x in home_profiler]


    print("Node name:", node_name, "and id", node_id)
    print("Starting the main thread on port", FLASK_PORT)

    
    get_network_data = get_network_data_mapping()
    get_resource_data = get_resource_data_mapping()
    # while init_folder() != "ok":  # Initialize the local folers
    #     pass

    global local_mapping, local_children,local_responsibility, manager,total_assign_child
    manager = Manager()
    local_mapping = manager.dict()
    local_children = manager.dict()
    total_assign_child = manager.dict()
    

    global all_node_geo, cluster, mygeo
    all_node_geo_info = os.environ['ALL_NODES_GEO']
    mygeo = os.environ['MY_GEO']
    mygeo = mygeo.split('-')[-1][0:3]
    info = all_node_geo_info.split('$')
    all_node_geo = dict()
    for geo in info:
        g = geo.split(':')[0]
        all_node_geo[g] = []
        tmp = geo.split(':')[1].split('#')
        for t in tmp:
            all_node_geo[g].append(t)

    cluster = define_cluster(all_node_geo,3)

    global myneighbors
    myneighbors = set(cluster[mygeo])

    for node in myneighbors:
        total_assign_child[node] = 0

    myneighbors.remove(node_name)
    # print('--------------My neighbors')
    # print(myneighbors)

    

    local_responsibility = "task_responsibility"
    os.mkdir(local_responsibility)

    init_task_topology()
    # Get resource data
    _thread.start_new_thread(get_resource_data, ())

    # Get network profile data
    _thread.start_new_thread(get_network_data, (my_profiler_ip, MONGO_SVC_PORT,network_map))

    #monitor Task responsibility folder for the incoming tasks
    w = Watcher()
    w.run()

    app.run(host='0.0.0.0', port=int(FLASK_PORT))


if __name__ == '__main__':
    main()
    