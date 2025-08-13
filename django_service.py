import sys
sys.path.append(r"D:\Projects\Python_Projects\ProjectManagementApp\project_management_app\django_service.py")
sys.path.append(r"D:\Projects\Python_Projects\ProjectManagementApp\project_management_app\project_management_app")


import os

# Activate venv before anything else
venv_path = r"D:\Projects\Python_Projects\Environments\django_env\Scripts\activate_this.py"
with open(venv_path) as f:
    exec(f.read(), dict(__file__=venv_path))

import servicemanager  # Now it should work
import win32serviceutil

import time
import signal
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess

class DjangoWaitressService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DjangoWaitressVenv"
    _svc_display_name_ = "Django App with Waitress (Venv)"
    _svc_description_ = "Runs a Django application using Waitress in a virtual environment"
    _exe_name_ = r"D:\Projects\Python_Projects\Environments\django_env\Scripts\pythonservice.exe"
    

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        servicemanager.LogInfoMsg("Stopping Django+Waitress...")
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Starting Django+Waitress in virtual environment...")
        self.main()

    def main(self):
        # Path to your virtual environment's Python
        venv_python = r"D:\Projects\Python_Projects\Environments\django_env\Scripts\python.exe"

        # Path to Django's manage.py
        manage_py = r"D:\Projects\Python_Projects\ProjectManagementApp\project_management_app\manage.py"

        # Command to run Waitress
        cmd = [
            venv_python,
            "-m", "waitress",
            "--host=0.0.0.0",
            "--port=8000",
            "myproject.wsgi:application"
        ]

        # Start Waitress
        self.process = subprocess.Popen(
            cmd,
            cwd=os.path.dirname(manage_py),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Keep service alive until stopped
        while True:
            rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)
            if rc == win32event.WAIT_OBJECT_0:
                break

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DjangoWaitressService)
