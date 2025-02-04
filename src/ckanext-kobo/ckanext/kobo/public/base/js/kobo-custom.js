/* Image Upload with Kobo Button */
/* Image Upload
 *
 */

document.addEventListener("DOMContentLoaded", () => {
  const validateKoboButton = document.getElementById("validate-kobo");
  const finalUrl = document.getElementById("field-resource-url");
  const kfUrlField = document.getElementById("field-kf-url");
  const hashField = document.getElementById("field-hash");
  const assetUidField = document.getElementById("field-asset-uid");
  const tokenField = document.getElementById("field-kobo-token");

  const logConstructedUrl = () => {
    const kfUrl = kfUrlField.value;
    const assetUid = assetUidField.value;
    const token = tokenField.value;

    if (kfUrl && assetUid && token) {
      validateKoboButton.classList.remove("btn-danger");
      validateKoboButton.classList.add("btn-info");
      validateKoboButton.innerHTML = "Validate";
      validateKoboButton.classList.remove("disabled");
      const mergedUrl = `${window.location.protocol}//${window.location.host}/api/2/kobo/${assetUid}`;
      finalUrl.value = mergedUrl;
      finalUrl.readOnly = true;
      hashField.value = assetUid;
    } else {
      validateKoboButton.classList.add("disabled");
    }
  };

  const getInfo = () => {
    if (!validateKoboButton.classList.contains("disabled")) {
      // add loading spinner
      validateKoboButton.innerHTML = `<i class="fa fa-spinner fa-spin"></i> Validating...`;
      const kfUrl = kfUrlField.value;
      const assetUid = assetUidField.value;
      const token = tokenField.value;
      const nameField = document.getElementById("field-name");

      if (kfUrl && assetUid && token) {
        const kfUrlValue = kfUrl.replace("https://", "");
        fetch(`/api/2/kobo-info/${token}/${assetUid}/${kfUrlValue}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            if (nameField.value === "") {
              nameField.value = data.name;
            }
            validateKoboButton.innerHTML = `<i class="fa fa-check"></i> Validated`;
            validateKoboButton.classList.remove("btn-info");
            validateKoboButton.classList.add("btn-success");
          })
          .catch((error) => {
            console.error("Error:", error);
            validateKoboButton.innerHTML = `<i class="fa fa-times"></i> Error`;
            validateKoboButton.classList.remove("btn-info");
            validateKoboButton.classList.add("btn-danger");
          })
          .finally(() => {
            validateKoboButton.classList.remove("disabled");
          });
      }
    }
  };

  if (kfUrlField && assetUidField && tokenField) {
    kfUrlField.addEventListener("change", logConstructedUrl);
    assetUidField.addEventListener("input", logConstructedUrl);
    validateKoboButton.addEventListener("click", getInfo);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const uploadDiv = document.getElementById("field-resource-upload-block");

  const uploadField = document.getElementById("field-resource-upload");
  const urlField = document.getElementById("field-resource-url");
  const urlKoboFields = document.getElementById("kobo-inputs");

  const removeUpload = document.getElementById("remove-upload");
  const alertDiv = document.getElementById("info-alert");

  const buttonUpload = document.getElementById("button-upload");
  const buttonKobo = document.getElementById("button-kobo");

  const showUpload = () => {
    uploadDiv.style.display = "block";
    urlKoboFields.style.display = "none";
    buttonUpload.classList.add("active");
    buttonUpload.classList.add("btn-info");
    buttonUpload.classList.remove("btn-label");
    buttonKobo.classList.add("btn-label");
    buttonKobo.classList.remove("active");
    buttonKobo.classList.remove("btn-info");
  };

  const showKobo = () => {
    if (uploadField.value) {
      alertDiv.innerHTML = `You have already uploaded a file. If you want to use Kobo, please remove the file first.`;
      alertDiv.style.display = "block";
    } else {
      uploadDiv.style.display = "none";
      urlKoboFields.style.display = "block";
      buttonKobo.classList.add("active");
      buttonKobo.classList.add("btn-info");
      buttonKobo.classList.remove("btn-label");
      buttonUpload.classList.add("btn-label");
      buttonUpload.classList.remove("active");
      buttonUpload.classList.remove("btn-info");
    }
  };

  if (removeUpload) {
    removeUpload.addEventListener("click", () => {
      uploadField.value = "";
      urlField.value = "";
      const nameField = document.getElementById("field-name");
      nameField.value = "";
      alertDiv.style.display = "none";
    });
  }

  if (buttonUpload && buttonKobo) {
    buttonUpload.addEventListener("click", showUpload);
    buttonKobo.addEventListener("click", showKobo);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  // Upload File change event
  const uploadField = document.getElementById("field-resource-upload");
  const nameField = document.getElementById("field-name");

  if (uploadField) {
    uploadField.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file) {
        if (nameField.value === "") {
          nameField.value = file.name;
        }
      }
    });
  }
});
