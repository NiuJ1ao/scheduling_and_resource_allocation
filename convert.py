import json
import csv 
import optparse

usage = "usage: python3 convert.py --fname <name>"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-f", "--fname", action="store", dest="fname", default=1, 
					help="CSV file name to convert to json")
opts, args = parser.parse_args()

nodes = ['onnx_1', 'muse_1', 'emboss_1', 'emboss_2', 'blur_1', 'emboss_3', 'vii_1', 'blur_2', 'wave_1', 'blur_3', 'blur_4', 'emboss_4', 'onnx_2', 'onnx_3', 'blur_5', 'wave_2', 'wave_3', 'wave_4', 'emboss_5', 'onnx_4', 'emboss_6', 'onnx_5', 'vii_2', 'blur_6', 'night_1', 'muse_2', 'emboss_7', 'onnx_6', 'wave_5', 'emboss_8', 'muse_3', 'onnx_7', 'onnx_8', 'wave_6']

with open(f'{opts.fname}.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    vals = list(csv_reader)[0]
    vals = [int(i.strip()) for i in vals]
    print(vals)
    order = [nodes[i - (1 if max(vals) == 34 else 0)] for i in vals]
    dictionary = {'workflow_0': order}
    with open(f"{opts.fname}.json", "w") as outfile:
        json.dump(dictionary, outfile, indent=4)