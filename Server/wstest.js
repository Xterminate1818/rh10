const socket = new WebSocket("ws://192.168.0.20:8080/bots");

let track = {x: [], y: [], length: 0};
let car = {x: 10.0, y: 10.0};
let id = -1;

socket.onopen = function(e) {
  socket.send(JSON.stringify({
    throttle: 0.0,
    steer: 0.0,
    breaking: 0.0,
    id: 1,
  }));
}

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
}


function formSubmit(e) {
  e.preventDefault();
  const throttle = document.getElementById("throttle");
  const steer = document.getElementById("steer");
  const breaking = document.getElementById("break");
  let s = JSON.stringify({
    throttle: parseFloat(throttle.value),
    steer: parseFloat(steer.value),
    breaking: parseFloat(breaking.value),
    id: id
   });
  socket.send(s);
}

function init() {
  const form = document.getElementById("test-form");
  form.addEventListener("submit", formSubmit);
}

function drawCircle(x, y) {
  const canvas = document.getElementById("cv");
  const ctx = canvas.getContext("2d");
  ctx.strokeStyle = "rgb(255, 0, 0)";
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
  drawCircle(car.x, car.y)
}

window.addEventListener("DOMContentLoaded", init)
