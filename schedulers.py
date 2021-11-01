from src.workflow import *
from src.utils import *
import numpy as np
import random

def randomscheduler(workflow, dictionary):
	schedule = []
	while not workflow.check_complete():
		possible_nodes = workflow.get_possible_nodes()
		selected = random.choice(possible_nodes)
		workflow.remaining_graph.remove_node(selected)
		schedule.append(selected)
	return schedule

def simplescheduler(workflow, dictionary):
	schedule = []
	while not workflow.check_complete():
		possible_nodes = workflow.get_possible_nodes()
		duedates = [dictionary[workflow.name]['due_dates'][node] for node in possible_nodes]
		selected = possible_nodes[np.argmin(duedates)]
		workflow.remaining_graph.remove_node(selected)
		schedule.append(selected)
	return schedule
