// function handleCredentialResponse(response) {
//   formData = new FormData();
//   formData.append('jwt', response.credential);
//   fetch(authURL, {
//     method: "POST",
//     body: formData,
//     headers: {
//       "X-CSRFToken": csrf_token,
//     }
//   })
// }
// window.onload = function () {
//   google.accounts.id.initialize({
//     client_id: "129500516432-6rbd9893voa71k8dgpbrqo3hfi02rnhv.apps.googleusercontent.com",
//     ux_mode: "popup",
//     context: "use",
//     login_uri: authURL,
//   });
//   google.accounts.id.renderButton(
//     document.getElementById("gbutton"),
//     { theme: "outline", size: "large", text: "continue_with"}  // customization attributes
//   );
//   google.accounts.id.prompt(); // also display the One Tap dialog
// }
