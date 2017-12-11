/**
 * Created by qinsw on 12/11/17.
 */

var msg = document.getElementById("msg");
var connect = document.getElementById("connect");
var send = document.getElementById("send");

var orig_color = connect.getAttribute("color");
// Create WebSocket connection.
var socket;
var timer = 1;

connect.addEventListener("click", function (event) {
  console.log("hahahaha");
  if (timer > 1) {
    return;
  }
  timer = 2;
  connect.setAttribute("color","#101010");
  socket= new WebSocket('ws://localhost:11528');
// Connection opened
  socket.addEventListener('open', function (event) {
    console.log("socket opened~")
  });
// Listen for messages
  socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
  });
  socket.addEventListener('close',function (event) {
    console.log("Connection closed! reset timer == 1");
    timer = 1;
    connect.setAttribute("color",orig_color);
  })
});

send.addEventListener("click", function (event) {
  console.log("hahahaha");
  socket.send("command:open");
});


// var webClient = new Commander(IP_ADDRESS, PORT);
// function sendCommand(message) {
//   webClient.connect()
//     .ondata(function (event) {
//       if (!event.data){
//         return;
//       }
//       if (typeof event.data == 'string'){
//         console.log("event data == " + event.data)
//       }
//     })
//     .onopen(function () {
//       console.log("webclient open")
//       webClient.send("open send mf")
//     })
//     .onerror(function (event) {
//       console.log("error type = " + event.type + ", data = " + event.data)
//     })
//     .onclose(function () {
//       console.log("onclose")
//     });
// }


