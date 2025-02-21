const teams = {
  red1: { name: "Red Warriors", image: "red-warriors.png" },
  red2: { name: "Red Dragons", image: "red-dragons.png" },
  red3: { name: "Red Falcons", image: "red-falcons.png" },
  blue1: { name: "Blue Sharks", image: "blue-sharks.png" },
  blue2: { name: "Blue Phoenix", image: "blue-phoenix.png" },
  blue3: { name: "Blue Thunder", image: "blue-thunder.png" },
};

redTeamSelect.addEventListener("change", function () {
  redTeamImage.src = teams[this.value].image;
  redTeamImage.alt = teams[this.value].name;
});

blueTeamSelect.addEventListener("change", function () {
  blueTeamImage.src = teams[this.value].image;
  blueTeamImage.alt = teams[this.value].name;
});

function setTeams() {
  const selectedRedTeam = redTeamSelect.value;
  const selectedBlueTeam = blueTeamSelect.value;
  const teamData = {
    red: teams[selectedRedTeam],
    blue: teams[selectedBlueTeam],
  };

  socket.emit("updateTeams", teamData);
  socket.emit("saveTeams", teamData);
}
