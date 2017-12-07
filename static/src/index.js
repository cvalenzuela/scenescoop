/*
Client
*/

import { sendData } from './manageForm';
import { input, output, changeSource } from './video';

let sceneSearch = false;
let currentSceneDescription = '';
let currentInputName = '';
const videoUploadRoute = '/upload';
const makeVideoRoute = '/make';
const outputVideosPath = 'videos/outputs'

window.addEventListener("load", () => {
  const inputVideo = document.getElementById("inputVideo");
  const outputVideo = document.getElementById("outputVideo");
  const form = document.getElementById("form");
  const inputFileVideo = document.getElementById("inputFileVideo");
  const inputText = document.getElementById("inputText");
  const outputText = document.getElementById("outputText");
  const loadingTextInput = document.getElementById("loadingTextInput");
  const loadingTextOutput = document.getElementById("loadingTextOutput");
  const sceneSearchBtn = document.getElementById("sceneSearch");
  const movies = document.getElementById("movies");

  // Manage the video preview
  const onSelectFile = () => {
    const file = inputFileVideo.files[0];
    currentInputName = file.name;
    const url = URL.createObjectURL(file);
    inputText.innerText = '';
    changeSource(input, url)
  };

  // Event Listeners
  inputFileVideo.addEventListener('change', onSelectFile, true)

  // Manage the video upload
  form.addEventListener("submit", event => {
    loadingTextInput.style.display = 'inline';
    updateSceneSearchBtn('DEACTIVATE');
    inputText.innerText = '';
    sceneSearch = false;
    event.preventDefault();
    sendData(form, { name: currentInputName }, videoUploadRoute,  response => {
      response = JSON.parse(response);
      loadingTextInput.style.display = 'none';
      currentSceneDescription = response.content;
      inputText.innerText = response.content.charAt(0).toUpperCase() + response.content.slice(1);
      if(response.status == 200){
        updateSceneSearchBtn('ACTIVATE');
        sceneSearch = true;
      }
    });
  });

  // Manage the new scene search
  sceneSearchBtn.addEventListener('click', () => {
    if (true){
      loadingTextOutput.style.display = 'inline';
      updateSceneSearchBtn('DEACTIVATE');
      sceneSearch = false;
      outputText.innerText = '';
      const data = { 
        name: currentInputName,
        duration: input.duration(),
        movie: movies.value,
      }
      sendData(form, data, makeVideoRoute, response => {
        response = JSON.parse(response);
        loadingTextOutput.style.display = 'none';
        if(response.status == 200){
          const description = response.movie.scene_closest_meaning;
          outputText.innerText = description.charAt(0).toUpperCase() + description.slice(1);
          updateSceneSearchBtn('ACTIVATE');
          sceneSearch = true;
          changeSource(output, `${outputVideosPath}${response.movie.name}`)
        }
      });
    }
  });

  // Utils
  const updateSceneSearchBtn = state => {
    let background, color, cursor;
    if(state == 'ACTIVATE'){
      background = '#2d8258';
      color = '#f7f7f7';
      cursor = 'pointer';
    } else {
      background = '#353535';
      color = '#7d7d7d';
      cursor = 'inherit';
    }
    sceneSearchBtn.style.background = background;
    sceneSearchBtn.style.color = color;
    sceneSearchBtn.style.cursor = cursor;
  }

});