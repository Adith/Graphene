# -*- coding: UTF-8 -*-

 # ██╗     ██╗██████╗ 
 # ██║     ██║██╔══██╗
 # ██║     ██║██████╔╝
 # ██║     ██║██╔══██╗
 # ███████╗██║██████╔╝
 # ╚══════╝╚═╝╚═════╝ 

import copy
from collections import namedtuple

graphList = []
nodeList = []

globalLastNodeIDVal = 0
globalLastGraphIDVal = 0

# class Node(namedtuple('Node', ['value', 'left', 'right'])):
#     def __new__(cls, value=None, left=None, right=None):
#         return super(Node, cls).__new__(cls, value, left, right)

class Node(object):
	'''Internal representation of the node type'''
	def print_data(child):
		print "\tid : ",child.id
		for k,v in child.mapping.iteritems():
			print "\t", v, ":", getattr(child, v)
	
	id = -1

	def inc_id(self, child):
		global globalLastNodeIDVal
		child.id = globalLastNodeIDVal + 1
		globalLastNodeIDVal = globalLastNodeIDVal + 1


def node_init(self, *args):
	for k,v in self.mapping.iteritems():
		if k > len(args)-1:
			break
		setattr(self,v,args[k])
	Node().inc_id(self)

class Graph:
# ''' Internal representation of a graph object '''
    id = -1
    
    edgeList = {}

    def __init__(self, data = None):
    	global globalGraphIDVal
        self.id = globalGraphIDVal + 1
        globalGraphIDVal = globalGraphIDVal + 1
        
        if data is not None:
       		self.edgeList.extend(data)

    def get_id(self):
    	return self.id

    def get_list(self):
    	return self.edgeList

    # Print to console
    def print_data(self):
    	print edgeList


# OO dropped by design choice in favor of python ease of dict use
# class Edge:

# 	src = -1
# 	dst = -1

# 	properties = dict()

# 	def __init__(self, srcD = None, dstD = None, data = None):
# 		if data is not None:
# 			src = srcD
# 			dst = dstD
# 			properties = data

# 	def get_prop():
# 		return properties

# 	def get_src():
# 		return src

# 	def get_dst():
# 		return dst
