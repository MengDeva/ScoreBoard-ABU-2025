function setTeams() {
  const redTeam = document.getElementById("redTeamSelect").value;
  const blueTeam = document.getElementById("blueTeamSelect").value;

  const data = { redTeam, blueTeam };

  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.text())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
