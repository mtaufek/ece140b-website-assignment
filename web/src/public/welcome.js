function add_user() {
  var firstname = document.getElementById('firstname').value;
  var lastname = document.getElementById('lastname').value;
  var email = document.getElementById('email').value;
  var comment = document.getElementById('comment').value;
  var x = document.getElementById("alert");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
  var new_user = {
    "firstname": firstname,
    "lastname": lastname,
    "email": email,
    "comment": comment
  }
  fetch('add_user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(new_user),
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      alert("Thank you for visiting!");
    })
    .catch((error) => {
      console.error('Error!!!');
    });

}