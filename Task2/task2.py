import xml.etree.ElementTree as ET
from toposort import toposort

xml_path = "Job.xml"
config_path = "ComputersGroups.ini"
task_flow_index = 1
tasks_json_list = []
xmlnms = "{urn:proactive:jobdescriptor:3.2}"
output_path = "output.txt"
edges = {}

with open(config_path, "r") as file:
    # read config file and load it to memory
    config_data = file.read().lower()
    config_array = config_data.split("\n")
    computers_config = {str(i[0:i.find("=") - 1]): i[i.find("=") + 3:i.rfind("\""):].split(",") for i in config_array}


def parse_task(task_element):
    """
    Given an Element object, parse it to json in the format:
    {name: <string> , parameters: [<command>,<arguments>,<computers>]}
    :param task_element: xml.etree.ElementTree
    :return: json object representing the object
    """
    deps = task_element.findall("./" + xmlnms + "depends")
    additional_info = task_element.findall(".//" + xmlnms + "parameter")
    name = task_element.get('name')
    parameters = [additional_info[i].get("value") for i in range(0, 3)]

    return {"name": name, "parameters": parameters, "deps": deps}


def run(task_json):
    """
    Given a json representing a task, return a string representing all of the data of the task for all of it's computers
    :param task_json: json object
    :return: string
    """
    str_to_return = ""
    for i in computers_config[task_json['parameters'][2].lower()]:
        str1 = "{}: ({}) '{}' {}\n".format(task_json['name'], i, task_json['parameters'][0], task_json['parameters'][1])
        str_to_return += str1
    return str_to_return


task_flow_label = ET.parse(xml_path).getroot()[task_flow_index]  # get the root of the elementTree
tasks = [parse_task(task) for task in task_flow_label]  # parse the XML

# Build an adjacency list for each of the tasks . j in edges[i] iff i is dependent in j. We will use it
# for topological sort.
for i in range(len(tasks)):
    edges[i] = set()
    for j in range(len(tasks[i]['deps'])):
        edges[i].add(j)
sorted = list(toposort(edges))  # topological sort, 3rd party libary. Now we have a list of sets, for each
# dependency level (most independent - level 0)
with open(output_path, "w") as output_file:
    for level in sorted:
        for index in level:
            output_file.write(run(tasks[index]))  # write to the output file.
