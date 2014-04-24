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
    
    
    
    