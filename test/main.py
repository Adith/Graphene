#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from itertools import cycle
import os.path
from collections import OrderedDict
import logging

import logging
import sys
import pexpect
import time
import json

TEST_LOG = "test/test.log"
MINOR = "MINOR"
CRITICAL = "CRITICAL"
PANIC = "PANIC"
PASS = 1
FAIL = 0
log = None

tests = OrderedDict()
tests = {
    "print": {
                "commands" : ["print('hi');"],
                "expect" : "hi\n",
                "name" : "Print",
                "severity" : CRITICAL
            },
    "set_var_print": { 
                "commands" : ["a=5;","print(a);"],
                "expect" : "5\n",
                "name" : "Variable Assignment & Print",
                "severity" : CRITICAL
            },
    "add_numbers": { 
                "commands" : ["a=5;","b=5;","c=a+b;","print(c);"],
                "expect" : "10\n",
                "name" : "Addition of Numbers & Print",
                "severity" : CRITICAL
            },
    "print_list_element": { 
                "commands" : ["a=[1,2,3];","print(a[1]);"],
                "expect" : "2\n",
                "name" : "Printing a List Element",
                "severity" : CRITICAL
            },
    "if_statement": { 
                "commands" : ["if(1<2){print(\"inside if\");};"],
                "expect" : "inside if\n",
                "name" : "Checking IF Statement",
                "severity" : CRITICAL
            },
    "else_statement": { 
                "commands" : ["if (2<1) {print(\"inside if\");} else {print(\"inside else\");};"],
                "expect" : "inside else\n",
                "name" : "Checking ELSE Statement",
                "severity" : CRITICAL
            },
    "while_loop": { 
                "commands" : ["a=5;","while(a<10){print(a);a=a+1;};"],
                "expect" : "5\n6\n7\n8\n9\n",
                "name" : "Checking WHILE Loop",
                "severity" : CRITICAL
            },
    "for_loop": { 
                "commands" : ["for(i=0;i<5;i=i+1;){print(i);};"],
                "expect" : "0\n1\n2\n3\n4\n",
                "name" : "Checking WHILE Loop",
                "severity" : CRITICAL
            },
    "foreach_loop": { 
                "commands" : ["Student has name,age;","a = Student('aa',1);","b = Student('b',1);","c = Student('c',1);","Graph g has d{ 0->1,1->2};","foreach(x in g.getNodes()){print(x);};"],
                "expect" : "Node has\n\tname : aa\n\tage : 1\nNode has\n\tname : b\n\tage : 1\nNode has\n\tname : c\n\tage : 1\n",
                "name" : "Checking FOREACH Loop by Looping through Nodes of a Graph and Printing",
                "severity" : CRITICAL
            },
    "function_1": { 
                "commands" : ["def() => func{print(\"hi\");} => ();","func();"],
                "expect" : "hi\n",
                "name" : "Checking Basic Function with No Arguments, No Return",
                "severity" : CRITICAL
            },
    "function_2": { 
                "commands" : ["def(a) => func{print(a);} => ();","func(\"hi\");"],
                "expect" : "hi\n",
                "name" : "Checking Basic Function with 1 Argument, No Return",
                "severity" : CRITICAL
            },
    "function_3": { 
                "commands" : ["def(a) => func{print(a);} => ();","func(1+2);"],
                "expect" : "3\n",
                "name" : "Checking Basic Function with 1 Argument, Expression as return",
                "severity" : CRITICAL
            },
    "function_4": { 
                "commands" : ["def(a,b) => func{c=a+b;} => (c,10);","x=10;","b=func(x,20);","print(b);"],
                "expect" : "30\n10\n",
                "name" : "Checking Basic Function with Multiple Argument, Multiple return",
                "severity" : CRITICAL
            },
    "function_5": { 
                "commands" : ["def(a,b) => func{c=a+b;} => (c+10);","x=10;","b=func(x,20);","print(b);"],
                "expect" : "40\n",
                "name" : "Checking Basic Function with Multiple Argument, Expression as return",
                "severity" : CRITICAL
            },
    "list_1": { 
                "commands" : ["a = [1,2,3,\"columbia\"];","print(a[3]);"],
                "expect" : "columbia\n",
                "name" : "Print List Element by Index",
                "severity" : CRITICAL
            },
    "list_2": { 
                "commands" : ["a = [1,2,3,\"columbia\"];","b = a[2];","print(b);"],
                "expect" : "3\n",
                "name" : "Assign List Element by Index & Print",
                "severity" : CRITICAL
            },
    "list_3": { 
                "commands" : ["a = [\"columbia\",\"newyork\"];","a[1] = \"university\";","print(a);"],
                "expect" : "columbia\nuniversity\n",
                "name" : "Modify List element & Print",
                "severity" : CRITICAL
            },
    "arithmetic": { 
                "commands" : ["a = [1,2,3];","b = [10,11,12];","c = a[0]+b[1]+10/2;","print(c);"],
                "expect" : "17\n",
                "name" : "Test Arithmetic Operations & Print",
                "severity" : CRITICAL
            },
    "logical": { 
                "commands" : ["a = True;","b=10;","c=5;","if (a && b<c || b>0) {print (\"Logical works\");};"],
                "expect" : "Logical works\n",
                "name" : "Test Logical Operations in If Statement",
                "severity" : CRITICAL
            },
    "error_1": { 
                "commands" : ["a = 1+c;"],
                "expect" : "Error at line 1: Identifier 'c' not found\n\n",
                "name" : "Test Error Handling - Unknown Identifier",
                "severity" : CRITICAL
            },
    "error_2": { 
                "commands" : ["a = 1+\"columbia\";"],
                "expect" : "Error at line 1: Unsupported operand types for '+'\n\n",
                "name" : "Test Error Handling - Unsupported Operand Types",
                "severity" : CRITICAL
            },
    "error_3": { 
                "commands" : ["myfunc();"],
                "expect" : "Error at line 1: Function 'myfunc' not found\n\n",
                "name" : "Test Error Handling - Function Not Found",
                "severity" : CRITICAL
            },
    "error_4": { 
                "commands" : ["def (a,b) => myfunc{} => ();","myfunc();"],
                "expect" : "Error at line 2: Mis-match in number of function arguments\n\n",
                "name" : "Test Error Handling - Function Argument Mismatch",
                "severity" : CRITICAL
            },
    "warning_1": { 
                "commands" : ["def (a) => myfunc{print(a);} => ();","myfunc(1,2);"],
                "expect" : "Warning - Mis-match in number of function arguments on line 2\n1\n",
                "name" : "Test Warning - Function Argument Mismatch",
                "severity" : CRITICAL
            },
    "node_1": { 
                "commands" : ["Student has name,age;","a = Student ('a',1);","print(a);"],
                "expect" : "Node has\n\tname : a\n\tage : 1\n",
                "name" : "Node Type Declaration, Node Assignment & Print",
                "severity" : CRITICAL
            },
    "lambda_1": { 
                "commands" : ["x = lambda(a):{d=a+1;}=>(d);"," y=x(3);","print(y);"],
                "expect" : "4\n",
                "name" : "Lambda Sanity",
                "severity" : CRITICAL
            },
    "lambda_2": { 
                "commands" : ["x = lambda(a):{d=a+1;}=>(d);","def (l,p)=>apply{z=l(p);}=>(z);","y=apply(x,7);","print(y);"],
                "expect" : "8\n",
                "name" : "Lambda as Parameter to Function",
                "severity" : CRITICAL
            },
}

