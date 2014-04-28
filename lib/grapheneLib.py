# -*- coding: UTF-8 -*-

 # ██╗     ██╗██████╗ 
 # ██║     ██║██╔══██╗
 # ██║     ██║██████╔╝
 # ██║     ██║██╔══██╗
 # ███████╗██║██████╔╝
 # ╚══════╝╚═╝╚═════╝ 

import copy
from collections import namedtuple
import logging
import inspect

graphList = {}
nodeList = {}

globalLastNodeIDVal = -1
globalLastGraphIDVal = -1

class modified_dict(dict):
	def __getitem__(self, key):
		try:
			val = dict.__getitem__(self, key)
			logging.debug("Lookup for "+key+" in "+str(self))
			logging.info("Retrieved from local scope")
		except KeyError, e:
			if "__global__" in self.keys():
				val = self["__global__"][key]
				logging.info("Retrieved from global scope")
			else:
				raise KeyError
		return val

class modified_list(list):
	def __init__(self,arg = None):
		self.len = 0
		if arg!=None:
			super(modified_list, self).extend(arg)
			self.len = len(arg)

	def append(self,item):
		if isinstance(item,list):
			for i in item:
				super(modified_list, self).append(i)
		else:
			super(modified_list, self).append(item)
		self.len = self.len + 1

	def length(self):
		return self.len

class Node(object):
	'''Internal representation of the node type'''
	def print_data(child):
		print "\t","ID:", child.id
		for k,v in child.mapping.iteritems():
			print "\t", v, ":", getattr(child, v)
	
	id = -1

	def get_data(self,child):
		result = {}
		for a in inspect.getmembers(child, lambda a:not(inspect.isroutine(a))):
			if not(a[0].startswith('__') and a[0].endswith('__')):
				result[a[0]] = a[1]
		return result

def node_init(self, *node_data):
	global globalLastNodeIDVal
	call_from_ui = False
	if isinstance(node_data[0],dict):
		call_from_ui = True
	for k,v in self.mapping.iteritems():
		if k > len(node_data)-1:
			break
		if call_from_ui:
			setattr(self,v,node_data[0][v])
		else:
			setattr(self,v,node_data[k])
	self.id = globalLastNodeIDVal + 1
	globalLastNodeIDVal = globalLastNodeIDVal + 1

class Graph:
	''' Internal representation of a graph object '''
	id = -1
	
	edgeList = {}

	clusters = []
	
	# Shadow edge list maintains a mapping of destinations to all sources it is in contact with
	# eg. 	edgeList: 0 <-> 1, 3 -> 1, 4 -> 1
	# 		shadowEdgeList: 1 : {0:None,3:None,4:None}
	shadowEdgeList = {}

	
	def __init__(self, edgeList = None, gtype = 'd', gkey = "id"):
		global globalLastGraphIDVal
		
		self.id = globalLastGraphIDVal
		globalLastGraphIDVal = globalLastGraphIDVal + 1

		if edgeList is not None:
			self.edgeList = dict.copy(edgeList)
			for source, destinations in edgeList.iteritems():
				for destination, properties in destinations.iteritems():
					try:
						self.shadowEdgeList[destination][source] = None
					except KeyError, e:
						self.shadowEdgeList[destination] = { source : None }


	def get_id(self):
		return self.id

	def get_data(self):
		return self.edgeList

	def get_shadow(self):
		return self.shadowEdgeList

	def getNodes(self):
		nodeIds = modified_list()
		for n in self.edgeList:
			if n not in nodeIds:
				nodeIds.append(n)
		for n in self.shadowEdgeList:
			if n not in nodeIds:
				nodeIds.append(n)
		nodes = modified_list()
		for n in nodeIds:
			nodes.append(nodeList[n])
		return nodes

	def getAdjacent(self, node):
		adjacent = []
		if node in self.shadowEdgeList:
			for adjacent_id in self.shadowEdgeList[node]:
				adjacent.append(nodeList[adjacent_id])
		if node in self.edgeList:
			for adjacent_id in self.edgeList[node]:
				adjacent.append(nodeList[adjacent_id])
		return adjacent

	# Print to console
	def print_data(self):
		for k,v in self.edgeList.iteritems():
			print '\tNode(',k,')', 
			for k1,v1 in v.iteritems():
				print v1["__connector__"],'Node(',k1,')'
				for k2,v2 in v1.iteritems():
					if k2 in ["__connector__"]:
						continue
					print "\t\t",k2,':',v2
	# DFS
	def listAdjacent(self,node):
		a = [adj for adj in self.edgelist[node].keys()]
		return a

	def cluster_data(self):
		clusters = []
		edges_copy = copy.deepcopy(self.edgeList)
		while len(edges_copy.keys()):
			randombegin = edges_copy.keys()[0]
			queue = [randombegin]
			cluster_instance = [randombegin]
			while len(queue):
				for item in queue:
					if item in edges_copy.keys():
						queue.extend(edges_copy[item].keys())
						cluster_instance.extend(edges_copy[item].keys())
						edges_copy.pop(item)
					queue.remove(item)
			clusters.append(cluster_instance)

		return clusters

    # # Cluster Nodes
    # def cluster_data(self):
    # 	clusters = [] 
    # 	while self.edgeList:
    # 		graph = self.__init__()

      
