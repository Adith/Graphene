#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from itertools import cycle
import os.path
from collections import OrderedDict

import sys
import pexpect
import time
import json

TEST_LOG = "test.log"
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
                "expect" : "hi",
                "name" : "Print",
                "severity" : CRITICAL
            },
    "set_var_print": { 
                "commands" : ["a=5;","print(a);"],
                "expect" : "5",
                "name" : "Variable Assignment & Print",
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

if sys.argv[1] == "i":
    isolated = True
elif sys.argv[1] == "t":
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
        else:
            c.sendline(command)
        print('.',end="")
        c.expect(PROMPT)
    
    if ''.join(c.before.split("\r\n")[1:-1]) != test["expect"]:
        ''' Test Failed '''
        print(" => Failed.")
        test["received"] = c.before
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

print("\nStatistics:")
print("Ran:", ran)
print("Failed:", failed)

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
        print("\tSeverity:",tests[v]["severity"])

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
