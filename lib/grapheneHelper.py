import grapheneLib as lib

ids=lib.modified_dict()

def scope_in():
    global ids
    if "__global__" in ids.keys():
        caller_local = lib.modified_dict(ids)
        caller_local.pop("__global__", None)
        ids = lib.modified_dict({"__global__": ids["__global__"], "__caller_local__" : caller_local})
    else:
        ids = lib.modified_dict({"__global__": ids})
    
def scope_out():
    global ids
    if "__caller_local__" in ids.keys():
        __global = ids["__global__"]
        ids = ids["__caller_local__"]
        ids["__global__"] = __global
    else:
        ids = ids["__global__"]
    
# output format to internal representation
# Depracated in favor of copy constructor
#
# def outToInNodes(nodes):
#     final =dict()
#     for node in nodes:
#         final[node['id']] = node
#     return final

def outToInLinks(links):
    final = dict()
    for link in links:
        properties = {}
        for k,v in link.iteritems():
            if k not in ["source","target","left","right"]:
                properties[k] = v
        if link["left"] == True:
            properties["__connector__"] = "<->"
        else:
            properties["__connector__"] = "->"
        try:
            final[link['source']][link['target']] = (properties)
        except KeyError:
            final[link['source']] = {link['target'] : properties}
    return final


#internal representation to output

def inToOutNodes(nodeL):
    finalStr =[]
    for id,node in nodeL.iteritems():
        finalStr.append(node.get_data())
    return finalStr

def inToOutLinks(sources):
    links = []
    for source, targets in sources.iteritems():
        for target,properties in targets.iteritems():
            link = {'source': int(source), 'target' :int(target), 'right':True }
            if properties["__connector__"] == "<->":
                link["left"] = True
            else:
                link["left"] = False

            for k,v in properties.iteritems():
                link[k] = v
            if "weight" not in link.keys():
                link["weight"] = ''
            links.append(link)
    return links

def completeCodeStmt(str):
    qcount = 0
    pcount = 0
    for c in str:
        if c == '"':
            qcount += 1
        elif qcount%2 == 0:
            if c == '{':
                pcount += 1
            elif c == '}':
                pcount -= 1
    if qcount%2 == 0 and pcount==0:
        return True
    return False 
    