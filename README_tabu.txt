## Prerequisite
This code runs Python 3.8 with the following libraries:
- numpy
pip install numpy
- tabulate (optional)
pip install tabulate

## Run
python tabu_search.py \
--workflow_file input.json --process_time_file process_times.txt --dump_schedule \
-i 10 -t 5 -g 100

