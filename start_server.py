import subprocess
import webbrowser
import socket
import atexit

port = 2930

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def start_server():
    command = ["python3", "-m", "http.server", f"{port}"]
    process = subprocess.Popen(command)
    print(f"Server started on port {port}")
    return process

def stop_server(process):
    if process:
        print("Stopping server...")
        process.terminate()
        process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    ip_address = get_ip_address()
    process = start_server()
    
    atexit.register(stop_server, process)

    try:
        url = f"http://{ip_address}:{port}"
        webbrowser.open(url)
        print("Press Ctrl+C to stop the server.")
        
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stop_server(process)