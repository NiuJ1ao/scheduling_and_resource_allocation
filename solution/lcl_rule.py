from my_utils import get_workflow_from_json, tardiness, dump_schedule, total_tardiness
import numpy as np
import random
random.seed(42)
try:
    from tabulate import tabulate
except ImportError:
    print("pip install tabulate for intermediate results")

def schedule_complete_time(graph, node_types, process_times):
    return np.sum([process_times[node_types[node].split('_')[0]] for node in graph])

def update_graph(graph, job):
    graph.pop(job)
    
    # n_i -= 1 for all jobs i ∈ V that have j as immediate successor
    for node in graph:
        successors = graph[node]
        if job in successors:
            successors.remove(job)

def least_cost_last(workflow):
    graph = workflow["graph"]
    total_nodes = len(graph)
    
    node_types = workflow["node_types"]
    process_times = workflow["process_times"]
    due_dates = workflow["due_dates"]

    schedule = [-1]*len(graph)
    
    intermediate_sol = []
    for k in range(total_nodes-1, -1, -1):
        # compute total process time p(V)
        process_time = schedule_complete_time(graph, node_types, process_times)

        # find jobs with no immediate successors
        nodes = [node for node in graph if len(graph[node]) == 0]
        
        # compute g for all jobs in V
        gs = {node: tardiness(process_time, due_dates[node]) for node in nodes}
        
        # find the minimum g among nodes of no successors
        min_g = min(gs.values())

        # Find job j in V with n_j = 0 and minimal g_j(p(V))
        cands = [node for node in nodes if gs[node] == min_g]
        j = random.choice(cands) # break tie

        # Schedule j in k-th position of the optimal sequence S
        schedule[k] = j

        # Remove j from V
        update_graph(graph, j)
        
        intermediate_sol.append([k, [job+1 for job in schedule if job != -1], {node+1: round(gs[node], 2) for node in gs}])

    if 'tabulate' in globals():
        print(tabulate(intermediate_sol, headers=['k', 'schedule', 'g_j with no immediate successors']))
    
    complete_times = np.cumsum([process_times[node_types[j].split('_')[0]] for j in schedule])
    return np.array(schedule) + 1, complete_times[-1], total_tardiness(schedule, complete_times, due_dates)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--workflow_file', type=str,
                        default="input.json",
                        help='Input JSON file of workflow')
    parser.add_argument('--process_time_file', type=str,
                        default="process_times.txt",
                        help='Text file of obtained process times')
    parser.add_argument('--dump_schedule', action='store_true',
                        help='True if dump final schedule to a CSV file')
    args = parser.parse_args()
    print(args)

    workflow = get_workflow_from_json(fflow=args.workflow_file, ftime=args.process_time_file)
    schedule, complete_time, cost = least_cost_last(workflow)
    print("Schedule:", schedule)
    print("Complete time:", complete_time)
    print("Total tardiness:", cost)
    if args.dump_schedule:
        dump_schedule("lcl.csv", schedule)
