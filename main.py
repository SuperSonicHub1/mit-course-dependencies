import networkx as nx
from networkx import DiGraph
from pprint import pprint
import matplotlib.pyplot as plt
from pathlib import Path
import json
from itertools import combinations, chain
from typing import Iterable, Dict, Any

G = DiGraph()

def list_reqs() -> Iterable[Dict[str, Any]]:
	for path in (Path.cwd() / "requirements").glob("*.json"):
		with path.open() as f:
			yield json.load(f)

def handle_requirements(requirements: dict | list, G: DiGraph, parent: str, subset: int):
	if 'reqs' in requirements:
		reqs = requirements['reqs']
		
		if isinstance(reqs, list):
			for req in reqs:
				handle_requirements(req, G, parent, subset + 1)
		else:
			connection_type = reqs['connection-type']
			handle_requirements(reqs, G, parent, subset + 1)
	elif 'req' in requirements:
		req = requirements['req']
		G.add_node(req, subset=subset)
		G.add_edge(parent, req)

for requirements in list_reqs():
	parent = requirements['title']
	G.add_node(parent, subset=0)
	handle_requirements(requirements, G, parent, 1)

intersecting_courses = []

for major_l, major_r in combinations((node for node in G.nodes if not G.in_degree(node)), 2):
	if (major_l in major_r) or (major_r in major_l):
		continue
	common_classes = set(G.successors(major_l)).intersection(set(G.successors(major_r)))
	if common_classes:
		intersecting_courses.append((major_l, major_r, common_classes))

for major_l, major_r, common_classes in sorted(intersecting_courses, key=lambda x: len(x[2]), reverse=True):
	print(f'{major_l} & {major_r} with {len(common_classes)} common classes: ', common_classes)

# bachelors = ["Bachelor of Science in Computation and Cognition", "Bachelor of Science in Electrical Engineering and Computer Science"]
# masters = ["Master of Engineering in Computation and Cognition", "Master of Engineering in Electrical Engineering and Computer Science"]

# degrees = bachelors + masters

# sub_graph = G.subgraph(degrees + list(chain.from_iterable(G.successors(degree) for degree in degrees)))

# shells = [
# 	[node for node, subset in sub_graph.nodes(data='subset') if subset == i]
# 	for i
# 	in range(8)
# ]

# # https://stackoverflow.com/questions/27030473/how-to-set-colors-for-nodes-in-networkx
# color_map = ['red' if sub_graph.in_degree(node) > 1 else 'blue' for node in sub_graph.nodes]

# # pos = nx.multipartite_layout(sub_graph, scale=10, align='horizontal')
# pos = nx.shell_layout(G, nlist=shells, scale=100)
# nx.draw_networkx(sub_graph, pos=pos, node_color=color_map, font_color='green', edge_color='gray')
# plt.show()
