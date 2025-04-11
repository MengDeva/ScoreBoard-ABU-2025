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

controller_connections:list = []
display_connected = False

timer_running = False
start_time = time.monotonic()

game_time = 160
shot_clock_time = 20

data = {
        "red_team_name": "",
        "blue_team_name": "",
        "red_team_side":"",
        "blue_team_side":"",
        "game_clock": game_time,
        "shot_clock": shot_clock_time,
        "overlay_timer": 0,
        "overlay_message": ""
    }

def update_connections():
    if display_connected:
        print("Display Connected: Yes")
        print(f"Controller Connections: {len(controller_connections)}")
    else:
        print("Display Connected: No")
        print(f"Controller Connections: {len(controller_connections)}")

async def handle_controller(websocket):
    global controller_connections, data, start_time, timer_running
    controller_connections.append(websocket)
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

            elif rev_data["command"] == "start":
                if not timer_running:
                    timer_running = True
                    start_time = time.monotonic()
                elif timer_running:
                    timer_running = False

            elif rev_data["command"] == "resetAll":
                reset()
                timer_running = False
                await broadcast_to_controllers(json.dumps({"command": "reset"}))
            
            elif rev_data["command"] == "reset":
                data["shot_clock"] = shot_clock_time

            elif rev_data["command"] == "prepare":
                data["overlay_timer"] = 60
                data["overlay_message"] = "Prepare Time"
                start_time = time.monotonic()
                timer_running = True

            elif rev_data["command"] == "countdown":
                data["overlay_timer"] = 5
                data["overlay_message"] = "Starting in .."
                start_time = time.monotonic()
                timer_running = True

            elif rev_data["command"] == "pause":
                if timer_running == False:
                    start_time = time.monotonic()
                    timer_running = True
                else:
                    timer_running = False
                
            data_json = json.dumps(data)
            await broadcast_to_displays(data_json)
            updateFileJson()


    finally:
        controller_connections.remove(websocket)
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

async def broadcast_to_controllers(message):
    global controller_connections
    if controller_connections:
        try:
            print(f"Broadcasting to {len(controller_connections)} controllers")
            tasks = [asyncio.create_task(ws.send(message)) for ws in controller_connections]
            await asyncio.gather(*tasks)
        except websockets.exceptions.ConnectionClosed:
            controller_connections = [ws for ws in controller_connections if ws.open]
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
        "red_team_side":"",
        "blue_team_side":"",
        "game_clock": game_time,
        "shot_clock": shot_clock_time,
        "overlay_timer": 0,
        "overlay_message": ""
    }

    asyncio.run_coroutine_threadsafe(broadcast_to_displays(json.dumps(data)), server_loop)


def updateFileJson():
    global data
    with open("data/data.json", 'w') as f:
        f.write(json.dumps(data, indent=4))
        json.dump(data, f)

def timer():
    global timer_running, start_time, game_time, shot_clock_time, data
    while True:
        if timer_running:
            elapsed_time = time.monotonic() - start_time
            
            if data["overlay_timer"] > 0:
                data["overlay_timer"] -= elapsed_time
                if data["overlay_timer"] <= 0 and data["overlay_message"] == "Prepare Time":
                    timer_running = False
            
            else:
                if data["shot_clock"] <= 0:
                    timer_running = False
                else:
                    data["game_clock"] -= elapsed_time
                    data["shot_clock"] -= elapsed_time
            
            start_time = time.monotonic()
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
