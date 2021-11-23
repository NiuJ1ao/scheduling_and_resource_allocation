from os import pread
from my_utils import get_workflow_from_json, total_tardiness, dump_schedule, weighted_tardiness
from collections import deque, defaultdict
import copy
import numpy as np
try:
    from tabulate import tabulate
except ImportError:
    print("pip install tabulate for intermediate results")

class tabu_list():
    def __init__(self, tabu_size):
        self._l = deque(tabu_size*[0], tabu_size)
        self._idx = 0
    
    def add(self, pair):
        self._l.popleft()
        self._l.append(pair)

    def __iter__(self):
        self._idx = 0
        return self

    def __next__(self):
        try:
            result = self._l[self._idx]
        except IndexError:
            self._idx = 0
            raise StopIteration
        self._idx += 1
        return result

    def __str__(self):
        return str([(tuple(e)[0]+1, tuple(e)[1]+1) for e in self._l if e != 0])

def validate_neighbour(schedule, precedences, idx_i, idx_j):
    job_i, job_j = schedule[idx_i], schedule[idx_j]
    p_i, p_j = precedences[job_i], precedences[job_j]
    
    for p in p_i + p_j:
        if p not in schedule[:idx_j]:
            return False
    
    return True

def get_precedences(graph):
    p = defaultdict(list)
    for i in graph:
        for j in graph[i]:
            p[j].append(i)
    return p
    
def read_init_schedule(fname="sinit.csv"):
    with open(fname, 'r') as f:
        line = f.read()
        jobs = line.split(',')
        schedule = [int(j)-1 for j in jobs]
        
    return schedule

def tabu_search(workflow, init_s, iter_num=5, tabu_size=5, gamma=30):
    node_types = workflow["node_types"]
    process_times = workflow["process_times"]
    due_dates = workflow["due_dates"]
    graph = workflow["graph"]
    precedences = get_precedences(graph)

    tabu = tabu_list(tabu_size)

    # compute g for init_s
    process_init = [process_times[node_types[j].split('_')[0]] for j in init_s]
    complete_times = np.cumsum(process_init)
    g_best = total_tardiness(init_s, complete_times, due_dates)
    g_x = g_best

    candidates = [init_s]
    best_idx = 0
    
    # for visualize intermediate solution
    intermediate_sol = [[0, copy.deepcopy(tabu), g_best, np.array(init_s)+1, round(g_x, 2), "x"]]
    for k in range(iter_num):
        sol = [k+1]
        sol.append(copy.deepcopy(tabu))
        sol.append(g_best)
        
        # schedule x_k from last round
        x = candidates[-1]

        neighbours = []
        candidates_k = {}
        for i in range(len(x)-1):
            # swap jobs to create a neighbour
            pair = {x[i], x[i+1]}
            y = copy.deepcopy(x)
            y[i], y[i+1] = y[i+1], y[i]

            # check for job precedences
            if not validate_neighbour(y, precedences, i, i+1):
                continue
            
            # compute g(y)
            process_times_y = [process_times[node_types[j].split('_')[0]] for j in y]
            complete_times = np.cumsum(process_times_y)
            g_y = total_tardiness(y, complete_times, due_dates)
            
            # delta = g(x_k) - g(y)
            delta = g_x - g_y
            
            neighbours.append(y)
            candidates_k[str(y)] = {"cost": g_y, "pair": pair, "delta": delta}
            
        # selet next neighbour in lexicographic order
        neighbours.sort()
        
        visual_k, gs_k, is_tabu = [], [], []
        is_optimal = True
        for y in neighbours:
            y_str = str(y)
            g_y = candidates_k[y_str]["cost"]
            pair = candidates_k[y_str]["pair"]
            delta = candidates_k[y_str]["delta"]
            
            visual_k.append(y)
            gs_k.append(g_y)
            if pair in tabu:
                is_tabu.append(["o"])
            else:
                is_tabu.append(["x"])
            
            # stop criterias
            if (delta > -gamma and pair not in tabu) or g_y < g_best:
                is_optimal = False
                sol.append(np.array(visual_k) + 1)
                sol.append(np.array([round(g, 2) for g in gs_k]).reshape(-1,1))
                sol.append(np.array(is_tabu))
                break
            
        if is_optimal:
            print("Early stop! Cannot find a candidate.")
            break
        
        # append y for next iteration and add node pair to tabu
        candidates.append(y)
        g_x = g_y
        tabu.add(pair)
        
        # store the best schedule
        if g_best > g_y:
            best_idx = k
            g_best = g_y
        
            intermediate_sol.append(sol)
    
    # visualize intermediate 
    if 'tabulate' in globals():
        print(tabulate(intermediate_sol, headers=['k', 'tabu', 'g_best', 'candidates', 'g_y', "tabu?"]))

    best = np.array(candidates[best_idx+1])
    process_times_y = [process_times[node_types[j].split('_')[0]] for j in best]
    complete_times = np.cumsum(process_times_y)
    return best + 1, complete_times[-1], total_tardiness(best, complete_times, due_dates)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--iter', type=int,
                        default=5,
                        help='Iteration number')
    parser.add_argument('-t', '--tabu_size', type=int,
                        default=5,
                        help='Size of tabu table')
    parser.add_argument('-g', '--gamma', type=int,
                        default=30,
                        help='Gamma')
    
    parser.add_argument('--workflow_file', type=str,
                        default="input.json",
                        help='Input JSON file of workflow')
    parser.add_argument('--process_time_file', type=str,
                        default="process_times.txt",
                        help='Text file of obtained process times')
    parser.add_argument('--init_schedule_file', type=str,
                        default="sinit.csv",
                        help='CSV file of initial schedule')
    parser.add_argument('--dump_schedule', action='store_true',
                        help='True if dump final schedule to a CSV file')
    args = parser.parse_args()
    print(args)
    
    workflow = get_workflow_from_json(fflow=args.workflow_file, ftime=args.process_time_file)
    init_s = read_init_schedule(args.init_schedule_file)
    schedule, complete_time, cost = tabu_search(workflow, init_s=init_s, iter_num=args.iter, tabu_size=args.tabu_size, gamma=args.gamma)
    print("Schedule:", schedule)
    print("Complete time:", complete_time)
    print("Total tardiness:", cost)
    
    if args.dump_schedule:
        dump_schedule("tabu.csv", schedule)
    