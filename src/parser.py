import optparse

usage = "usage: python3 main.py --runs <num_runs> --scheduler <scheduler_name> --vm <vmname>"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-r", "--runs", action="store", dest="runs", default=1, 
					help="Number of runs for statistical significance")
parser.add_option("-s", "--scheduler", action="store", dest="scheduler", default="sinit", 
					help="Name of the scheduler to run")
parser.add_option("-v", "--vm", action="store", dest="vm", default="vm", 
					help="Name of the VM to run experiments")
opts, args = parser.parse_args()