failed_tests = []

PROMPT = "graphene>"
print("\n\n")
print(" ███████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗███████╗    ████████╗███████╗███████╗████████╗    ███████╗██╗   ██╗██╗████████╗███████╗");
print(" ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║██╔════╝████╗  ██║██╔════╝    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝    ██╔════╝██║   ██║██║╚══██╔══╝██╔════╝");
print(" ██║  ███╗██████╔╝███████║██████╔╝███████║█████╗  ██╔██╗ ██║█████╗         ██║   █████╗  ███████╗   ██║       ███████╗██║   ██║██║   ██║   █████╗  ");
print(" ██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║██╔══╝  ██║╚██╗██║██╔══╝         ██║   ██╔══╝  ╚════██║   ██║       ╚════██║██║   ██║██║   ██║   ██╔══╝  ");
print(" ╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║███████╗██║ ╚████║███████╗       ██║   ███████╗███████║   ██║       ███████║╚██████╔╝██║   ██║   ███████╗");
print("  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝       ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝\n\n");

c = pexpect.spawn('/usr/bin/python graphene.py')
c.expect(PROMPT)
ran = 0
failed = 0
isolated = False
test_name = -1

if len(sys.argv) >1:
    if sys.argv[1] == "-i":
        isolated = True
    elif sys.argv[1] == "-t":
        test_name = sys.argv[2]

