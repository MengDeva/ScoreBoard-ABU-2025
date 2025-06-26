const ws = new WebSocket(`ws://${window.location.hostname}:2932`);

ws.onopen = () => {
  console.log("Connected to WebSocket server");
};

ws.onclose = () => {
  console.log("WebSocket connection closed");
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log("Received message:", message);
  if(message.command=="changeSide"){
    changeSide(message)
  }
}

function sendDataToServer(data) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(data));
    console.log("Data sent to WebSocket server:", data);
  } else {
    console.error("WebSocket is not connected. Unable to send data.");
  }
}

function setTeams() {
  const command = "setTeams";
  const redTeamName = document.getElementById("redTeamSelect").value;
  const blueTeamName = document.getElementById("blueTeamSelect").value;
  const redTeamSide = document.getElementById("redTeamSideSelect").value;
  const blueTeamSide = document.getElementById("blueTeamSideSelect").value;

  const data = { command, redTeamName, blueTeamName, redTeamSide, blueTeamSide };
  sendDataToServer(data);
}

function setSides() {
  command = "setSides";
  const redTeamSide = document.getElementById("redTeamSideSelect");
  const blueTeamSide = document.getElementById("blueTeamSideSelect");
  redTeamSide.value = redTeamSide.value === "DEFENSIVE" ? "OFFENSIVE" : "DEFENSIVE";
  blueTeamSide.value = blueTeamSide.value === "OFFENSIVE" ? "DEFENSIVE" : "OFFENSIVE";
  const data = { 
    command, 
    redTeamSide: redTeamSide.value,
    blueTeamSide: blueTeamSide.value 
  };
  
  sendDataToServer(data);
}

function singleButton(command){
  const data = { command };
  sendDataToServer(data);
}

function changeSide(data){
  document.getElementById("redTeamSideSelect").value = data.redTeamSide;
  document.getElementById("blueTeamSideSelect").value = data.blueTeamSide;
}