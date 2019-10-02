import sys
import importlib 

sys.path.insert(0, './venv/lib/python3.6/site-packages')
ws =  importlib.import_module('config_drive_ws', 'config_drive_ws.py')

def application(environ, start_response):
    return ws.app.wsgi_app(environ, start_response)

#def application(environ, start_response):
#    start_response("200 OK", [("Content-Type", "text/plain")])
#    return (b"Hello, Unit!")  
