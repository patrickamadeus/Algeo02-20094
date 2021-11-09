document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");
  
    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });
  
    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });
  
    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });
  
    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });
  
    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();
  
      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }
  
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });
  
  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
  
    // Removing Prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }
  
    // Kondisi tidak ada Thumbnail Element, pembuatan baru
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }
  
    thumbnailElement.dataset.label = file.name;
  
    // Show thumbnail buat image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
  
      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }

  
  const formImage = document.getElementById("reportImage");
  formImage.onsubmit = async function (event) {

    event.preventDefault();
    const inputFiles = document.getElementById("reportFile");
    const inputCompression = document.getElementById("reportCompression");
    const percentageShow = document.getElementById("perc");
    const downloadButton = document.getElementById("download-button");

    console.log(inputCompression.value);


    // conditional situation untuk tipe file yang di-upload
    if (inputFiles.files[0] !== undefined && inputFiles.files[0].type.startsWith("image/")){
      sessionStorage.clear();

      //buat download button jadi kelihatan
      if (downloadButton.style.display !== "block"){
        downloadButton.style.display = "block";
      }

      percentageShow.innerHTML = inputCompression.value + "% Compression";
  
      console.log("VALID");
      const reader = new FileReader();
      reader.readAsDataURL(inputFiles.files[0]);

      var beforeImg = document.getElementById('before-image');
      var afterImg = document.getElementById('after-image');

      beforeImg.src = URL.createObjectURL(inputFiles.files[0]);
      afterImg.src = URL.createObjectURL(inputFiles.files[0]);

      reader.addEventListener("load",() => {
        sessionStorage.setItem("image" , reader.result);
      })
    }
    else{
      if (downloadButton.style.display !== "none"){
        downloadButton.style.display = "none";
      }

      percentageShow.innerHTML = "Error!";
      console.log("NO");
    }
  };


  //toggle show result section
  const targetDiv = document.getElementById("compression-result");
  const submit = document.getElementById("show-button");

  submit.onclick = function () {
    if (targetDiv.style.display !== "block") {
      targetDiv.style.display = "block";
    }
    else{
      targetDiv.style.display = "none";
    }
  };


  //download compressed image section
  const btnDownload = document.querySelector("#download");
  const imgDownload = document.querySelector("#after-image");

  function getFileName(file){
    return file.substring(file.lastIndexOf('/') + 1);
  }
  
  
  btnDownload.addEventListener('click', () => {
    const path = imgDownload.getAttribute('src');
    saveAs(path,"compressed-image");
  })


  
  