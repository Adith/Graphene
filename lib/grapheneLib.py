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
import grapheneUI as gui
import ast
import json

graphList = {}
nodeList = {}

chained = False

globalLastNodeIDVal = -1
globalLastGraphIDVal = -1

class modified_dict(dict):
	def __getitem__(self, key):
		try:
			val = dict.__getitem__(self, key)
			logging.debug("Lookup for "+key+" in "+str(self))
			logging.info("Retrieved from local scope")
		except KeyError, e:
			if "__caller_local__" in self.keys():
				val = self["__caller_local__"][key]
				if val != None:
					logging.info("Retrieved from parent scope")
					return val
			if "__global__" in self.keys():
				val = self["__global__"][key]
				if val != None:
					logging.info("Retrieved from global scope")
					return val
			return None
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

	def first(self):
		return super(modified_list, self).__getitem__(0)

	def last(self):
		return super(modified_list, self).__getitem__(-1)

class Node(object):
	'''Internal representation of the node type'''
	def print_data(child):
		for k,v in child.mapping.iteritems():
			print "\t", v, ":", getattr(child, v)
	
	id = -1
	__tags__ = " "
	__cluster__ = None

	def get_data(self,child):
		result = {}
		for a in inspect.getmembers(child, lambda a:not(inspect.isroutine(a))):
			if not(a[0].startswith('__') and a[0].endswith('__')):
				result[a[0]] = a[1]
			result["__tags__"] = child.__tags__
			result["__cluster__"] = child.__cluster__
		return result

