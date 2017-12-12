/**
 * Created by qinsw on 12/11/17.
 */

// Communication protocol
//     command:[Action]->[system command]
//         open: open the file with system command
//         other: not be handled temporary
//      e.g "command:open->gedit /home/qinsw/pengtian/shell/test.sh"

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

  socket.addEventListener('open', function (event) {
    console.log("socket opened~")
  });

  socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
  });

  socket.addEventListener('close',function (event) {
    console.log("Connection closed! reset timer == 1");
    timer = 1;
    connect.setAttribute("color",orig_color);
  })

});

var test_file_path = "/home/qinsw/Downloads/null.log";
send.addEventListener("click", function (event) {
  console.log("hahahaha");
  socket.send("command:open->gedit " + "'" + test_file_path + "'" + "<-");
});


