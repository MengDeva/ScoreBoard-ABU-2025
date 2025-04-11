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
  if(message.command=="reset"){
    resetScores();
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

function addScore7(increment) {
  const score7 = document.getElementById("score7");
  score7.innerText = parseInt(score7.innerText) + increment;
  count = parseInt(score7.innerText);
  data = { command: "score", side: "b7", value: count };
  updateTotalScore();
  sendDataToServer(data);
}

function addScore3(increment) {
  const score3 = document.getElementById("score3");
  score3.innerText = parseInt(score3.innerText) + increment;
  count = parseInt(score3.innerText);
  data = { command: "score", side: "b3", value: count };
  updateTotalScore();
  sendDataToServer(data);
}

function addScore2(increment) {
  var score2 = document.getElementById("score2");
  score2.innerText = parseInt(score2.innerText) + increment;
  count = parseInt(score2.innerText);
  data = { command: "score", side: "b2", value: count };
  updateTotalScore();
  sendDataToServer(data);
}

function addScore1(increment) {
  var score1 = document.getElementById("score1");
  score1.innerText = parseInt(score1.innerText) + increment;
  count = parseInt(score1.innerText);
  data = { command: "score", side: "b1", value: count };
  updateTotalScore();
  sendDataToServer(data);
}

function updateTotalScore(){
  const score1 = parseInt(document.getElementById("score1").innerText) || 0;
  const score2 = parseInt(document.getElementById("score2").innerText) || 0;
  const score3 = parseInt(document.getElementById("score3").innerText) || 0;
  const score7 = parseInt(document.getElementById("score7").innerText) || 0;
  
  const totalScore = score1 + score2 * 2 + score3 * 3 + score7 * 7;
  
  document.getElementById("totalScore").innerText = totalScore;
}

function resetScores() {
  const score1 = document.getElementById("score1");
  const score2 = document.getElementById("score2");
  const score3 = document.getElementById("score3");
  const score7 = document.getElementById("score7");
  
  score1.innerText = 0;
  score2.innerText = 0;
  score3.innerText = 0;
  score7.innerText = 0;
  
  updateTotalScore();
}