// Simple POST
// https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_forms_through_JavaScript

const sendData = (form, data, route ,callback) => {
  const XHR = new XMLHttpRequest();
  const FD = new FormData(form);
  for (const key in data){
    FD.set(key, data[key]);
  }
  
  XHR.addEventListener("load", event => {
    callback(event.target.responseText)
  });

  XHR.addEventListener("error", event => {
    console.log('Oups! Something goes wrong.');
  });

  XHR.open("POST", route);

  XHR.send(FD);
}

export { sendData }