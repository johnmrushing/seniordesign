let express = require('express');

// const serial = require('serialport');
// serial.list((err, ports) => {
//   console.log(ports)
// })
// const port = new serial('COM1')

let app = express();
let server = require('http').createServer(app);
let num = 0;
let io = require('socket.io').listen(server);
server.listen(80);

io.on('connection', function (socket) {
  console.log("Connected successfully to the socket...");

  socket.on('obd-in', function (data){
    socket.broadcast.emit("obd-out", data);
  });

  socket.on('begin',function (data) {
      socket.broadcast.emit("start",data)
  });

  socket.on('end',function (data) {
    socket.broadcast.emit("stop",data)
  });

  socket.on('possibleCodes',function (data) {
    socket.broadcast.emit("frontEndPossibleCodes",data)
  });

  socket.on('userSelectedCodes',function (data) {
    socket.broadcast.emit("selectedCodes",data)
  });
  socket.on('disconnect', function (data){
    console.log("Socket Disconnected");
  });

});