def node_init(self, *node_data):
	global globalLastNodeIDVal
	call_from_ui = False
	if isinstance(node_data[0],dict):
		call_from_ui = True
	for k,v in self.mapping.iteritems(): 
		if k > len(node_data):
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
	graph_type = "d"

	clusters = []
	
	# Shadow edge list maintains a mapping of destinations to all sources it is in contact with
	# eg. 	edgeList: 0 <-> 1, 3 -> 1, 4 -> 1
	# 		shadowEdgeList: 1 : {0:None,3:None,4:None}
	shadowEdgeList = {}

	
	def __init__(self, edgeList = None, gtype = 'd', gkey = "id"):
		global globalLastGraphIDVal
		import grapheneHelper as helper
		
		if(isinstance(gkey, ast.ASTNode)):
			gkey = gkey.value # Fix, because this is an ASTNode. :/
		if(isinstance(gtype, ast.ASTNode)):
			gtype = gtype.value # Fix, because this is an ASTNode. :/

		parsed_edgeList = {}
		for source, destinations in edgeList.iteritems():
			for destination, properties in destinations.iteritems():
				destination = helper.get_node_id_from_key_value(destination, gkey)
				source = helper.get_node_id_from_key_value(source, gkey)
				try:
					parsed_edgeList[source][destination] = properties
				except KeyError, e:
					parsed_edgeList[source] = { destination : properties }
		edgeList = parsed_edgeList
		
		self.id = globalLastGraphIDVal + 1
		self.graph_type = gtype
		globalLastGraphIDVal = globalLastGraphIDVal + 1

		if edgeList is not None:
			
			import grapheneHelper as helper
			self.edgeList = dict.copy(edgeList)
			for source, destinations in edgeList.iteritems():
				for destination, properties in destinations.iteritems():
					try:
						self.edgeList[source][destination] = properties
					except KeyError, e:
						self.edgeList[source] = { destination : properties }

					try:
						self.shadowEdgeList[destination][source] = None
					except KeyError, e:
						self.shadowEdgeList[destination] = { source : None }

					
					if(gtype != "d"):
						try:
							self.edgeList[destination][source] = properties
						except KeyError, e:
							self.edgeList[destination] = { source : properties }
	
						try:
							self.shadowEdgeList[source][destination] = None
						except KeyError, e:
							self.shadowEdgeList[source] = { destination : None }

	def overlay(self, overlay_list=None):
		try:
			overlay_node_list = []
			if overlay_list:
				if isinstance(overlay_list, ast.ASTNode):
					for e in overlay_list.value:
						if e.__class__.__bases__[0].__name__ in ["Node"]:
							overlay_node_list.append(e.id)
						else:	
							overlay_node_list.append(e.value)
				else:
					overlay_node_list.append(overlay_list.id)
			else:
				gui.output()
				return

			state = json.loads(open('./proc/state.json', 'r').read())
			node_ref = {}
			for node in state["nodes"]:
				node_ref[node["id"]] = node

			for node_id in overlay_node_list:
				node_ref[node_id]["__tags__"] = node_ref[node_id]["__tags__"] + "active"
			state["attributes"] = {"overlay":True}
			with open('./proc/state.json', 'w') as outfile:
				json.dump(state, outfile)

			gui.output()
		except Exception, e:
			import traceback
			traceback.print_exc()
		

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

	def hasNode(self, node):
		if node.__class__.__bases__[0].__name__ not in ["Node"]:
			if(isinstance(node, list)):
				node = node[0]
			else:
				try:
					node = nodeList[node]
				except KeyError, e:
					logging.error("Node not found")
					gexit()
				except Exception, e:
					logging.error("Illegal Lookup")
					gexit()

		if node in self.getNodes():
			return True
		return False

	def hasEdge(self, src, dst):
		src_id = src[0].id
		dst_id = dst[0].id
		try:
			if(dst_id in self.edgeList[src_id]):
				return True
			return False
		except Exception, e:
			return False

	def inDegree(self, node):
		if isinstance(node,list):
			node_id = node[0].id
		else:
			node_id = node

		try:
			return len(self.shadowEdgeList[node_id].keys())
		except Exception, e:
			return 0

	def outDegree(self, node):
		if isinstance(node,list):
			node_id = node[0].id
		else:
			node_id = node

		try:
			return len(self.edgeList[node_id].keys())
		except Exception, e:
			return 0

	def degree(self, node):
		if isinstance(node,list):
			node_id = node[0].id
		else:
			node_id = node

		if self.graph_type == "d":
			return self.inDegree(node_id) + self.outDegree(node_id)
		else:
			return self.outDegree(node_id)

	def getAdjacent(self, node):
		adjacent = modified_list()
		if(isinstance(node,list)):
			node =  ast.evaluateAST(node)[0]
		if node.id in self.shadowEdgeList:
			for adjacent_id in self.shadowEdgeList[node.id]:
				adjacent.append(nodeList[adjacent_id])
		if node.id in self.edgeList:
			for adjacent_id in self.edgeList[node.id]:
				adjacent.append(nodeList[adjacent_id])
		return adjacent

	def getNonAdjacent(self,node):
		all_nodes = self.getNodes()
		adjacent = self.getAdjacent(node)
		adjacent.extend(node) 
		return [item for item in all_nodes if item not in adjacent]

	def listAdjacent(self, node):
		nodes = self.getAdjacent(node)
		ret = modified_list()
		for node in nodes:
			ret.append(node.id)
		return ret

	# Print to console
	def print_data(self):
		for k,v in self.edgeList.iteritems():
			print '\n\tNode(',k,')', 
			first = True
			for k1,v1 in v.iteritems():
				if first:
					print v1["__connector__"],'Node(',k1,')'
					first = False
				else:
					print "\t\t   ",v1["__connector__"],'Node(',k1,')'
				for k2,v2 in v1.iteritems():
					if k2 in ["__connector__"]:
						continue
					print "\t\t",k2,':',v2
	# DFS
	# def listAdjacent(self,node):
	# 	a = [adj for adj in self.edgelist[node].keys()]
	# 	return a

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

	def edgeHasProperty(self, source, target, property):
		try:
		 if self.edgeList[source.id][target.id][property[0]] == property[1] :
			return True
		 else:
			return False
		except KeyError:
			return False

	def findconnections(self,root,properties):
		results = []
		for node in edgelist[root]:
			if {properties[0]:properties[1]} in node[node.keys()[0]]:
				results.append(node.keys()[0])
		print results

	def mockFuncCall(self,fname,fargs):
	    node = ast.ASTNode()
	    node.type = "funccall"
	    node.children.append(fname)

	    arglistNode = ast.ASTNode()
	    arglistNode.type = "arglist"
	 
	    for arg in fargs:
	        node0 = ast.ASTNode()
	        node0.type = "terminal"
	        node0.value=arg
	        #node0.children.append(arg.get_data()['name'])
	        arglistNode.children.append(node0)

	    node.children.append(arglistNode)
	    return node

	def cluster(self,lamda):
	    global chained
	    import grapheneHelper as helper
	    clusters = []
	    
	    nodes = self.getNodes()
	  
	    if ast.evaluateAST(self.mockFuncCall(lamda.children[3],[nodes[0],nodes[1]])).value:
	        clusters.append([nodes[0],nodes[1]])
	    else:
	        clusters.append([nodes[0]])
	        clusters.append([nodes[1]])
	    
	    nodes = nodes[2:]
	    for node in nodes:
	        cluster_ids = []
	        index = 0 
	        for cluster in clusters:
	            #if lamda(node,cluster[0]):
	            if ast.evaluateAST(self.mockFuncCall(lamda.children[3],[node,cluster[0]])).value:
	                cluster.append(node)
	                cluster_ids.append(index)
	            index+=1
	        if len(cluster_ids)==0:
	            clusters.append([node])

	        # Merge all clusters a node belongs to
	        if len(cluster_ids)>1:
	            clusters[cluster_ids[0]] = list(set(clusters[cluster_ids]))
	            for ind in range(1,len(cluster_ids)):
	                clusters[ind]=None
	        clusters = filter(lambda a: a != None, clusters)
	    #print '+++++',len(clusters),'++++++'

	    index=0
	    for cluster in clusters:
	        for node in cluster: 
	            #print lib.nodeList[node.get_data()['id']].get_data()
	            nodeList[node.id].__cluster__ = index
	            node.__cluster__=index
	        index+=1
	    #print nodeList
	    
	    if chained:
	    	helper.goutput(self)
	    return self

    # # Cluster Nodes
    # def cluster_data(self):
    # 	clusters = [] 
    # 	while self.edgeList:
    # 		graph = self.__init__()

      
