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

function addScore15(increment) {
    const score15 = document.getElementById("score15");
    score15.innerText = parseInt(score15.innerText) + increment;
    count = parseInt(score15.innerText);
    data = { command: "score", side: "b15", value:count };
    sendDataToServer(data);
}

function addScore10(increment) {
    const score10 = document.getElementById("score10");
    score10.innerText = parseInt(score10.innerText) + increment;
    count = parseInt(score10.innerText);
    data = { command: "score", side: "b10", value:count };
    sendDataToServer(data);
}

function addScore5(increment) {
    var score5 = document.getElementById("score5");
    score5.innerText = parseInt(score5.innerText) + increment;
    count = parseInt(score5.innerText);
    data = { command: "score", side: "b5", value:count };
    sendDataToServer(data);
}