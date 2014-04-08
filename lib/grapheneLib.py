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
    
    adjList = []
    
    def __init__(self, data = None):
    	global globalGraphIDVal
        self.id = globalGraphIDVal + 1
        globalGraphIDVal = globalGraphIDVal + 1
        
        if data is not None:
        	self.adjList.append(data)

    def get_id(self):
    	return self.id

    def get_list(self):
    	return self.adjList
