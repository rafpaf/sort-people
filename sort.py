import networkx as nx
import csv
import sys

quit_now = False
try:
    prefs_file = sys.argv[1]
except IndexError:
    quit_now = True
    print("Please specify a CSV filename containing people's preferences as the first parameter")

try:
    capacities_file = sys.argv[2]
except IndexError:
    quit_now = True
    print("Please specify a CSV filename listing the maximum sizes of the groups as the second parameter")

try:
    costs_str = sys.argv[3]
except IndexError:
    quit_now = True
    print("Please specify the costs of assigning non-first choices as the third parameter, e.g. -100,50,100,200 means that first choices have a negative cost of -100, and the costs of assigning second, third and fourth choices are 50, 100, and 200 respectively")

if quit_now:
    exit()

reader = csv.reader(open(prefs_file, 'r'))
prefs = {}
for row in reader:
    prefs[row[0]] = row[1:]
del reader

reader = csv.reader(open(capacities_file, 'r'))
capacities = {}
for row in reader:
    capacities[row[0]] = int(row[1])

costs = [int(x) for x in costs_str.split(',')]

G=nx.DiGraph()

num_persons=len(prefs)
G.add_node('dest',demand=num_persons)
A=[]
for person,projectlist in prefs.items():
    G.add_node(person,demand=-1)
    for i,project in enumerate(projectlist):
        cost = costs[i]
        G.add_edge(person,project,capacity=1,weight=cost) # Edge taken if person does this project

for project,c in capacities.items():
        G.add_edge(project,'dest',capacity=c,weight=0)

flowdict = nx.min_cost_flow(G)
for person in prefs:
    for project,flow in flowdict[person].items():
        if flow:
            print person,'joins',project
