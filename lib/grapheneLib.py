# -*- coding: UTF-8 -*-

# ██╗     ██╗██████╗ 
# ██║     ██║██╔══██╗
# ██║     ██║██████╔╝
# ██║     ██║██╔══██╗
# ███████╗██║██████╔╝
# ╚══════╝╚═╝╚═════╝ 
                   
import copy

graphList = []
nodeList = []
globalNodeIDVal = 0
globalGraphIDVal = 0

class Node:
# ''' Internal representation of a node object '''
	id = -1
	properties = dict()
	
	def __init__(self, data = None):
		global globalNodeIDVal
		self.id = globalNodeIDVal + 1
		globalNodeIDVal = globalNodeIDVal + 1
		if data is not None:
			self.id = data["id"]
			self.properties = dict.copy(data)

	def get_id(self):
		return self.id

	def get_prop(self):
		return self.properties

class Graph:
# ''' Internal representation of a graph object '''
    id = -1
    
    edgeList = []
    
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
