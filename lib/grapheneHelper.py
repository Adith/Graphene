import grapheneLib as lib
import ast
import string
import logging
import json
import random
import grapheneUI as gui
import sys

ids=lib.modified_dict()

def gexit():
    sys.exit(0)

def gprint(*node):
    logging.debug('******print******')
    for e in node:
        if(isinstance(e,ast.ASTNode)):
            e = ast.evaluateAST(e)
        if type(e).__bases__[0].__name__ in ["Node"]:
            print "Node has"
            e.print_data();
        elif isinstance(e, lib.Graph):
            print "Graph has {"
            e.print_data();
            print "}"
        elif isinstance(e,list):
            for v in e:
                if isinstance(v, ast.ASTNode):
                    gprint(ast.evaluateAST(v).value)
                else:
                    gprint(v)
        else:
            try:
                print ast.evaluateAST(e)
            except Exception, e:
                logging.error("Unknown expression")
                gexit()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def ginput(*args):
    if len(args)==2:
        #########################################
        try:
            f = open(args[1],'r')
        except Exception, e:
            logging.error("File Not Found.")
            gexit()
            
        lines = f.readlines()
        f.close()
        finalEdgeList = dict()
        nodes = {}
        number_of_nodes = len(lib.nodeList)
    
        for i,line in enumerate(lines):
            properties = {}
            edgeF, edgeT = [int(x) for x in line.split()]
            
            properties["__connector__"] = "->"
            if edgeF not in lib.nodeList.keys():
                lib.nodeList[edgeF] = func_map[args[0]](id_generator(), id_generator())
                lib.nodeList[edgeF].id = edgeF
            if edgeT not in lib.nodeList.keys():
                lib.nodeList[edgeT] = func_map[args[0]](id_generator(), id_generator())
                lib.nodeList[edgeT].id = edgeT
            try:
                finalEdgeList[edgeF][edgeT] = properties
            except KeyError:
                finalEdgeList[edgeF] = {edgeT : properties}
        
        lib.graphList[len(lib.graphList)] = lib.Graph(finalEdgeList)
        print "One graph and",len(lib.nodeList)-number_of_nodes,"nodes touched."

        
        #########################################
    elif len(args)==0:
        input = json.loads(gui.input())
        lib.graphList[len(lib.graphList)] = lib.Graph(outToInLinks(input['links']))

        # Unfortunately, we have to decide whether to create a template node class or one for EVERY node in input. This one does the former.
        template_node_class = type("template", (lib.Node,), dict(((k,None) for k,v in input["nodes"][0].iteritems()),__init__=lib.node_init, print_data=lambda self:lib.Node.print_data(self), get_data= lambda self: lib.Node().get_data(self), mapping=dict((i,el) for i,el in enumerate(input["nodes"][0]))))
    
        for k in input['nodes']:
            lib.nodeList[k["id"]] = template_node_class(k);

        print "One graph and",len(input["nodes"]),"nodes touched."
        logging.debug(lib.nodeList)
        logging.debug(lib.graphList)
        logging.debug(outToInLinks(input['links']))
    else:
        logging.error("Input takes 0 arguments for input from user, or 3 for input from file <node_type, file>.")
        gexit()
    return lib.graphList[len(lib.graphList)-1]

def goutput(graph=None, chained=False):
    # Prints state to D3
    # Note: state = ALL graphs

    # Dump state to json
    nodes = []
    graphs = []
    if graph == None:
        nodes = inToOutNodes(lib.nodeList)
        for k,g in lib.graphList.iteritems():
            graphs.extend(inToOutLinks(g.get_data()))
    else:
        graphs.extend(inToOutLinks(graph.get_data()))
        g = graph.get_data()
        graph_nodelist = {}
        for source, destinations in g.iteritems():
            graph_nodelist[source] = lib.nodeList[source]
            for destination, properties in destinations.iteritems():
                graph_nodelist[destination] = lib.nodeList[destination]

        nodes = inToOutNodes(graph_nodelist)

    # Nodes and Links converted from IR to json
    logging.debug("nodes:"+str(nodes))
    logging.debug("links:"+str(graphs))

    # Dump json to file
    with open('./proc/state.json', 'w') as outfile:
         json.dump({"nodes":nodes, "lastNodeId": len(nodes)-1, "links": graphs}, outfile)

    if not chained:
        gui.output()
    return_val = lib.Graph(outToInLinks(graphs))
    lib.globalLastGraphIDVal = lib.globalLastGraphIDVal - 1

    return return_val

def gcluster(graph,lamda):
    clusters = []
    #lamda = lambda x,y:x.get_data()['age']==y.get_data()['age']
    nodes = graph.getNodes()
    for n in nodes:
        print n.get_data()

    if lamda(nodes[0],nodes[1]):
        clusters.append([nodes[0],nodes[1]])
    else:
        clusters.append([nodes[0]])
        clusters.append([nodes[1]])
    print clusters
    nodes = nodes[2:]
    for node in nodes:
        cluster_ids = []
        index = 0 
        for cluster in clusters:
            if lamda(node,cluster[0]):
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
    print len(clusters)
    index=0
    for cluster in clusters:
        for node in cluster: 
            #print lib.nodeList[node.get_data()['id']].get_data()
            node.__cluster__=index
        index+=1
    #print nodeList
    return clusters

func_map = {'input' : ginput, 'output' : goutput,  'print' : gprint, 'exit': gexit, 'cluster': gcluster}


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
    print ids
    if "__caller_local__" in ids.keys():
        __global = ids["__global__"]
        ids = ids["__caller_local__"]
        ids["__global__"] = __global
    else:
        ids = ids["__global__"]
    print ids
    
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
    