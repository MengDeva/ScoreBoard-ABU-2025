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
    const redTeamScore = document.getElementById("redTeamScore");
    const blueTeamScore = document.getElementById("blueTeamScore");
    const red15 = document.getElementById("r15");
    const red10 = document.getElementById("r10");
    const red5 = document.getElementById("r5");
    const blue15 = document.getElementById("b15");
    const blue10 = document.getElementById("b10");
    const blue5 = document.getElementById("b5");

    redTeamName.textContent = data.red_team_name;
    blueTeamName.textContent = data.blue_team_name;

    const r15 = parseInt(data.r15) || 0;
    const r10 = parseInt(data.r10) || 0;
    const r5 = parseInt(data.r5) || 0;
    const b15 = parseInt(data.b15) || 0;
    const b10 = parseInt(data.b10) || 0;
    const b5 = parseInt(data.b5) || 0;

    red15.textContent = r15;
    red10.textContent = r10;
    red5.textContent = r5;
    blue15.textContent = b15;
    blue10.textContent = b10;
    blue5.textContent = b5;

    const redScore = r15 * 15 + r10 * 10 + r5 * 5;
    const blueScore = b15 * 15 + b10 * 10 + b5 * 5;

    redTeamScore.textContent = redScore;
    blueTeamScore.textContent = blueScore;
}