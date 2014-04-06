from threading import Thread
import SimpleHTTPServer
import SocketServer
import webbrowser
import pyperclip
import time
import select
port = 0

continue_server = True

def keep_running():
    global continue_server
    return continue_server == True

def run_while_true():
    global continue_server, port

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

def main():
    global continue_server, port
    thread = Thread(target = run_while_true, args = ())
    thread.start()
    
    while port==0:
        pass
    url = 'localhost:'+str(port)+'/template/d3.html'
    webbrowser.open_new(url)

    oldValue = pyperclip.paste()

    while pyperclip.paste() == oldValue:
        time.sleep(1)

    continue_server = False
    retValue = pyperclip.paste()
    pyperclip.copy(oldValue)
    thread.join()
    port = 0
    continue_server = True
    return retValue
