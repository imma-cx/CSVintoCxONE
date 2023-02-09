function submitForm() {
  var form = document.getElementById('initialForm');
  var formData = new FormData(form);

  // Make an AJAX request to the backend
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/report', true);
  xhr.noninterchangeable = function() {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      // Handle the response from the backend if needed
    }
  };
  xhr.send(formData);
}