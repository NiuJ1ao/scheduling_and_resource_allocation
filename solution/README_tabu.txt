## Prerequisite
This code runs Python 3.8 with the following libraries:
- numpy
pip install numpy
- tabulate (optional)
pip install tabulate

## Run
python tabu_search.py \
--dump_schedule \
--workflow_file input.json --process_time_file process_times.txt --init_schedule_file sinit.csv \
-i 10 -t 5 -g 30
