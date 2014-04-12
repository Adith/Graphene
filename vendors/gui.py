# -*- coding: UTF-8 -*-

#  ██████╗ ██╗   ██╗██╗
# ██╔════╝ ██║   ██║██║
# ██║  ███╗██║   ██║██║
# ██║   ██║██║   ██║██║
# ╚██████╔╝╚██████╔╝██║
#  ╚═════╝  ╚═════╝ ╚═╝
                     

from threading import Thread
import SimpleHTTPServer
import SocketServer
import webbrowser
import pyperclip
import time
import select
import os
import sys
port = 0

continue_server = True

def keep_running():
    global continue_server
    return continue_server == True

def run_while_true():
    global continue_server, port

    f = open(os.devnull, 'w')
    sys.stderr = f
    
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)
    httpd.allow_reuse_address = True
    port = httpd.socket.getsockname()[1]
    srvfd = httpd.fileno()
    while keep_running():
        ready = select.select([srvfd], [], [], 1) # Give one second
        if srvfd in ready[0]:
            httpd.handle_request()
    httpd.socket.close()

    sys.stderr = sys.__stderr__
    f.close()

def renderHelper(direction):
    thread = Thread(target = run_while_true, args = ())
    thread.start()
    
    while port==0:
        pass

    if(direction == 'output'):
        query = '?static'
    else:
        query = ''

    url = 'http://localhost:'+str(port)+'/template/d3.html'+query
    if os.name == 'posix':
        # Works best on Chrome.
        try:
            webbrowser.get("open -a /Applications/Google\ Chrome.app %s").open(url)
        except Exception, e:
            webbrowser.get().open(url)
    elif os.name == 'nt':
        # Has to be tested.
        webbrowser.get('windows-default').open(url)
    return thread

def input():
    global continue_server, port
    oldValue = pyperclip.paste()
    thread = renderHelper("input")

    while pyperclip.paste() == oldValue:
        time.sleep(0.5)

    continue_server = False
    retValue = pyperclip.paste()
    pyperclip.copy(oldValue)
    thread.join()
    port = 0
    continue_server = True
    return retValue

def output():
    global continue_server, port
    oldValue = pyperclip.paste()
    thread = renderHelper("output")

    # HACK-O-RAMA! Find a better way to figure out how to stop server after page load!
    time.sleep(3)

    continue_server = False
    
    thread.join()
    port = 0
    continue_server = True