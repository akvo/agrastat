// country list
// only for /dataset/edit/xxx or /dataset/new
if (
  window.location.pathname.includes("/dataset/edit/") ||
  window.location.pathname === "/dataset/new"
) {
  document.addEventListener("DOMContentLoaded", function () {
    const countryDropdown = document.getElementById("field-country");

    // Fetch countries from the API when the page loads
    fetch("/api/countries")
      .then((response) => response.json())
      .then((data) => {
        // Populate the dropdown with countries
        data.forEach((country) => {
          const option = document.createElement("option");
          option.value = country.code;
          option.textContent = country.name;
          countryDropdown.appendChild(option);
        });
      });

    // Optional: Add autocomplete functionality
    const searchInput = document.querySelector('[data-module="autocomplete"]');
    searchInput.addEventListener("input", function () {
      const query = searchInput.value;

      fetch(`/api/countries?q=${query}`)
        .then((response) => response.json())
        .then((data) => {
          // Clear the dropdown
          countryDropdown.innerHTML =
            '<option value="">{{ _("Select a country") }}</option>';

          // Populate with filtered countries
          data.forEach((country) => {
            const option = document.createElement("option");
            option.value = country.code;
            option.textContent = country.name;
            countryDropdown.appendChild(option);
          });
        });
    });
  });
  $(document).ready(function () {
    // Select the Select2 element by its ID
    $("#field-tags").on("change.select2", function () {
      // Get the current value(s)
      const selectedTags = $(this).val();
      console.log("Selected tags:", selectedTags);

      // Perform your custom action here
      handleTagChange(selectedTags);
    });

    // Example custom action
    function handleTagChange(tags) {
      alert("Tags updated to: " + tags);
    }
  });
}
