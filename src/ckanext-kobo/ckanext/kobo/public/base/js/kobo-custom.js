/* Image Upload with Kobo Button */
/* Image Upload
 *
 */

document.addEventListener("DOMContentLoaded", () => {
  const finalUrl = document.getElementById("field-image-url");
  const kfUrlField = document.getElementById("field-kf-url");
  const hashField = document.getElementById("field-hash");
  const assetUidField = document.getElementById("field-asset-uid");
  const exportSettingsUidField = document.getElementById(
    "field-export-settings-uid",
  );

  const logConstructedUrl = () => {
    const kfUrl = kfUrlField.value;
    const assetUid = assetUidField.value;
    const exportSettingsUid = exportSettingsUidField.value;

    if (kfUrl && assetUid && exportSettingsUid) {
      const mergedUrl = `${window.location.protocol}//${window.location.host}/api/2/kobo/${assetUid}`;
      finalUrl.value = mergedUrl;
      hashField.value = assetUid;
    }
  };

  kfUrlField.addEventListener("change", logConstructedUrl);
  assetUidField.addEventListener("input", logConstructedUrl);
  exportSettingsUidField.addEventListener("input", logConstructedUrl);
});
