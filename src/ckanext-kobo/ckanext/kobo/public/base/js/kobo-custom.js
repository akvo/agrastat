/* Image Upload with Kobo Button */
/* Image Upload
 *
 */

document.addEventListener("DOMContentLoaded", () => {
  const validateKoboButton = document.getElementById("validate-kobo");
  const finalUrl = document.getElementById("field-image-url");
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
      const name = document.getElementById("field-name");

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
            if (name.value === "") {
              name.value = data.name;
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
