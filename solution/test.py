from lcl_rule import least_cost_last
from tabu_search import tabu_search, read_init_schedule
from my_utils import get_workflow_from_json

def test_lsl():
    workflow = get_workflow_from_json("/home/ycniu/IC/SRA/70068-cwk-ay2021-22/input.json", "/home/ycniu/IC/SRA/70068-cwk-ay2021-22/process_times.txt")
    graph = workflow["graph"]
    optimal_schedule, _, _ = least_cost_last(workflow)
    assert len(optimal_schedule) == 34, "schedule length does not match"
    assert len(optimal_schedule) == len(set(optimal_schedule)), "Repeat job in schedule"
    for i, job in enumerate(optimal_schedule):
        successors = graph[job-1]
        for s in successors:
            assert s + 1 in optimal_schedule[i], "child not find in subschdule after parent"

def test_tabu():
    init_s = read_init_schedule()
    workflow = get_workflow_from_json("/home/ycniu/IC/SRA/70068-cwk-ay2021-22/input.json", "/home/ycniu/IC/SRA/70068-cwk-ay2021-22/process_times.txt")
    graph = workflow["graph"]
    optimal_schedule, _, _ = tabu_search(workflow, init_s=init_s, iter_num=10, tabu_size=5, gamma=30)
    assert len(optimal_schedule) == 34, f"schedule length does not match, {len(optimal_schedule)}"
    assert len(optimal_schedule) == len(set(optimal_schedule)), "Repeat job in schedule"
    for i, job in enumerate(optimal_schedule):
        successors = graph[job-1]
        for s in successors:
            assert s + 1 in optimal_schedule[i+1:], "child not find in subschdule after parent"

    
    optimal_schedule, _, _ = tabu_search(workflow, init_s=init_s, iter_num=100, tabu_size=5, gamma=30)
    assert len(optimal_schedule) == 34, "schedule length does not match"
    assert len(optimal_schedule) == len(set(optimal_schedule)), "Repeat job in schedule"
    for i, job in enumerate(optimal_schedule):
        successors = graph[job-1]
        for s in successors:
            assert s + 1 in optimal_schedule[i+1:], "child not find in subschdule after parent"
    
    optimal_schedule, _, _ = tabu_search(workflow, init_s=init_s, iter_num=1000, tabu_size=5, gamma=30)
    assert len(optimal_schedule) == 34, "schedule length does not match"
    assert len(optimal_schedule) == len(set(optimal_schedule)), "Repeat job in schedule"
    for i, job in enumerate(optimal_schedule):
        successors = graph[job-1]
        for s in successors:
            assert s + 1 in optimal_schedule[i+1:], "child not find in subschdule after parent"

def test_tabu_2():
    # [3, 4, 5, 7]
    node_types = {0: 'onnx_1_', 1: 'muse_1_', 2: 'emboss_1', 3: 'wave_5'}
    process_times = {"onnx": 16, "muse": 11, "emboss": 4, "wave": 8}
    due_dates = {0: 1, 1: 2, 2: 7, 3: 9}
    workflow = {"node_types": node_types, "process_times": process_times, "due_dates": due_dates}
    s = tabu_search(workflow, [3,1,0,2], 4, 2, 20)
    print(s)
    
def test_tabu_3():
    # [14, 12, 1, 12]
    node_types = {0: 'onnx_1_', 1: 'muse_1_', 2: 'emboss_1', 3: 'wave_5'}
    process_times = {"onnx": 10, "muse": 10, "emboss": 13, "wave": 4}
    due_dates = {0: 4, 1: 2, 2: 1, 3: 12}
    workflow = {"node_types": node_types, "process_times": process_times, "due_dates": due_dates}
    s = tabu_search(workflow, [1,0,3,2], 3, 2, 100)
    print(s)
    
if __name__ == '__main__':
    # test_lsl()
    # test_tabu()
    test_tabu_3()
