# Project Detail
This project is the scoring system for Robocon 2025 National Competition in Cambodia

Developed by:  
MengDeva(Front-end)  
aYukine(Back-end)  


# Content subject to change
# Starting the program
### 1. Make sure you have installed all neccessary module by running the following command:
> pip install requirement.txt

### 2. Start server
> python3 server.py

### 3. start http server
> python3 http_server.py

### 4. Open all neccessary page
> Display (Main score page)
> Red controller (Controller for red side score)
> Blue controller (Controller for blue score)
> Time controller (Controller for time and general setting)

### 5. Controller instruction

> Select team name and side then click ***set team*** to set team name and side  
> Select team side and click ***set side*** to change just team side  
> ***Preparing*** - 60 seconds countdown for preparing robot  
> ***Start*** - 5 seconds countdown and start the game  
> ***Possession Change*** - start 10 seconds countdown for possession change but shot clock and side will not change automatically   
> ***Reset*** - reset the shot clock back to 20 seconds  
> ***Reset All*** - reset all data to starting point  
> ***Pause/Resume*** - for pause/resume clock  

> Score can be incremented and decremented in the red and blue controller  
> After 2, 3, 7 score is added, 10 seconds possession change will trigger side will be switch automatically and shot clock will be reset    

> If shot clock reach zero, 10 seconds possession change will trigger and side will be switch automatically and shot clock will be reset  

# Game procedure
### Set up
> 2 Team will compete with each other where one is in defensive and one is in offensive  
> As Prepare timer start, each team will have 60 seconds to set up and prepare their robot on the game field accordingly  
> After the prepare time is over, all team must leave the game field  

### Start Game
> After game field is cleared to start, the 5 seconds starting counting will commence  
> After the 5 seconds is over, the game begins and the robot may start competing  

### Each round
> There are 3 scoring type:
> - ***2 Point Zone*** : 2 Score
> - ***3 Point Zone*** : 3 Score
> - ***Dunk Shot*** : 7 Score
> When a robot successfully perform any kind of scoring, score will be given, shot clock will be reset and possession change will start immediately with 10 seconds countdown   
> If scoring is not achieved within 20 seconds of shot clock, it'll be reset, possession change will start immediately with 10 seconds countdown

> Players must immediately set up their robot and leave the field within 10 seconds
> After 10 seconds, new round begin and robot may start performing again


### Violation, Foul and extra score
