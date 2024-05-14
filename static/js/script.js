function cleanup() {
    document.getElementById("textToTranslate").value = "";
    document.getElementById("translationOutput").innerHTML = "";
  }


const outputArea = document.getElementById("translationOutput");
const textarea = document.getElementById("textToTranslate");
const language = document.getElementById("languageSelect");
const loader = document.querySelector(".loader");


document.getElementById("translationForm").addEventListener("submit", (e) => {
    e.preventDefault();
    if(textarea.value != '') {
    loader.style.visibility = "visible";
    document.getElementById("submit_btn").disabled = true;

    text = textarea.value;
    lang = language.value;

    formData = new FormData();
    formData.append("text", text);
    formData.append("lang", lang);
    
    fetch(translateURL, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken
        },
        body: formData
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Assuming response is JSON
    })
    .then(data => {
        outputArea.innerHTML = '';
        loader.style.visibility = "hidden";
        outputArea.innerHTML = data.translation;
        document.getElementById("submit_btn").disabled = false;
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation
        console.error('Fetch error:', error);
    });
    }
  });
