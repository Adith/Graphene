from threading import Thread
import SimpleHTTPServer
import webbrowser
import SocketServer
import vendors/pyperclip

PORT = 8000

continue_server = True

def keep_running():
    global continue_server
    return continue_server == True

def run_while_true():
    global continue_server
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    while keep_running():
        httpd.handle_request()



def main():
    global continue_server
    thread = Thread(target = run_while_true, args = ())
    thread.start()
    
    oldValue = pyperclip.paste()

    url = '/template/d3.html'

    webbrowser.open_new(url)
    
    while pyperclip.paste() == oldValue:
        sleep(1)

    continue_server = False
    retValue = pyperclip.paste()
    pyperclip.copy(oldValue)
    return retValue
