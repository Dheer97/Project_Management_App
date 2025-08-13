import os
import sys
import time
import subprocess
import requests
import win32serviceutil
import win32service
import win32event
import servicemanager

# ==== CONFIGURATION ====
VENV_PYTHON = r"D:\Projects\Python_Projects\Environments\django_env\Scripts\python.exe"
PROJECT_DIR = r"D:\Projects\Python_Projects\ProjectManagementApp\project_management_app"
MANAGE_PY = os.path.join(PROJECT_DIR, "manage.py")
WSGI_APP = "project_management_app.wsgi:application"
HOST = "127.0.0.1"
PORT = "8000"
HEALTH_URL = f"http://{HOST}:{PORT}/"
CHECK_INTERVAL = 10  # seconds between health checks
# ========================

sys.path.append(PROJECT_DIR)


class DjangoWaitressService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DjangoWaitressVenv"
    _svc_display_name_ = "Django App with Waitress (Venv)"
    _svc_description_ = "Runs a Django application using Waitress in a virtual environment"
    _exe_name_ = os.path.join(os.path.dirname(VENV_PYTHON), "pythonservice.exe")

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        servicemanager.LogInfoMsg("Stopping Django+Waitress...")
        self.stop_waitress()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Starting Django+Waitress in virtual environment with health checks...")
        self.main()

    def start_waitress(self):
        """Start the Waitress process."""
        cmd = [
            VENV_PYTHON,
            "-m", "waitress",
            f"--host={HOST}",
            f"--port={PORT}",
            WSGI_APP
        ]
        self.process = subprocess.Popen(
            cmd,
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        servicemanager.LogInfoMsg("Waitress process started.")

    def stop_waitress(self):
        """Stop the Waitress process."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
        servicemanager.LogInfoMsg("Waitress process stopped.")

    def waitress_healthy(self):
        """Check if Waitress is responding."""
        try:
            r = requests.get(HEALTH_URL, timeout=2)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def main(self):
        self.start_waitress()

        while True:
            # Wait for stop signal or timeout
            rc = win32event.WaitForSingleObject(self.hWaitStop, CHECK_INTERVAL * 1000)
            if rc == win32event.WAIT_OBJECT_0:
                break

            # Check if process is still running
            if self.process.poll() is not None:
                servicemanager.LogErrorMsg("Waitress process died unexpectedly. Restarting...")
                self.start_waitress()
                continue

            # Check health via HTTP
            if not self.waitress_healthy():
                servicemanager.LogErrorMsg("Waitress is unresponsive. Restarting...")
                self.stop_waitress()
                self.start_waitress()

        # Stop process on service exit
        self.stop_waitress()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DjangoWaitressService)
