const ws = new WebSocket(`ws://${window.location.hostname}:2931`);
ws.onopen = () => {
    console.log("Connected to WebSocket server");
};

ws.onmessage = (event) => {
    console.log("Message from server:", event.data);
    const data = JSON.parse(event.data);
    updateDisplay(data);
};

ws.onclose = () => {
    console.log("WebSocket connection closed");
};

ws.onerror = (error) => {
    console.error("WebSocket error:", error);
};

function updateDisplay(data) {
    const redTeamName = document.getElementById("redTeamName");
    const blueTeamName = document.getElementById("blueTeamName");
    const redTeamSide = document.getElementById("redTeamSide");
    const blueTeamSide = document.getElementById("blueTeamSide");
    const redTeamScore = document.getElementById("redTeamScore");
    const blueTeamScore = document.getElementById("blueTeamScore");
    const red7 = document.getElementById("r7");
    const red3 = document.getElementById("r3");
    const red2 = document.getElementById("r2");
    const blue7 = document.getElementById("b7");
    const blue3 = document.getElementById("b3");
    const blue2 = document.getElementById("b2");

    redTeamName.textContent = data.red_team_name;
    blueTeamName.textContent = data.blue_team_name;
    redTeamSide.textContent = data.red_team_side;
    blueTeamSide.textContent = data.blue_team_side;

    const r7 = parseInt(data.r7) || 0;
    const r3 = parseInt(data.r3) || 0;
    const r2 = parseInt(data.r2) || 0;
    const r1 = parseInt(data.r1) || 0;
    const b7 = parseInt(data.b7) || 0;
    const b3 = parseInt(data.b3) || 0;
    const b2 = parseInt(data.b2) || 0;
    const b1 = parseInt(data.b1) || 0;

    red7.textContent = r7;
    red3.textContent = r3;
    red2.textContent = r2;
    blue7.textContent = b7;
    blue3.textContent = b3;
    blue2.textContent = b2;

    const redScore = r7 * 7 + r3 * 3 + r2 * 2 + r1 * 1;
    const blueScore = b7 * 7 + b3 * 3 + b2 * 2 + b1 * 1;

    redTeamScore.textContent = redScore;
    blueTeamScore.textContent = blueScore;
}