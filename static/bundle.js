(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
"use strict";

var _manageForm = require("./manageForm");

window.addEventListener("load", function () {
  var inputVideo = document.getElementById("inputVideo");
  var outputVideo = document.getElementById("outputVideo");
  var form = document.getElementById("form");
  var inputFileVideo = document.getElementById("inputFileVideo");

  var onSelectFile = function onSelectFile() {
    var file = inputFileVideo.files[0];
    var url = URL.createObjectURL(file);
    inputVideo.setAttribute('src', url);
  };

  inputFileVideo.addEventListener('change', onSelectFile, true);

  form.addEventListener("submit", function (event) {
    var name = new Date().getTime();
    event.preventDefault();

    (0, _manageForm.sendData)(form, { name: name }, updateInputVideo);
  });
}); /*
    Client
    */

},{"./manageForm":2}],2:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
// Simple POST
// https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_forms_through_JavaScript

var sendData = function sendData(form, data, callback) {
  var XHR = new XMLHttpRequest();
  var FD = new FormData(form);
  for (var key in data) {
    FD.set(key, data[key]);
  }

  XHR.addEventListener("load", function (event) {
    callback(event.target.responseText);
  });

  XHR.addEventListener("error", function (event) {
    console.log('Oups! Something goes wrong.');
  });

  XHR.open("POST", "/video");

  XHR.send(FD);
};

exports.sendData = sendData;

},{}]},{},[1]);
