const socket = new WebSocket("ws://localhost:8080/view");
const mult = 1
const car1 = new Image()
car1.src = "/cars/1.png"
const car2 = new Image()
car2.src = "/cars/2.png"
const car3 = new Image()
car3.src = "/cars/3.png"
const car4 = new Image()
car4.src = "/cars/4.png"

let track = {x: [], y: [], length: 0};
let id = -1;

socket.onmessage = function (e) {
  let data = JSON.parse(e.data);
  if (data.track.x != null) {
    track = data.track
  }
  drawTrack();
  for (let i = 0; i < data.length; i += 1) {
    console.log(i)
    drawCar(data.x[i], data.y[i], data.r[i])
  }
}

function drawCircle(x, y, color) {
  const canvas = document.getElementById("cv");
  const ctx = canvas.getContext("2d");
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, 10.0, 0, 2 * Math.PI);
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
    ctx.lineTo(track.x[p] * mult, track.y[p] * mult);
    ctx.moveTo(track.x[p] * mult, track.y[p] * mult);
    ctx.stroke();
  }
  ctx.lineTo(track.x[0] * mult, track.y[0] * mult);
  ctx.stroke();
}

function drawCar(x, y, angle) {
  const canvas = document.getElementById("cv");
  const ctx = canvas.getContext("2d");
  ctx.save();
  ctx.translate((x - 25), (y - 50));
  ctx.rotate(angle);
  ctx.drawImage(car1, 0, 0);
  ctx.restore();
  //drawCircle(x * mult, y * mult, "rgb(255, 0, 0)")
}
