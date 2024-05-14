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
    
        outputArea.innerHTML = '';
        const reader = response.body.getReader();
        console.log("inside response of streamer");
    
        const processStream = ({ value, done }) => {
            if (done) {
                console.log("Stream complete");
                loader.style.visibility = "hidden";
                document.getElementById("submit_btn").disabled = false;
                return;
            }
    
            const chunk = new TextDecoder().decode(value);
            outputArea.innerHTML += chunk;
    
            return reader.read().then(processStream);
        };
    
        reader.read().then(processStream);
    })
    .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
    });
    }
  });
