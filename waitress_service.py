import os
import socket
import sys
import threading
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
from django.core.wsgi import get_wsgi_application
from waitress import serve

# --- Configuration ---
# Use a service-specific directory for better isolation
SERVICE_DIR = r"D:\Projects\Python_Projects\ProjectManagementApp"
# VENV_PATH = r"D:\Projects\Python_Projects\Environments\django_env"
VENV_PATH=r"D:\Projects\Python_Projects\Environments\django_env\Scripts\activate_this.py"
with open(VENV_PATH) as f:
    exec(f.read(), {'__file__': VENV_PATH})

LOG_FILE = os.path.join(SERVICE_DIR, "django_service.log")

# --- Logging Setup ---
try:
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO, # Changed to INFO for typical use, DEBUG can be too verbose
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode="a"
    )
except Exception as e:
    # Fallback to event log if file logging fails
    servicemanager.LogErrorMsg(f"Logging setup failed: {str(e)}. Falling back to Event Log.")
    
# --- Virtualenv Path Fix ---
# Add both site-packages and the virtualenv's scripts directory
venv_site_packages = os.path.join(VENV_PATH, 'Lib', 'site-packages')
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)
    
# --- Django WSGI Application Setup ---
def setup_wsgi():
    """Initializes the Django WSGI application and handles potential errors."""
    global application
    try:
        servicemanager.LogInfoMsg("Setting up Django WSGI application...")
        logging.info("Setting up Django WSGI application...")
        
        # Ensure the current working directory is the project directory
        os.chdir(SERVICE_DIR)
        
        
        # Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_management_app.settings')
        
        application = get_wsgi_application()
        logging.info("WSGI application initialized successfully.")
        servicemanager.LogInfoMsg("WSGI application initialized successfully.")
    except Exception as e:
        logging.exception("Failed to initialize Django WSGI application.")
        servicemanager.LogErrorMsg(f"Failed to initialize Django WSGI application: {str(e)}")
        # Raise the exception to prevent the service from starting improperly
        raise

# A global variable to hold the Waitress server instance
waitress_server = None

class DjangoService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ProjectManagementService"
    _svc_display_name_ = "Project Management Web Service"
    _svc_description_ = "Runs the Project Management Django application using Waitress."
    _exe_name_ = r"D:\Projects\Python_Projects\Environments\django_env\Scripts\pythonservice.exe"

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(120)
        self.is_running = False
        
        
    def SvcStop(self):
        logging.info("Service stop requested. Sending stop pending status.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        # Stop the Waitress server gracefully
        global waitress_server
        if waitress_server:
            logging.info("Shutting down Waitress server...")
            waitress_server.close()
            
        win32event.SetEvent(self.hWaitStop)
        logging.info("Waitress server shut down. Stop event set.")

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Service SvcDoRun method started.")
        logging.info("SvcDoRun method started. Reporting service as running.")
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.is_running = True
        
        # Setup WSGI inside SvcDoRun to ensure it runs in the service context
        try:
            setup_wsgi()
        except Exception:
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
            return

        thread = threading.Thread(target=self.run_server)
        thread.daemon = True
        thread.start()
        
        # Wait for the stop event
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        
        logging.info("Service SvcDoRun method finished.")

    def run_server(self):
        """Worker function to start the Waitress server."""
        global waitress_server
        try:
            logging.info("Starting Waitress server on 0.0.0.0:5000...")
            waitress_server = serve(application, host="0.0.0.0", port=5000, _quiet=True)
            
            # The 'serve' function blocks, so this part is only reached on shutdown
            logging.info("Waitress server has stopped.")
        except Exception as e:
            logging.exception("An error occurred while running Waitress.")
            servicemanager.LogErrorMsg(f"Waitress server error: {str(e)}")
            self.is_running = False
            # Set the stop event to signal the main thread to exit
            win32event.SetEvent(self.hWaitStop)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DjangoService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DjangoService)