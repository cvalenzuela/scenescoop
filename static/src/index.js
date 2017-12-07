/*
Client
*/

import { sendData } from './manageForm';
import { input, output, changeSource } from './video';
import { moviesList } from './movies';

let sceneSearch = false;
let movieSelected = false;
let currentSceneDescription = '';
let currentInputName = '';
const videoUploadRoute = '/upload';
const makeVideoRoute = '/make';
const outputVideosPath = 'videos/outputs'
let currentSelectedMovie = 'vertigo';

window.addEventListener("load", () => {
  const inputVideo = document.getElementById("inputVideo");
  const outputVideo = document.getElementById("outputVideo");
  const form = document.getElementById("form");
  const inputFileVideo = document.getElementById("inputFileVideo");
  const selectVideoBtn = document.getElementById("selectVideoBtn");
  const uploadVideoBtn = document.getElementById("uploadVideoBtn");
  const inputText = document.getElementById("inputText");
  const outputText = document.getElementById("outputText");
  const loadingTextInput = document.getElementById("loadingTextInput");
  const loadingTextOutput = document.getElementById("loadingTextOutput");
  const sceneSearchBtn = document.getElementById("sceneSearch");
  const dropdownBtn = document.getElementById('dropdownBtn');
  const dropdowns = document.getElementsByClassName("dropdown-content");
  const moviesDD = document.getElementById("moviesDD");

  // Create the dropdown Menu
  moviesList.forEach(e => {
    let d = document.createElement('a');
    d.dataset.file = e.file;
    d.innerText = e.name;
    d.addEventListener('click', () => {
      dropdownBtn.innerText = e.name;
      currentSelectedMovie = e.file;
      movieSelected = true;
      if(sceneSearch){
        updateSceneSearchBtn('ACTIVATE');
      }
    })
    moviesDD.appendChild(d);
  })

  // Manage the video preview
  const onSelectFile = () => {
    const file = inputFileVideo.files[0];
    currentInputName = file.name;
    const url = URL.createObjectURL(file);
    inputText.innerText = '';
    changeSource(input, url)
  };

  // Event Listeners
  dropdownBtn.addEventListener('click', () => {
    document.getElementById("moviesDD").classList.toggle("show");
  })
  inputFileVideo.addEventListener('change', onSelectFile, true);
  selectVideoBtn.addEventListener('click', () => {
    inputFileVideo.click();
  });
  uploadVideoBtn.addEventListener('click', () => {
    loadingTextInput.style.display = 'inline';
    updateSceneSearchBtn('DEACTIVATE');
    inputText.innerText = '';
    sceneSearch = false;
    event.preventDefault();
    sendData(form, { name: currentInputName }, videoUploadRoute, response => {
      response = JSON.parse(response);
      loadingTextInput.style.display = 'none';
      currentSceneDescription = response.content;
      inputText.innerText = response.content.charAt(0).toUpperCase() + response.content.slice(1);
      if (response.status == 200) {
        movieSelected && updateSceneSearchBtn('ACTIVATE');
        sceneSearch = true;
      }
    });
  });

  // Manage the scene search
  sceneSearchBtn.addEventListener('click', () => {
    if (sceneSearch && movieSelected) {
      loadingTextOutput.style.display = 'inline';
      updateSceneSearchBtn('DEACTIVATE');
      sceneSearch = false;
      outputText.innerText = '';
      const data = {
        name: currentInputName,
        duration: input.duration(),
        movie: currentSelectedMovie,
      }
      sendData(form, data, makeVideoRoute, response => {
        response = JSON.parse(response);
        loadingTextOutput.style.display = 'none';
        if (response.status == 200) {
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
    if (state == 'ACTIVATE') {
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

  // Un-toggle dropdown when click outside
  window.onclick = event => {
    if (!event.target.matches('#dropdownBtn')) {
      for (let i = 0; i < dropdowns.length; i++) {
        let openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
});