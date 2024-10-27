
function send(id) {
  const socket = new WebSocket("ws://192.168.0.20:8080/bots");
  socket.onopen = function(e) {
    socket.send(JSON.stringify({
      throttle: 0.0,
      steer: 0.0,
      breaking: 0.0,
      id: id,
    }));
    socket.close();
  }
}

