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
    
    edgeList = []
    
    def __init__(self, data = None):
        id = ++globalGraphIDVal
        
        if data is not None:
        	edgeList = data

    def get_id():
    	return id

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


