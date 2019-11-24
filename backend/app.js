let express = require('express');
let fs = require('fs');


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
    //console.log("gotEEEM" + JSON.stringify(data));
    socket.broadcast.emit("selectedCodes",data)
  });
  socket.on('disconnect', function (data){
    console.log("Socket Disconnected");
  });
  socket.on('profiles', function () {
    fs.readdir('./profiles', function(err, items) {
      if (err) {
        return console.log('Unable to scan directory: ' + err);
      }
      console.log(items);
      socket.broadcast.emit("frontEndProfiles",items)
    });
  });
  socket.on('profileSave', function (data) {
    let filePath = './profiles/'+data.profile+'.json';
    let profile = [{},{},{},{},{},{}];
    let newData = {listID: data.listID, data: data.data};
    let newProf = data.listID
    fs.readFile(filePath, function (err, data) {
      //3console.log(JSON.parse(data))
      for( let i in JSON.parse(data)){
        profile[i] = JSON.parse(data)[i];
      }
      profile[newProf] = newData;
      fs.writeFile(filePath,JSON.stringify(profile),function(err){
        // throws an error, you could also catch it here
        if (err) throw err;
        // success case, the file was saved
        console.log('Profile saved!');
      });

    });

  });

  socket.on('getProfile', function (data) {
    let filePath = './profiles/'+data+'.json';
    fs.readFile(filePath, function (err, data) {
      let newData = JSON.parse(data)
      socket.broadcast.emit("frontEndSavedProfile", newData)
      console.log("Sent Profile");
    });

  });

  socket.on('VideoSetting', function (data) {
     socket.broadcast.emit("backendVideoSettings", data)
  });

});
