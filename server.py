import asyncio
import websockets
import json
import threading
import socket
import time
import os
import math

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

log = ""
game_round = 1 

data = {
        "red_team_name": "",
        "blue_team_name": "",
        "red_team_side":"",
        "blue_team_side":"",
        "game_clock": game_time,
        "shot_clock": shot_clock_time,
        "overlay_timer": 0,
        "overlay_message": "",
        "r1": 0,
        "r2": 0,
        "r3": 0,
        "r7": 0,
        "b1": 0,
        "b2": 0,
        "b3": 0,
        "b7": 0
    }

def update_connections():
    if display_connected:
        print("Display Connected: Yes")
        print(f"Controller Connections: {len(controller_connections)}")
    else:
        print("Display Connected: No")
        print(f"Controller Connections: {len(controller_connections)}")

async def handle_controller(websocket):
    global controller_connections, data, start_time, timer_running, log, game_round
    controller_connections.append(websocket)
    update_connections()

    try:
        async for message in websocket:
            clock = data["game_clock"]
            rev_data = json.loads(message)
            print(f"Controller received: {message}")
            if rev_data["command"] == "setTeams":
                data['red_team_name'] = rev_data["redTeamName"]
                data['blue_team_name'] = rev_data["blueTeamName"]
                data['red_team_side'] = rev_data["redTeamSide"]
                data['blue_team_side'] = rev_data["blueTeamSide"]

            elif rev_data["command"] == "setSides":
                data['red_team_side'] = rev_data["redTeamSide"]
                data['blue_team_side'] = rev_data["blueTeamSide"]
                log += f"Game Time:{math.ceil(clock)} - Round {game_round} - Sides Changed\n"

            elif rev_data["command"] == "score":
                data[rev_data['side']] = rev_data["value"]
                side= rev_data['side']
                if side == "r1":
                    log += f"Game Time:{math.ceil(clock)} - Round {game_round} - {rev_data['value']} Score added to {data['red_team_name']}!\n"
                elif side == "b1":
                    log += f"Game Time:{math.ceil(clock)} - Round {game_round} - {rev_data['value']} Score added to {data['blue_team_name']}!\n"
                else:
                    data["overlay_timer"] = 10
                    data["shot_clock"] = 20
                    if side[0] == "r":
                        data["overlay_message"] = f"Posession Change\n{data['red_team_name']} scored {side[1]}!"
                        log += f"Game Time:{math.ceil(clock)} - Round {game_round} - {data['red_team_name']} scored {side[1]}!\n"
                        game_round += 1
                        change_team_side()
                    else:
                        data["overlay_message"] = f"Posession Change\n{data['blue_team_name']} scored {side[1]}!"
                        log += f"Game Time:{math.ceil(clock)} - Round {game_round} - {data['blue_team_name']} scored {side[1]}!\n"
                        game_round += 1
                        change_team_side()

            elif rev_data["command"] == "p_change":
                timer_running = True
                data["overlay_timer"] = 10
                data["overlay_message"] = f"Posession Change"
                log += f"Game Time:{math.ceil(clock)} - Round {game_round} - Possesion Change!\n"

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

            elif rev_data["command"] == "start":
                data["overlay_timer"] = 5
                data["overlay_message"] = "Starting in .."
                start_time = time.monotonic()
                timer_running = True

            elif rev_data["command"] == "pause":
                if timer_running == False:
                    start_time = time.monotonic()
                    timer_running = True
                    if log != "":
                        log += f"Game Time:{math.ceil(clock)} - Round {game_round} - Game Resume\n"
                else:
                    timer_running = False
                    if log != "":
                        log += f"Game Time:{math.ceil(clock)} - Round {game_round} - Game Paused\n"
                
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
    global data, log

    data = {
        "red_team_name": "",
        "blue_team_name": "",
        "red_team_side":"",
        "blue_team_side":"",
        "game_clock": game_time,
        "shot_clock": shot_clock_time,
        "overlay_timer": 0,
        "overlay_message": "",
        "r1": 0,
        "r2": 0,
        "r3": 0,
        "r7": 0,
        "b1": 0,
        "b2": 0,
        "b3": 0,
        "b7": 0
    }
    log = ""
    asyncio.run_coroutine_threadsafe(broadcast_to_displays(json.dumps(data)), server_loop)


def change_team_side():
    global data
    if data["red_team_side"] == "OFFENSIVE":
        data["red_team_side"] = "DEFENSIVE"
        data["blue_team_side"] = "OFFENSIVE"
    else:
        data["red_team_side"] = "OFFENSIVE"
        data["blue_team_side"] = "DEFENSIVE"
    
    changeSideCommand = {
        "command": "changeSide",
        "redTeamSide": data["red_team_side"],
        "blueTeamSide": data["blue_team_side"]
        }
    
    asyncio.run_coroutine_threadsafe(broadcast_to_controllers(json.dumps(changeSideCommand)), server_loop)

def updateFileJson():
    global data
    file_path = "data/data.json"
    if not os.path.exists(file_path):
        os.makedirs("data")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def log_game():
    global log
    timestamp = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    file_path = f"data/log_{timestamp}.txt"

    with open(file_path, 'w') as f:
        f.write(log)
        log = ""
        print(f"Game log saved to {file_path}")

def timer():
    global timer_running, start_time, game_time, shot_clock_time, data, log, game_round
    while True:
        if timer_running:
            elapsed_time = time.monotonic() - start_time
            
            if data["overlay_timer"] > 0:
                data["overlay_timer"] -= elapsed_time
                if data["overlay_timer"] <= 0 and data["overlay_message"] == "Prepare Time":
                    timer_running = False
            
            else:
                if data["shot_clock"] <= 0:
                    data["overlay_timer"] = 10
                    data["shot_clock"] = 20
                    data["overlay_message"] = "Possesion Change\nShot Clock Over"
                    log += f"Game Time:{math.ceil(clock)} - Round {game_round} - Shot Clock Over\n"
                    game_round += 1
                    change_team_side()

                elif clock <= 0:
                    total_red = data["r1"] + 2*data["r2"] + 3*data["r3"] + 7*data["r7"]
                    total_blue = data["b1"] + 2*data["b2"] + 3*data["b3"] + 7*data["b7"]
                    if total_red > total_blue:
                        winner = data["red_team_name"]
                    elif total_blue > total_red:
                        winner = data["blue_team_name"]
                    else:
                        winner = "Draw"
                    data["overlay_timer"] = f"winner : {winner}"
                    data["overlay_message"] = "Game Finished"
                    log += f"Game Time:{math.ceil(clock)} - Round {game_round} - Game Finished\n"
                    log += f"Red Team: {data['red_team_name']} - Score: {total_red}\n"
                    log += f"Blue Team: {data['blue_team_name']} - Score: {total_blue}\n"
                    timer_running = False
                    log_game()

                else:
                    clock -= elapsed_time
                    data["shot_clock"] -= elapsed_time
            
            start_time = time.monotonic()
            updateFileJson()
            
            asyncio.run_coroutine_threadsafe(broadcast_to_displays(json.dumps(data)), server_loop)
            time.sleep(0.05)

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
