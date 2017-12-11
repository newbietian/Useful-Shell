/**
 * Created by qinsw on 12/11/17.
 */
'use strict';

const IP_ADDRESS = "127.0.0.1";
const PORT = "11528";

const DEBUG = true;

function printLog(msg) {
  DEBUG && console.log(msg);
}

function Commander (ip, port) {
  this._socket = undefined;
  this._ip = ip;
  this._port = port;
}

Commander.prototype.getYlogPort = function () {
  return YLOG_PORT;
};

Commander.prototype.getSlogPort = function () {
  return SLOG_PORT;
};

Commander.prototype.getIP = function () {
  return IP_ADDRESS;
};

Commander.prototype.connect = function () {
  printLog(this._ip + this._port);
  this._socket = window.navigator.mozTCPSocket.open(this._ip, this._port);
  return this;
};

Commander.prototype.ondata = function (callback) {
  if (!this._socket) {
    return null;
  }
  this._socket.ondata = callback;
  return this;
};

Commander.prototype.onerror = function (callback) {
  if (!this._socket) {
    return null;
  }
  this._socket.onerror = callback;
  return this;
};

Commander.prototype.onopen = function (callback) {
  if (!this._socket) {
    return null;
  }
  this._socket.onopen = callback;
  return this;
};

Commander.prototype.onclose = function (callback) {
  if (!this._socket) {
    return null;
  }
  this._socket.onclose = callback;
  return this;
};

//发送命令
Commander.prototype.send = function (message) {
  if (!this._socket) {
    printLog("client - Socket have not been initialized");
    return;
  }
  if (!message) {
    printLog("client - message is empty");
    return;
  }
  printLog("client - send message = " + message);
  message += "\r\n";
  if (this.hasConnected()) {
    this._socket.send(message);
  } else {
    printLog("client - connection has not established");
  }
};

Commander.prototype.disconnect = function () {
  if (!this._socket) {
    printLog("client - Socket have not been initialized");
    return;
  }
  this._socket.close();
  this._socket = null;
};

Commander.prototype.hasConnected = function () {
  if (!this._socket) {
    printLog("client - Socket have not been initialized");
    return false;
  }
  return this._socket.readyState == "open";
};

Commander.prototype.mockServer = function (port) {
  var serverSocket = window.navigator.mozTCPSocket.listen(port);
  serverSocket.onconnect = function (event) {
    printLog("server -----------------------------");
    if (event && event.socket) {
      var socket = event.socket;
      printLog("Server - connection");

      socket.ondata = function (event) {
        printLog("server receive- " + event.data);
        if(event.data.indexOf(SLOG_CP_TYPE_GNSS) > -1) {
          socket.send("OK ON\n")
        } else {
          socket.send("OK 1024\n");
        }
      };

      socket.onclose = function () {
        printLog("server - disconnected!");
      };
    }
  }
};