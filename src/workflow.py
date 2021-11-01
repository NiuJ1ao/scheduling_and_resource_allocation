from copy import deepcopy
from subprocess import run, Popen, PIPE
import os
from time import time
import networkx as nx

class Workflow():
	def __init__(self, name, graph):
		self.name = name
		self.graph = graph
		self.remaining_graph = deepcopy(graph)
		self.dist_convered_from_root = -1
		self.executed = {}
		os.makedirs(f'temp/{self.name}/')

	def get_root(self):
		nodes = [n for n,d in self.graph.in_degree() if d==0] 
		return nodes[0]

	def get_possible_nodes(self):
		nodes = [n for n,d in self.remaining_graph.in_degree() if d==0] 
		return nodes

	def check_complete(self):
		return len(self.remaining_graph.nodes()) == 0

	def execute(self, node, ip):
		assert node not in self.executed.keys()
		input_path, output_path = 'samples/', f'./temp/{self.name}' 
		dist = max(0, len(nx.shortest_path(self.graph, self.get_root(), node)) - 1)
		update_imgs = True #dist > self.dist_convered_from_root
		if update_imgs: self.dist_convered_from_root = dist
		if self.dist_convered_from_root > 0: 
			input_path = output_path
		dataset = list(filter(lambda k: '.md' not in k, os.listdir(input_path)))
		app = node.split('_')[0]
		for file in dataset:
			predecessors = list(self.graph.predecessors(node))
			predecessor = predecessors[0] if predecessors else None
			if predecessor and predecessor not in file: continue
			input_img = os.path.join(input_path, file)
			output_img = os.path.join(output_path, node+'_'+file.split('_')[-1])
			cmd = f'http http://{ip}:7071/api/{app} @{input_img}'
			if update_imgs:
				cmd += f' > {output_img}'
			run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
			if update_imgs:
				if os.path.getsize(output_img) == 0:
					raise(Exception('Azure functions are not running.'))
		self.executed[node] = time()
		self.remaining_graph.remove_node(node)

