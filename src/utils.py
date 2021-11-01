from .workflow import *
from .dags import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import shutil
import json
import os

HEADER = '\033[1m'
FAIL = '\033[91m'
ENDC = '\033[0m'

function_types = [fn for fn in os.listdir('./functions/') if '.' not in fn]
color_lookup = {k:v for v, k in enumerate(function_types)}
low, *_, high = sorted(color_lookup.values())
norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)

def visualize_graph(graph, save_pdf=False):
	plt.clf()
	color_lookup = {n:function_types.index(n.split('_')[0]) for n in graph.nodes()}
	df = pd.DataFrame(index=graph.nodes(), columns=graph.nodes())
	for row, data in nx.shortest_path_length(graph):
	    for col, dist in data.items(): df.loc[row,col] = dist 
	df = df.fillna(df.max().max()); df = df / 2
	df = df.to_dict()
	for k in df:
		for j in df[k]:
			if k.split('_')[0] == j.split('_')[0] and not k == j:
				df[k][j] = 0.2; break
	nx.draw(graph, pos=nx.kamada_kawai_layout(graph, dist=df),
        nodelist=color_lookup,
        node_size=200,
        node_color=[mapper.to_rgba(i) 
                    for i in color_lookup.values()], 
        with_labels=True)
	if save_pdf:
		os.makedirs('dags', exist_ok=True)
		val = len(os.listdir('dags'))
		plt.savefig(f'dags/{val}.pdf')
		return
	plt.show()

def get_only_node_names(graph):
	return [n.split('_')[0] for n in graph.nodes()]

def form_dag(edge_set):
	graph = nx.DiGraph()
	graph.add_edges_from(edge_set)
	assert nx.is_directed_acyclic_graph(graph) # Check DAG
	assert not set(get_only_node_names(graph)) - set(function_types) # Check no exta nodes
	visualize_graph(graph, save_pdf=True)
	return graph

def form_all_workflows():
	shutil.rmtree('dags', ignore_errors=True)
	shutil.rmtree('temp', ignore_errors=True)
	workflows = []; dictionary = {}
	for i, edge_set in enumerate(edge_sets):
		graph = form_dag(edge_set)
		workflows.append(Workflow(f'workflow_{i}', graph))
		d = {'edge_set': edge_set, 'due_dates': due_dates[i]}
		dictionary[f'workflow_{i}'] = d
	with open("input.json", "w") as outfile:
	    json.dump(dictionary, outfile, indent=4)
	return workflows, dictionary