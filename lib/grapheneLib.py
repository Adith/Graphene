graphList = []
nodeList = []
globalNodeIDVal = 0
globalGraphIDVal = 0

class Node:
# ''' Internal representation of a node object '''
	id = -1
	properties = dict()
	
	def __init__(self, data = None):
		id = ++globalNodeIDVal
		if data is not None:
			id = data["id"]
			properties = data	

	def get_id():
		return id

class Graph:
# ''' Internal representation of a graph object '''
    id = -1
    
    adjList = []
    
    def __init__(self, data = None):
        id = ++globalGraphIDVal
        
        if data is not None:
        	adjList = data

    def get_id():
    	return id
