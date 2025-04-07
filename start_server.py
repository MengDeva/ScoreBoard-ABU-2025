import subprocess

port = 2930

def start_server():
    command = ["python3", "-m", "http.server", f"{port}"]
    process = subprocess.Popen(command)
    print(f"Server started on port {port}")


if __name__ == "__main__":
    start_server()
    print("Press Ctrl+C to stop the server.")