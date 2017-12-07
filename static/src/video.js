/*
Manage the videos
*/

import videojs from 'video.js';

// Input video
const input = videojs("inputVideo", {
  controls: true,
  autoplay: true,
  loop: true,
  preload: 'auto',
  width: 300
}, () => {
  console.log('video input ready')
});

input.read

const changeSource = (elt, source) => {
  const src = {
    src: source,
    type: 'video/mp4'
  }
  elt.src(src)
}

// Output video
const outputSource = {
  src: "videos/outputs/demo.mp4",
  type: 'video/mp4'
};

const output = videojs("outputVideo", {
  controls: true,
  autoplay: true,
  loop: true,
  preload: 'auto',
  width: 300
}, () => {
  console.log('video output ready')
});

output.on('ready', () => {
  //output.src(outputSource)
})

export {
  input,
  output,
  changeSource
}