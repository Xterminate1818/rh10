const socket = new WebSocket("ws://192.168.0.20:8080/view");
const mult = 1
const car1 = new Image();
car1.src = "/cars/1.png";
const car2 = new Image();
car2.src = "/cars/2.png";
const car3 = new Image();
car3.src = "/cars/3.png";
const car4 = new Image();
car4.src = "/cars/4.png";
const cars = [car1, car2, car3, car4];
const grass = new Image();
grass.src = "/grass.png"

let track = {x: [], y: [], length: 0};
let id = -1;

socket.onmessage = function (e) {
  let data = JSON.parse(e.data);
  if (data.track.x != null) {
    track = data.track
  }
  drawTrack();
  for (let i = 0; i < data.length; i += 1) {
    var car;
    let id = data.id[i];
    if (id == 11) {
      car = car1;
    } else if (id == 12) {
      car = car2;
    } else if (id == 13) {
      car = car3;
    } else {
      car = car4;
    }
    console.log(data.id[i]);
    drawCar(car, data.x[i], data.y[i], data.r[i] + (Math.PI / 2))
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
  ctx.lineWidth = 20;
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

function drawCar (car, positionX, positionY, angle ) {
  const canvas = document.getElementById("cv");
  const ctx = canvas.getContext("2d");
  ctx.save();
  ctx.translate( positionX, positionY );
  ctx.rotate( angle );
  ctx.drawImage( car, -25, -50 );
  ctx.restore();
}
