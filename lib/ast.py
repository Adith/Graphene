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