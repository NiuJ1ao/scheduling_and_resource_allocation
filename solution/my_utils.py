import json
from collections import defaultdict

def _test_graph():
    return {"graph": {0: [33], 1: [0], 2: [33], 3: [2], 4: [1], 5: [33], 6: [5], 7: [6], 8: [7], \
        9: [8], 10: [4], 11: [4], 12: [11], 13: [12], 14: [10], 15: [14], 16: [15], \
            17: [16], 18: [17], 19: [18], 20: [17], 21: [20], 22: [21], 23: [4], 24: [23], \
                25: [24], 26: [25], 27: [26], 28: [27], 29: [28], 30: [28], 31: [30], \
                    32: [3, 9, 13, 19, 22, 29, 31], 33: []}, \
        "node_types": ['onnx_1', 'muse_1', 'emboss_1', 'emboss_2', 'blur_1', \
            'emboss_3', 'vii_1', 'blur_2', 'wave_1', 'blur_3', 'blur_4', \
                'emboss_4', 'onnx_2', 'onnx_3', 'blur_5', 'wave_2', \
                    'wave_3', 'wave_4', 'emboss_5', 'onnx_4', 'emboss_6', \
                        'onnx_5', 'vii_2', 'blur_6', 'night_1', 'muse_2', \
                            'emboss_7', 'onnx_6', 'wave_5', 'emboss_8', \
                                'muse_3', 'onnx_7', 'onnx_8', 'wave_6'], \
        "process_times": {"vii": 18.4808, "emboss": 1.6932, "blur": 5.6873, "wave": 14.6057, "muse": 11.1329, "night": 24.1065, "onnx": 5.2700}, \
        "due_dates": [172, 82, 18, 61, 93, 71, 217, 295, 290, \
            287, 253, 307, 279, 73, 355, 34, 233, 77, \
                88, 122, 71, 181, 340, 141, 209, 217, \
                    256, 144, 307, 329, 269, 102, 285, 51]}

# T_j = max(0, C_j - d_j)
def tardiness(complete_time, due_date):
    return max(0, complete_time - due_date)

def total_tardiness(schedule, complete_times, due_dates):
    weights = {j: 1 for j in schedule}
    return weighted_tardiness(schedule, complete_times, due_dates, weights)
    
def weighted_tardiness(schedule, complete_times, due_dates, weights):
    result = 0
    for j, c in zip(schedule, complete_times):
        result += weights[j] * tardiness(c, due_dates[j])
    return result

def max_tardiness(schedule, complete_times, due_dates):
    return max([tardiness(c, due_dates[j]) for j, c in zip(schedule, complete_times)])

def dump_schedule(fname, schedule):
    with open(fname, 'w') as f:
        delimiter = ""
        for job in schedule:
            f.write(f"{delimiter}{job}")
            delimiter = ", "

def get_process_times(fname):
    times = {}
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith("Processing Time"):
                toks = line.split()
                job = toks[3].strip()
                time = float(toks[5].strip())
                times[job] = time
                
    return times

def get_workflow_from_json(fflow, ftime, workflow="workflow_0"):
    with open(fflow, "r") as f:
        data = json.load(f)

    edge_set = data[workflow]["edge_set"]
    due_dates = data[workflow]["due_dates"]

    nodes_num = len(due_dates)
    
    node2idx, due_dates_list = {}, []
    for i, node in enumerate(due_dates):
        node2idx[node] = i
        due_dates_list.append(due_dates[node])
        
    
    graph = defaultdict(list)
    for parent, child in edge_set:
        graph[node2idx[parent]].append(node2idx[child])
    graph[nodes_num-1] = []

    node_types = [node for node in node2idx]
    
    process_times = get_process_times(ftime)
    
    return {"graph": graph, "node_types": node_types, "due_dates": due_dates_list, "process_times": process_times}
    
    
if __name__ == "__main__":
    workflow = get_workflow_from_json("/home/ycniu/IC/SRA/70068-cwk-ay2021-22/input.json")
    test = _test_graph()
    
    assert workflow["graph"] == test["graph"]
    assert workflow["node_types"] == test["node_types"]
    assert workflow["due_dates"] == test["due_dates"], (workflow["due_dates"], test["due_dates"])
    # assert task["process_times"] == test["process_times"], (task["process_times"], test["process_times"])
    
