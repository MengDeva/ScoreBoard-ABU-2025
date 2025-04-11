import asyncio
import websockets
import json
import threading
import socket
import time
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('10.255.255.255', 1))
IPAddr = s.getsockname()[0]
s.close()

controller_connections = 0
display_connected = False

timer_running = False
start_time = time.monotonic()

data = {
        "red_team_name": "",
        "blue_team_name": "",
        "red_team_score": 0,
        "blue_team_score": 0,
        "red_team_side":"",
        "blue_team_side":""
    }

def updateFile(data, file_path):
  with open(file_path, 'w') as f:
    f.write(data)

def update_connections():
    if display_connected:
        print("Display Connected: Yes")
        print(f"Controller Connections: {controller_connections}")
    else:
        print("Display Connected: No")
        print(f"Controller Connections: {controller_connections}")

async def handle_controller(websocket):
    global controller_connections, data
    controller_connections += 1
    update_connections()

    try:
        async for message in websocket:
            rev_data = json.loads(message)
            print(f"Controller received: {message}")
            if rev_data["command"] == "setTeams":
                data['red_team_name'] = rev_data["redTeamName"]
                data['blue_team_name'] = rev_data["blueTeamName"]
                data['red_team_side'] = rev_data["redTeamSide"]
                data['blue_team_side'] = rev_data["blueTeamSide"]

            elif rev_data["command"] == "score":
                data[rev_data['side']] = rev_data["value"]
                
            data_json = json.dumps(data)
            await broadcast_to_displays(data_json)


    finally:
        controller_connections -= 1
        update_connections()

async def handle_display(websocket):
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

async def start_controller():
    async with websockets.serve(handle_controller, IPAddr, 2932):
        print("Controller listening on port 2932")
        await asyncio.Future()

async def start_display():
    global display_ws
    async with websockets.serve(handle_display, IPAddr, 2931):
        print("Display server listening on port 2931")
        await asyncio.Future()

def reset():
    global data

    data = {
        "red_team_name": "",
        "blue_team_name": "",
        "r15": 0,
        "r10": 0,
        "r5": 0,
        "b15": 0,
        "b10": 0,
        "b5": 0
    }

    asyncio.run_coroutine_threadsafe(broadcast_to_displays(json.dumps(data)), server_loop)


def updateFileJson():
    global data
    with open("VData/data.json", 'w') as f:
        data = {
            'test':10
        }
        json.dump(data, f)

def timer():
    while True:
        if timer_running:
            elapsed_time = time.monotonic() - start_time
            pass
            updateFileJson()
            
            asyncio.run_coroutine_threadsafe(broadcast_to_displays(json.dumps(data)), server_loop)
            time.sleep(0.1)

def run_servers():
    global server_loop
    server_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(server_loop)

    try:
        server_loop.run_until_complete(asyncio.gather(start_controller(), start_display()))
    finally:
        server_loop.close()

server_thread = threading.Thread(target=run_servers)
timer_thread = threading.Thread(target=timer)

server_thread.start()
timer_thread.start()

server_thread.join()
timer_thread.join()
