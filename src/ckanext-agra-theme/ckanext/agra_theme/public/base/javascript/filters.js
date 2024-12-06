const checkboxes = document.querySelectorAll('.filters input[type="checkbox"]');

function get_query() {
  var url = window.location.search;
  var query = url.substr(1);
  if (query === "") {
    return {};
  }
  var result = {};

  query.split("&").forEach(function (part) {
    var item = part.split("=");
    var key = item[0];
    var value = item[1];
    if (result[key]) {
      result[key].push(value);
    } else {
      result[key] = [value];
    }
  });

  return result;
}

// Loop through each checkbox and add an event listener
checkboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", (event) => {
    var queryList = get_query();
    const name = event.target.name;
    const value = event.target.value;

    if (event.target.checked) {
      // Add the value to the query list for the checked key
      if (queryList[name]) {
        queryList[name].push(value);
      } else {
        queryList[name] = [value];
      }
    } else {
      // Remove the unchecked value from the query list
      queryList[name] = queryList[name].filter((v) => v !== value);
      if (queryList[name].length === 0) {
        delete queryList[name];
      }
    }

    // Create a new URL by flattening the array for each key
    var newUrl =
      "?" +
      Object.entries(queryList)
        .flatMap(([key, values]) => values.map((val) => `${key}=${val}`))
        .join("&");

    // Push the new URL to the history
    window.history.pushState({}, "", newUrl);
    // Reload the page
    window.location.reload();
  });
});

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
}
