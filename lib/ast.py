import logging
import sys

function=dict()

class Terminal(object):
    def __init__(self):
        self.id = None
        self.val = None
    

class ASTNode(object):
    def __init__(self):
        self.children = []
        self.chain_next = None
        self.properties = dict()
        self.isLeaf = False

    
def printTree(a):
    print len(a.children), "children"
    for x in a.children:
        print type(x), x
        if(isinstance(x, ASTNode)):
            print type(x)
            printTree(x)

def evaluateAST(a, lineno= "unknown", chained= False):
    global ids
    import grapheneLib as lib
    import grapheneHelper as helper

    if(isinstance(a,basestring)):
        return a

    if(isinstance(a,int)):
        return a

    if(isinstance(a,float)):
        return a
    
    if(type(a).__bases__[0].__name__ in ["Node"]):
        return a
    
    if(isinstance(a,list)):
        ret = []
        for e in a:
            val = evaluateAST(e, lineno)
            if isinstance(val, ASTNode):
                ret.append(evaluateAST(e, lineno).value)
            else:
                ret.append(val)
        return ret

    logging.debug("Evaluating type: "+str(a.type))

    if(a.type =="statementlist"):
        a.value = []
        logging.debug('Evaluating a list of statements')
        for e in a.children:
            logging.debug('Evaluating a statement in it...')
            evaluateAST(e, lineno)
        return a

    if(a.type == "terminal"):
        logging.debug("Terminal value: "+str(a.value))
        return a

    # if(a.type == "values"):
    #     logging.debug("Terminal value: "+str(a.value))
        # return a

    if a.type == "lambda":
        for child in a.children:
            print child.type
        return

    if a.type == "lamdaassign":
        print a.children[0], evaluateAST(a.children[1], lineno)
        function[a.children[0]]=a.children[1]
        print function
        print "lambda assigment"
        return

    if(a.type == "edgelist"):
        a.value = {}
        child_edge_list = {}
        child_edge_list_attr = {}
        child_edge_list_attr["__connector__"] = a.children[1]
        child_edge_list[a.children[2].value] = child_edge_list_attr
        a.value[a.children[0].value] = child_edge_list

        if len(a.children) != 3:
            if a.children[3] != None:
                for i,e in enumerate(evaluateAST(a.children[3], lineno).value):
                    child_edge_list_attr[i] = e

        if len(a.children) == 5:
            for k,v in evaluateAST(a.children[4], lineno).iteritems():
                if k in a.value.keys():
                    for k1,v1 in v.iteritems():
                        a.value[k][k1] = v1
                a.value[k] = v
        return a.value

    if(a.type == "arglist" or a.type == "returnset"):
        logging.debug("------argList | returnset-----")
        node=ASTNode()
        node.type="terminal"
        node.value = []
        for e in a.children:
            node.value.append(evaluateAST(e, lineno).value)
        return node

    if(a.type == "plus"):
        node=ASTNode()
        node.type="terminal"

        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        try:
            node.value=value1+value2
        except TypeError:
            print "Error at line "+str(lineno)+": Unsupported operand types\n"
            sys.exit(-1)

        return node

    if(a.type == "minus"):
        node=ASTNode()
        node.type="terminal"

        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        try:
            node.value=value1-value2
        except TypeError:
            print "Error at line "+str(lineno)+": Unsupported operand types\n"
            sys.exit(-1)

        return node

    if(a.type == "multiply"):
        node=ASTNode()
        node.type="terminal"

        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        try:
            node.value=value1*value2
        except TypeError:
            print "Error at line "+str(lineno)+": Unsupported operand types\n"
            sys.exit(-1)

        return node

    if(a.type == "divide"):
        node=ASTNode()
        node.type="terminal"

        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        try:
            node.value=value1/value2
        except TypeError:
            print "Error at line "+str(lineno)+": Unsupported operand types\n"
            sys.exit(-1)

        return node

    if(a.type == "less"):
        node=ASTNode()
        node.type="terminal"

        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        node.value=value1<value2;
        return node

    if(a.type == "greater"):
        node=ASTNode()
        node.type="terminal"
        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        node.value=value1>value2;
        return node

    if(a.type == "greaterequal"):
        node=ASTNode()
        node.type="terminal"
        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        node.value=value1>=value2;
        return node

    if(a.type == "lessequal"):
        node=ASTNode()
        node.type="terminal"
        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        node.value=value1<=value2;
        return node

    if(a.type == "equal"):
        node=ASTNode()
        node.type="terminal"
        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        node.value=value1==value2;
        return node

    if(a.type == "nequal"):
        node=ASTNode()
        node.type="terminal"
        value1 = evaluateAST(a.children[0], lineno).value
        value2 = evaluateAST(a.children[1], lineno).value

        if value1 is None or value2 is None:
            print "Error at line "+str(lineno)+": Used identifier not defined\n"
            sys.exit(-1)

        node.value=value1!=value2;
        return node

    if(a.type == "land"):
        node=ASTNode()
        node.type="terminal"
        node.value=(evaluateAST(a.children[0], lineno).value)and(evaluateAST(a.children[1], lineno).value);
        return node

    if(a.type == "lor"):
        node=ASTNode()
        node.type="terminal"
        node.value=(evaluateAST(a.children[0], lineno).value)or(evaluateAST(a.children[1], lineno).value);
        return node

    if(a.type == "assignment"):
        logging.debug("------assignment----")
        logging.debug(a.children[0])
        logging.debug(a.children[1])
    
        if (isinstance(a.children[0], ASTNode)):
            for index,i in enumerate(a.children[0].children):
                helper.ids[a.children[0].children[index].children[0]]= evaluateAST(evaluateAST(a.children[1], lineno).value[index], lineno).value                
        else:
            assignmentValue = evaluateAST(a.children[1], lineno).value
            if assignmentValue is None:
                print "Error at line "+str(lineno)+": Used identifier not defined\n"
                sys.exit(-1)
            helper.ids[a.children[0]]= assignmentValue
        logging.info('Assigned '+str(helper.ids[a.children[0]])+' to '+str(a.children[0])+' of type '+str(type(helper.ids[a.children[0]])))
        return

    if(a.type == "addedge"):
        logging.debug("------argEdge-----")
        curr =  helper.ids[a.children[0]].get_data()
        shadow = helper.ids[a.children[0]].get_shadow()
        if a.children[1].value in curr.keys():
            curr[a.children[1].value][a.children[3].value]={"__connector__":a.children[2]}
        else:
            curr[a.children[1].value] = {a.children[3].value : {"__connector__":a.children[2]}}
        try:
            shadow[a.children[3].value][a.children[1].value] = None
        except KeyError, e:
            shadow[a.children[3].value] = { a.children[1].value : None }
        
        helper.ids[a.children[0]].edgeList=curr
        return helper.ids[a.children[0]]

    if(a.type == "removenode"):
        logging.debug("------noderemoval-----")
        links =  helper.ids[a.children[0]].get_data()
        shadow = helper.ids[a.children[0]].get_shadow()

        nodes =  evaluateAST(a.children[1], lineno).value
        for node in nodes:
            node_id_to_be_removed = node.id
            pop_from_shadow = []
            if node_id_to_be_removed in links:
                pop_from_shadow = links[node_id_to_be_removed].keys()
            links.pop(node_id_to_be_removed, None)
            if node_id_to_be_removed in shadow:
                pop_from_links = [] 
                for destination in shadow[node_id_to_be_removed].keys():
                    links[destination].pop(node_id_to_be_removed, None)
                    if len(links[destination]) == 0:
                        pop_from_links.append(destination)
    
                for p in pop_from_links:
                    links.pop(p, None)
                shadow.pop(node_id_to_be_removed, None)
            pop_cleanup = []
            for p in pop_from_shadow:
                shadow[p].pop(node_id_to_be_removed, None)
                if len(shadow[p]) == 0:
                    pop_cleanup.append(p)
            for p in pop_cleanup:
                shadow.pop(p, None)
        helper.ids[a.children[0]].edgeList=links
        helper.ids[a.children[0]].shadowEdgeList=shadow
        return helper.ids[a.children[0]]

    if(a.type == "lookupnode"):
        try:
            result = ASTNode()
            result.type = "terminal"
            nodeSet = []
            result.value = nodeSet
            logging.debug("------lookupnode-----")
            if len(a.children) == 1:
                nodeSet.append(evaluateAST(a.children[0], lineno).value)
            else:
                key =  a.children[0]
                value = evaluateAST(a.children[1], lineno).value
                if key in ["id","ID"]:
                    nodeSet.append(lib.nodeList[value])
                    return result
                key = key.value
                for id,node in lib.nodeList.iteritems():
                    data = node.get_data()
                    if key in data: 
                        if data[key] == value:
                            nodeSet.append(node)
            result.value = nodeSet
            return result
        except KeyError, e:
            logging.critical("Node not found")
            helper.gexit()

    if(a.type == "member_funccall"):
        logging.debug('-----eval: member func_call----')
        
        node = ASTNode()
        node.type = "terminal"
        try:
            if isinstance(helper.ids[a.children[0]],ASTNode):
                if len(a.children) <= 2:
                    node.value = getattr(lib.modified_list(evaluateAST(helper.ids[a.children[0]], lineno)),a.children[1])()
                else: 
                    node.value = getattr(helper.ids[a.children[0]].value,a.children[1])(evaluateAST(a.children[2], lineno).value)
            else:
                if len(a.children) <= 2:
                    try:
                        node.value = getattr(helper.ids[a.children[0]],a.children[1].children[0])()
                    except Exception, e:
                        node.value = getattr(helper.ids[a.children[0]],a.children[1])()
                    # node.value = getattr(helper.ids[a.children[0]],a.children[1])()
                else:
                    node.value = getattr(helper.ids[a.children[0]],a.children[1])(*evaluateAST(a.children[2], lineno).value)

            return node
        except KeyError, e:
            logging.error("Unknown variable"+str(a.children[0]))
            helper.gexit()

        logging.info('Assigned '+str(helper.ids[a.children[0]])+' to '+str(a.children[0]))
        return

    if(a.type == "listassignment"):
        logging.debug("--- list assignment ---")
        listValues = lib.modified_list()

        if len(a.children[1].children) == 0:
            temp = evaluateAST(a.children[1], lineno).value
            for t in temp:

                if t.type == "terminal":
                    listValues.append(t) 

                if t.type == "id" and isinstance(evaluateAST(t, lineno).value,ASTNode):
                    if isinstance(evaluateAST(t, lineno).value.value,list):
                        ttemp = evaluateAST(t, lineno).value.value
                        innerList = lib.modified_list()
                        for tt in ttemp:
                            innerList.append(tt.value)
                        n = ASTNode()
                        n.type = "terminal"
                        n.value = innerList
                        listValues.append(n)

                elif t.type == "id":
                    n = ASTNode()
                    n.type = "terminal"
                    n.value = evaluateAST(t, lineno).value
                    listValues.append(n)

        nlistValues = lib.modified_list(listValues)
        node = ASTNode()
        node.type = "list"

        node.value = nlistValues
        helper.ids[a.children[0]] = node

        return


    if(a.type == 'list'):
        logging.debug("List value: "+str(a.value))
        return evaluateAST(a.value, lineno)

    if(a.type == 'indexassignment'):
        logging.debug("--- index assignment ---")
        value = evaluateAST(helper.ids[evaluateAST(a.children[1], lineno).value], lineno)[evaluateAST(a.children[2], lineno).value]
        if isinstance(value,list):
            node = ASTNode()
            node.type = "list"
            nlistValues = lib.modified_list(value)
            node.value = nlistValues
            helper.ids[a.children[0]] = node
        else:
            helper.ids[a.children[0]] = value
        return

    if(a.type == 'rindexassignment'):
        logging.debug("--- rindex assignment ---")

        listValues = evaluateAST(helper.ids[a.children[0]], lineno)
        if evaluateAST(a.children[1], lineno).value == len(listValues):
            listValues.append(evaluateAST(a.children[2], lineno).value)
        else:
            listValues[evaluateAST(a.children[1], lineno).value] = evaluateAST(a.children[2], lineno).value
        
        nlistValues = lib.modified_list(listValues)
        node = ASTNode()
        node.type = "list"
        node.value = nlistValues
        helper.ids[a.children[0]] = node

        return


    if(a.type == "addedge"):
           logging.debug("------argEdge-----")
           curr =  helper.ids[a.children[0]].get_data()
           if a.children[1].value in curr.keys():
               curr[a.children[1].value][a.children[3].value]={"__connector__":a.children[2]}
           else:
               curr[a.children[1].value] = {a.children[3].value : {"__connector__":a.children[2]}}
           helper.ids[a.children[0]].edgelist=curr
           return

    if(a.type == "callchain"):
        logging.debug('-----eval: callchain----')
        if a.chain_next == None:
            ret = evaluateAST(a.children[0], lineno)
        else:
            ret = evaluateAST(a.children[0], lineno, True)
            node = ASTNode()
            node.type = "member_funccall"
            helper.ids["__chaining_buffer__"] = ret.value
            node.children.append("__chaining_buffer__")                #object
            node.children.append(a.chain_next.children[0])      #member function
            
            if a.chain_next.children[1] != None:
                node.children.append(a.chain_next.children[1])
            try:
                return evaluateAST(node, lineno)
            except Exception, e:
                raise                        
        return ret

    if(a.type == "funccall"):
        logging.debug('-----eval: call----')

        node=ASTNode()
        node.type="terminal"
        args = []
        # built in
        func = ASTNode()
        func.type = "funccall"
        try:
            try:
                logging.debug("****inbuilt****")
                func.children.append(helper.func_map[a.children[0]])
                if(len(a.children)> 1):
                    logging.debug("****func_arg****")
                    func.children.append(a.children[1])
                else:
                    func.children.append(None)
                if a.children[0] == "output":
                    func.children.append(chained)

            except KeyError:
                # User-defined
                logging.debug("****userdefined****")
                func.children.append(function[a.children[0]].children[0])    #statements
                func.children.append(function[a.children[0]].children[1])    #arguments
                func.children.append(function[a.children[0]].children[2])    #returnargs
                if len(a.children) >1:
                    logging.debug("****func_arg****")
                    func.children.append(a.children[1])  #actual arguments passed to function
                else:
                    func.children.append(None)  #No arguments passed
        except KeyError, e:
            logging.error("Function not found.")
            logging.error("Offending function: "+a.children[0])
            helper.gexit()

        if isinstance(func.children[0],ASTNode):
            #Packing
            # helper.scope_in() #Commented because it should now be handled by scoping in and out by compoundstatement evaluation
            #End packing
            
            numArgs = len(func.children[1].children)
            
            if func.children[1].children[0] == None:
                numArgs = 0
            
            for i in range(0,numArgs):
                helper.ids[func.children[1].children[i]]= evaluateAST(func.children[3], lineno).value[i]
                logging.info('Assigned '+str(func.children[1].children[i])+' to '+str(helper.ids[func.children[1].children[i]])+' inside funccall')
            logging.debug("MODIFIED scope: Before call:",helper.ids)
            evaluateAST(func.children[0], lineno)
            
            node.value = []
            if len(func.children[2].children)!=0:
                if func.children[2].children[0] != None:       
                    if len(func.children[2].children) ==1:
                        node.value = evaluateAST(func.children[2].children[0], lineno).value
                    else:
                        for ret in func.children[2].children:
                            node.value.append(evaluateAST(ret, lineno))
                #Unpacking
            # helper.scope_out() #Refer above at scope_in() call
            #End unpacking
            logging.debug("MODIFIED scope: After call:",helper.ids)
        else:
            if func.children[1] != None:
                x = evaluateAST(func.children[1], lineno).value
                node.value=func.children[0](*x)
            else:
                if func.children[0] == helper.goutput and func.children[2] == True:
                    node.value=func.children[0](None, True)
                else:    
                    node.value=func.children[0]()                

            try:
                if func.children[0].__bases__[0].__name__ in ["Node"]:
                    lib.nodeList[lib.globalLastNodeIDVal] = node.value
            except Exception, e:
                pass
        return node

        
    if (a.type == 'compoundstatement'):
        logging.debug('compound statement')
        if a.children[0] != None:
            # helper.scope_in()
            evaluateAST(a.children[0], lineno)
            # helper.scope_out()

    if (a.type == 'funccompoundstatement'):
        logging.debug('function compound statement')
        if a.children[0] != None:
            evaluateAST(a.children[0], lineno)

    if(a.type == "sequence"):
        return evaluateAST(a.children[0], lineno)

    if(a.type == "id"):
        node=ASTNode()
        node.type="terminal"
        try:
            if a.children[0] in helper.ids:
                node.value = helper.ids[a.children[0]]
            else:
                node.value=helper.ids[a.children[0]]
        except KeyError, e:
            logging.critical("Unknown variable: '"+str(a.children[0])+"'")
            sys.exit(-1)
        return node

    if(a.type == "node-dec"):
        logging.debug('-----eval: node-dec----')
        new_node_class = type(a.children[0].value, (lib.Node,), dict(((el,None) for i,el in enumerate(a.children[1].value)), __init__=lib.node_init, print_data=lambda self:lib.Node.print_data(self), get_data= lambda self: lib.Node().get_data(self), mapping=dict((i,el) for i,el in enumerate(a.children[1].value))))

        helper.func_map[a.children[0].value] = new_node_class
        return

    if(a.type == "graph-dec"):
        logging.debug('-----eval: graph-dec----')

        new_graph = lib.Graph(evaluateAST(a.children[3], lineno), evaluateAST(a.children[1], lineno), evaluateAST(a.children[2], lineno))
        lib.graphList[lib.globalLastGraphIDVal] = new_graph

        for source, destinations in new_graph.get_data().iteritems():
            source = int(source)
            if source not in lib.nodeList.keys():
                logging.error("Source Node #"+str(source)+" not found.")
                sys.exit(0)
            for destination, properties in destinations.iteritems():
                destination = int(destination)
                if destination not in lib.nodeList.keys():
                    logging.error("Destination Node #"+str(destination)+"not found.")
                    sys.exit(0)

        helper.ids[a.children[0].value] = new_graph

        # new_graph.print_data()
        return

    if(a.type == "function-dec"):
        function[a.children[0]]=a.children[1]

    #while loop
    if(a.type == 'while'):
        logging.debug("evaluateAST of while")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0], lineno))
        logging.debug("*********************")
        while (evaluateAST(a.children[0], lineno).value):
            evaluateAST(a.children[1], lineno)

    if(a.type == "if"):
        logging.debug("evaluateAST of if")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0], lineno))
        logging.debug("*********************")
        if(evaluateAST(a.children[0], lineno).value):
            evaluateAST(a.children[1], lineno)
        elif(len(a.children)>2):
            evaluateAST(a.children[2], lineno)

    if(a.type == 'for'):
        logging.debug("evaluateAST of for")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0], lineno))
        logging.debug("*********************")

        evaluateAST(a.children[0], lineno); # Initialization

        while (evaluateAST(a.children[1], lineno).value != 0): # Check condition
            evaluateAST(a.children[3], lineno) # Evaluate statement
            evaluateAST(a.children[2], lineno) # Update loop statement
            
    if(a.type == 'foreach'):
        logging.debug("evaluateAST of foreach")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0], lineno))
        logging.debug("*********************")
        iterVar = 0
        
        # helper.scope_in()
        # logging.debug("scope in")
        if(a.children[1].type == 'id'):
            iteratingList = evaluateAST(helper.ids[a.children[1]], lineno)
        else:
            iteratingList = evaluateAST(a.children[1], lineno)
            if(isinstance(iteratingList, ASTNode)):
                iteratingList = iteratingList.value

        while iterVar < len(iteratingList):
            helper.ids[a.children[0]] = iteratingList[iterVar] #Update iterVariable
            logging.debug('Evaluating foreach statement')
            evaluateAST(a.children[2], lineno) #evaluate child compoundstatement
            iterVar += 1 #increment index of iterVar

        # while iterVar < len(evaluateAST(helper.ids[a.children[1]])):
        #     logging.debug(helper.ids[a.children[1]])
        #     helper.ids[a.children[0]] = evaluateAST(helper.ids[a.children[1]])[iterVar] #Update iterVariable
        #     logging.debug('Evaluating foreach statement')
        #     evaluateAST(a.children[2]) #evaluate child compoundstatement
        #     iterVar += 1 #increment index of iterVar
        
        logging.debug("scope out")
        # helper.scope_out()