import subprocess
import sys
import time
import psutil
import os
from typing import Optional

def is_postgres_running() -> bool:
    for proc in psutil.process_iter(['name']):
        if 'postgres' in proc.info['name'].lower():
            return True
    return False

def start_postgres():
    if sys.platform == 'darwin':  # macOS
        subprocess.run(['brew', 'services', 'start', 'postgresql'])
    elif sys.platform == 'linux':
        subprocess.run(['sudo', 'service', 'postgresql', 'start'])
    elif sys.platform == 'win32':
        print("On Windows, please ensure PostgreSQL service is running manually")

    print("Waiting for PostgreSQL to start...")
    time.sleep(5)

def find_process_by_port(port: int) -> Optional[psutil.Process]:
    for proc in psutil.process_iter():
        try:
            for conn in proc.connections('inet'):
                if conn.laddr.port == port:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def kill_process_on_port(port: int):
    process = find_process_by_port(port)
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
            pass

def install_dependencies():
    print("Installing backend dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

    print("\nInstalling frontend dependencies...")
    # First, remove node_modules to ensure clean install
    if os.path.exists('frontend/node_modules'):
        if sys.platform == 'win32':
            subprocess.run(['rmdir', '/S', '/Q', 'frontend\\node_modules'], shell=True)
        else:
            subprocess.run(['rm', '-rf', 'frontend/node_modules'])

    # Install dependencies with forced resolution
    subprocess.run(['npm', 'install', '--legacy-peer-deps'], cwd='frontend')

def initialize_database():
    print("Initializing database...")
    subprocess.run([sys.executable, 'createdb.py'])

def main():
    try:
        # Install dependencies
        print("Checking and installing dependencies...")
        install_dependencies()

        # Check and start PostgreSQL if needed
        if not is_postgres_running():
            print("Starting PostgreSQL...")
            start_postgres()

        # Initialize database if needed
        initialize_database()

        # Kill any processes using our ports
        print("Checking ports...")
        kill_process_on_port(8000)  # Backend port
        kill_process_on_port(3000)  # Frontend port

        # Start backend
        print("\nStarting backend server...")
        backend_env = os.environ.copy()
        backend_process = subprocess.Popen(
            ['uvicorn', 'backend.app.main:app', '--reload', '--port', '8000'],
            env=backend_env
        )

        # Wait a bit for backend to start
        time.sleep(2)

        # Start frontend
        print("\nStarting frontend server...")
        frontend_env = os.environ.copy()
        frontend_process = subprocess.Popen(
            ['npm', 'start', '--legacy-peer-deps'],
            cwd='frontend',
            env=frontend_env
        )

        print("\nApplication is running!")
        print("Frontend: http://localhost:3000")
        print("Backend API: http://localhost:8000")
        print("Press Ctrl+C to stop all servers")

        # Keep the script running
        backend_process.wait()
        frontend_process.wait()

    except KeyboardInterrupt:
        print("\nShutting down servers...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
            print("Servers stopped successfully!")
        except:
            print("Some processes may need to be stopped manually")
        print("Goodbye!")

if __name__ == '__main__':
    main()
