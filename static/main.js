var downloadButton = document.getElementById('download-button');
var outputContainer = document.getElementById('output-container');

var form = document.querySelector('form');
var outputContainer = document.querySelector('#output-container');
const imageContainer = document.querySelector('#image-container');
const downloadLink = document.querySelector('#download-link');
const loader = document.querySelector('#Loader');

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  var formData = new FormData(form);
  // var xhr = new XMLHttpRequest();
  // xhr.open('POST', '/process-image');
  // xhr.onload = function() {

  // };
  // xhr.send(formData);
  loader.classList.remove('hidden');
  const response = await fetch('/process-image/', {
    method: 'POST',
    body: formData,
  });

  if (response.status == 200) {
    const data = await response.json();
    imageContainer.innerHTML = `<img src="${data.thumnail}" style="width:100%; max-height:400px"/>`;
    downloadLink.setAttribute('href', data.thumnail);
  } else {
    alert('You need to provide the all data');
  }
  loader.classList.add('hidden');
});
