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
  sendDataToServer(data);
}

function addScore3(increment) {
  const score3 = document.getElementById("score3");
  score3.innerText = parseInt(score3.innerText) + increment;
  count = parseInt(score3.innerText);
  data = { command: "score", side: "b3", value: count };
  sendDataToServer(data);
}

function addScore2(increment) {
  var score2 = document.getElementById("score2");
  score2.innerText = parseInt(score2.innerText) + increment;
  count = parseInt(score2.innerText);
  data = { command: "score", side: "b2", value: count };
  sendDataToServer(data);
}

function addScore1(increment) {
  var score1 = document.getElementById("score1");
  score1.innerText = parseInt(score1.innerText) + increment;
  count = parseInt(score1.innerText);
  data = { command: "score", side: "b1", value: count };
  sendDataToServer(data);
}
