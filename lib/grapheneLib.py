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

class Node(object):
	'''Internal representation of the node type'''
	def print_data(child):
		print "\t","ID:", child.id
		for k,v in child.mapping.iteritems():
			print "\t", v, ":", getattr(child, v)
	
	id = -1

	def inc_id(self, child):
		global globalLastNodeIDVal
		child.id = globalLastNodeIDVal + 1
		globalLastNodeIDVal = globalLastNodeIDVal + 1

	def get_data(self,child):
		return child.__dict__

def node_init(self, *args):

	for k,v in self.mapping.iteritems():
		if k > len(args)-1:
			break
		setattr(self,v,args[k])
	Node().inc_id(self)

class Graph:
	''' Internal representation of a graph object '''
	id = -1
	
	edgeList = {}
	
	def __init__(self, edgeList = None, gtype = 'd', gkey = "id"):
		global globalLastGraphIDVal
		
		self.id = globalLastGraphIDVal + 1
		globalLastGraphIDVal = globalLastGraphIDVal + 1
		
		if edgeList is not None:
			self.edgeList = dict.copy(edgeList)

	def get_id(self):
		return self.id

	def get_data(self):
		return self.edgeList

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
