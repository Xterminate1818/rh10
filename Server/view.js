const socket = new WebSocket("ws://localhost:8080/view");

let track = {x: [], y: [], length: 0};
let car = {x: 10.0, y: 10.0};
let id = -1;

socket.onmessage = function (e) {
  let data = JSON.parse(e.data);
  id = data.id;
  console.log(data);
  if (data.kind == "reset") {
    track = data.track;
  }   
  car.x = data.inputs[0];
  car.y = data.inputs[1];
  drawTrack();
  drawCar();
  drawCircle(data.inputs[5], data.inputs[6], "rgb(0, 255, 0)")
}

function drawCircle(x, y, color) {
  const canvas = document.getElementById("cv");
  const ctx = canvas.getContext("2d");
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.arc(car.x, car.y, 10.0, 0, 2 * Math.PI);
  ctx.stroke();
}

function drawTrack() {
  const canvas = document.getElementById("cv");
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "rgb(0, 0, 0)";
  ctx.fillRect(0, 0, 500, 500);
  ctx.strokeStyle = "rgb(255, 255, 255)"
  ctx.lineWidth = 4;
  ctx.moveTo(track.x[0], track.x[0]);
  ctx.beginPath();
  for (let p = 0; p < track.length; p += 1) {
    ctx.lineTo(track.x[p], track.y[p]);
    ctx.moveTo(track.x[p], track.y[p]);
    ctx.stroke();
  }
  ctx.lineTo(track.x[0], track.y[0]);
  ctx.stroke();
}

function drawCar() {
  drawCircle(car.x, car.y, "rgb(255, 0, 0)")
}