for name, test in tests.iteritems():
    if test_name != -1:
        if name != test_name:
            continue
    print("Running Test '",name,"'",sep="", end="")
    for command in test["commands"]:
        if isinstance(command,list):
            for commandlet in command:
                c.sendline(commandlet)
                try:
                    c.expect(PROMPT)
                except Exception, e:
                    break
        else:
            c.sendline(command)
            try:
                c.expect(PROMPT)
            except Exception, e:
                break
            
            # logging.error("command:"+c.before)
        print('.',end="")

    # logging.error('Status:'+c.before)
    # logging.error('Parsed Status:'+'\n'.join(c.before.split("\r\n")[1:]))
    # logging.error('Expected:'+test["expect"])
    
    if '\n'.join(c.before.split("\r\n")[1:]) != test["expect"]:
        ''' Test Failed '''
        print(" => Failed.")
        test["received"] = '\n'.join(c.before.split("\r\n")[1:-1])
        test["result"] = FAIL
        failed = failed + 1
        failed_tests.append(name)
    else:
        print(" => Passed.")
        test["result"] = PASS
    ran = ran + 1
    if isolated:
        c.kill(1)
        c = pexpect.spawn('/usr/bin/python graphene.py')
        c.expect(PROMPT)

if os.path.isfile(TEST_LOG):
    with open(TEST_LOG, "r") as f:
        log = f.read()

c.kill(1)

if failed >0:
    print("Test",sep="", end="")
    if failed >1:
        print("s",sep="", end="")
    print(" ",sep="",end="")
    for i,v in enumerate(failed_tests):
        print("'",v,"'",sep="",end="")
        if i!=failed-1:
            print(",",end="")
    print(" failed.")

    for i,v in enumerate(failed_tests):
        print("Test '",v,"':",sep="")
        print("\tExpected:",tests[v]["expect"])
        print("\tReceived:",tests[v]["received"])
        print("\tSeverity:",tests[v]["severity"],"\n")

current_result = json.dumps({
    "time" : time.asctime(time.localtime(time.time())),
    "ran" : ran,
    "failed" : failed,
    "failed_tests" : failed_tests
    })

history = ""
try:
    with open(TEST_LOG, "r") as f:
        history = f.read()
except Exception, e:
    with open(TEST_LOG,"w") as f:
        pass

print("\nLast",len(history.split("\n")[:-1]),"runs:")
for run in history.split("\n")[:-1]:
    run = json.loads(run)
    print("Run at",run["time"])
    print("Ran:",run["ran"])
    print("Failed:",run["failed"])
    print("Failed Tests:",run["failed_tests"],"\n")

if len(history.split("\n"))>5:
    history = '\n'.join(history.split("\n")[1:-1]) + "\n"

with open(TEST_LOG, "w") as f:
        f.write(history+current_result+"\n")

print("\nStatistics:")
print("Ran:", ran)
print("Failed:", failed)

if failed == 0:
    print("\n\n")
    print(" ███████╗██╗   ██╗ ██████╗ ██████╗███████╗███████╗███████╗ ");
    print(" ██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝ ");
    print(" ███████╗██║   ██║██║     ██║     █████╗  ███████╗███████╗ ");
    print(" ╚════██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║ ");
    print(" ███████║╚██████╔╝╚██████╗╚██████╗███████╗███████║███████║ ");
    print(" ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝ \n\n");
                                                         
