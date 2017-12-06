/*
Client
*/

import { sendData } from './manageForm';

window.addEventListener("load", () => {
  const inputVideo = document.getElementById("inputVideo");
  const outputVideo = document.getElementById("outputVideo");
  const form = document.getElementById("form");
  const inputFileVideo = document.getElementById("inputFileVideo")

  const onSelectFile = () => {
    const file = inputFileVideo.files[0];
    const url = URL.createObjectURL(file);
    inputVideo.setAttribute('src', url)

  };

  inputFileVideo.addEventListener('change', onSelectFile, true)

  form.addEventListener("submit", event => {
    const name = (new Date()).getTime();
    event.preventDefault();

    
    sendData(form, { name }, updateInputVideo);
  });

});