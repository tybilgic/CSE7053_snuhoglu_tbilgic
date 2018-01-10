import csv
import networkx as nx
from igraph import *

def prepareGraph(nodes, relations):
  graph = nx.DiGraph()
  for node in nodes:
    graph.add_node(node['id'])
  for relation in relations:
    if graph.has_edge(relation['from'], relation['to']):
        graph[relation['from']][relation['to']]['weight'] += relation['pts']
    else:
        graph.add_edge(relation['from'], relation['to'], weight=relation['pts'])
  return graph

def employeeReader():
  nodes = []
  file = open('./nodes.csv', 'r')
  reader = csv.reader(file)
  for ln in reader:
    nodes.append({'id': int(ln[0]), 'deptName': ln[1], 'deptId': int(ln[2]), 'man': (ln[3]=='true'), 'manId': int(ln[4]), 'parentDeptId': int(ln[5])})
  return nodes

def relationsReader(type):
  relations = []
  file = open('./' + type + '.csv','r')
  reader = csv.reader(file)
  for ln in reader:
    relations.append({'id': int(ln[0]), 'from': int(ln[1]), 'to': int(ln[2]), 'type': type, 'pts': int(ln[3])})
  return relations

def centralities(graph, nodes, doPrint):
  undGraph = nx.Graph();
  edges = list(graph.edges())
  for e in edges:
      undGraph.add_edge(e[0], e[1])
  if doPrint:
    print('Betweenness Centrality')
    print(nx.betweenness_centrality(undGraph))
    print('Closeness Centrality')
    print(nx.closeness_centrality(undGraph))
    print('Degree Centrality')
    print(nx.degree_centrality(undGraph))
    print('Eigenvector Centrality')
    print(nx.eigenvector_centrality(undGraph))

def drawGraph(nodes, relations):
  g = Graph(directed=True)
  for node in nodes:
    if node['man']:
      g.add_vertex(name=node['id'], label=node['id'], employee="Man", color="blue")
    else:
      g.add_vertex(name=node['id'], label=node['id'], employee="Emp", color="white")
  for relation in relations:
    if (g.get_eid(relation['from'], relation['to'], directed=True, error=False) == -1):
      g.add_edge(relation['from'], relation['to'])
      eid = g.get_eid(relation['from'], relation['to'])
      edge = g.es[eid]
      edge["weight"] = 1
    else:
      eid = g.get_eid(relation['from'], relation['to'])
      edge = g.es[eid]
      edge["weight"] += 1
  layout = g.layout_auto()
  g.vs["label"] = g.vs["name"]
  visual_style = {}
  plot(g, **visual_style)
  return true

nodes = employeeReader()
takdirs = relationsReader('takdir')
tesekkurs = relationsReader('tesekkur')
dogumgunus = relationsReader('dogumgunu')

takdirGraph = prepareGraph(nodes, takdirs)
tesekkurGraph = prepareGraph(nodes, tesekkurs)
dogumgunuGraph = prepareGraph(nodes, dogumgunus)

print('Calculating centrality metrics for takdir relation')
centralities(takdirGraph, nodes, True)
print('Calculating centrality metrics for tesekkur relation')
centralities(tesekkurGraph, nodes, True)
print('Calculating centrality metrics for dogumgunu relation')
centralities(dogumgunuGraph, nodes, True)
#drawGraph(nodes, takdirs)
