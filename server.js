const fs = require("fs");
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

io.on("connection", (socket) => {
  console.log("Client connected");

  socket.on("updateTeams", (data) => {
    io.emit("updateTeams", data);
  });

  socket.on("saveTeams", (data) => {
    fs.writeFileSync("redTeam.json", JSON.stringify(data.red, null, 2));
    fs.writeFileSync("blueTeam.json", JSON.stringify(data.blue, null, 2));
  });
});

server.listen(4000, () => {
  console.log("Server listening on port 4000");
});
