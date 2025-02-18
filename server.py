import asyncio
import websockets
import json
import tkinter as tk
from tkinter import ttk
import threading
import socket
import time
import pygame

pygame.init()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('10.255.255.255', 1))
IPAddr = s.getsockname()[0]
s.close()

ltime = 0
timer_running = False
state = "preparing"
startTime = time.monotonic()
PrepareTime = 60
readyTime = 5

score_data = {
    'team1': "",
    'team2': "",
    "time": "",
}

controller_connections = 0
display_connected = False

def update_connections():
    controller_label.config(text=f"Controller Connections: {controller_connections}")
    if display_connected:
        display_label.config(text="Display Connected: Yes")
    else:
        display_label.config(text="Display Connected: No")

async def handle_display(websocket, path):
    global display_connected, display_ws
    display_connected = True
    display_ws = websocket
    update_connections()

    try:
        async for message in websocket:
            print(f"Display received: {message}")
    finally:
        display_connected = False
        update_connections()

async def broadcast_to_displays(message):
    global display_connected
    if display_connected:
        try:
            await display_ws.send(message)
        except websockets.exceptions.ConnectionClosed:
            display_connected = False
            update_connections()

async def start_display():
    global display_ws
    async with websockets.serve(handle_display, "localhost", 8991):
        print("Display server listening on port 8991")
        await asyncio.Future()

def run_gui():
    global root, controller_label, display_label, stateLabel, ent1, ent2

    root = tk.Tk()
    root.title("WebSocket Server")

    ip = ttk.Label(root, text=f"site: {IPAddr}:8821", font=30)
    ip.pack()

    controller_label = ttk.Label(root, text="Controller Connections: 0", font=30)
    controller_label.pack()

    display_label = ttk.Label(root, text="Display Connected: No", font=30)
    display_label.pack()

    frame1 = ttk.Frame(root)

    ent1 = ttk.Entry(frame1)
    ent1.pack(side="left")

    ent2 = ttk.Entry(frame1)
    ent2.pack(side="right")

    frame1.pack()

    root.mainloop()


def run_servers():
    global server_loop
    server_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(server_loop)

    try:
        server_loop.run_until_complete(asyncio.gather(start_display()))
    finally:
        server_loop.close()

gui_thread = threading.Thread(target=run_gui)
server_thread = threading.Thread(target=run_servers)

gui_thread.start()
server_thread.start()


gui_thread.join()
server_thread.join()
