import random
from lcl_rule import least_cost_last
from tabu_search import tabu_search
from my_utils import get_workflow_from_json, total_tardiness
from collections import defaultdict
import numpy as np

schedule, complete_time, cost = least_cost_last(get_workflow_from_json(fflow="input.json", ftime="process_times.txt"))
print("Schedule:", schedule)
print("Complete time:", complete_time)
print("Total tardiness:", cost)

def get_precedences(graph):
    p = defaultdict(list)
    for i in graph:
        for j in graph[i]:
            p[j].append(i)
    return p

workflow = get_workflow_from_json(fflow="input.json", ftime="process_times.txt")
graph = workflow["graph"]
process_times = workflow["process_times"]
node_types = workflow["node_types"]
due_dates = workflow["due_dates"]
V = len(graph)
precedences = get_precedences(graph)

while True:
    sinit = [32]
    candidates = set(graph[32])
    while len(sinit) < V:
        # print("candidates:", candidates)
        sinit.append(random.choice(list(candidates)))
        # print(np.array(sinit) + 1)
        node = sinit[-1]
        for cand in graph[node]:
            valid = True
            pre = precedences[cand]
            for j in pre:
                valid &= j in sinit
            if valid:
                candidates.add(cand)
        candidates.remove(node)
        
    for i, job in enumerate(sinit):
        successors = graph[job]
        for s in successors:
            assert s in sinit[i+1:], "child not find in subschdule after parent"   

    # print(sinit)
    schedule, complete_time, tabu_cost = tabu_search(workflow, init_s=sinit, iter_num=1000, tabu_size=5, gamma=30)


    if tabu_cost < cost:
        print()
        print("Sinit:", ",".join([str(j+1) for j in sinit]))
        ps = [process_times[node_types[j].split('_')[0]] for j in sinit]
        complete_times = np.cumsum(ps)
        print("Total tardiness:", total_tardiness(sinit, complete_times, due_dates))
        print("Schedule:", schedule)
        print("Complete time:", complete_time)
        print("Total tardiness:", tabu_cost)
