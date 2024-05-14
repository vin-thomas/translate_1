function cleanup() {
    document.getElementById("textToTranslate").value = "";
    document.getElementById("translationOutput").innerHTML = "";
  }


const outputArea = document.getElementById("translationOutput");
const textarea = document.getElementById("textToTranslate");
const language = document.getElementById("languageSelect");
const loader = document.querySelector(".loader");


document.getElementById("submit_btn").addEventListener("click", (e) => {
    e.preventDefault();
    if(textarea.value != '') {
    loader.style.visibility = "visible";
    document.getElementById("submit_btn").disabled = true;

    text = textarea.value;
    lang = language.value;

    formData = new FormData();
    formData.append("text", text);
    formData.append("lang", lang);
    
    formDataString = new URLSearchParams(formData).toString();
    
    fetch(translateURL, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrftoken,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok.");
          }
          const reader = response.body.getReader();
          console.log("inside response of streamer");
          // Function to consume the streaming data
          const processStream = ({ value, done }) => {
            if (done) {
                console.log("all done!");
              return;
            }
            const chunk = new TextDecoder().decode(value);
            outputArea.innerHTML = '';
            loader.style.visibility = "hidden";
            outputArea.innerHTML += chunk;
            document.getElementById("submit_btn").disabled = false;
            return reader.read().then(processStream);
          };
            return reader.read().then(processStream);
          // }
        })
        .catch((error) => {
          console.error("There was a problem with the fetch operation:", error);
        });
    }
  });
