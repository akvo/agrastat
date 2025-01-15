/* Agrovoc tags */
function handleTagChange(tags, query_params = "") {
  var tag = tags[tags.length - 1];
  var tag_suggestions = $("#tag-suggestions");
  var api_url = "/api/2/util/tag/suggestion?q=" + tag + query_params;
  var loading_suggestions = $("#loading-tag-suggestions");
  fetch(api_url)
    .then((response) => response.json())
    .then((data) => {
      data.forEach((suggestion) => {
        // create tag suggestion using pill
        var pill = document.createElement("div");
        pill.className = "label";
        pill.onclick = function () {
          var currentTags = $("#field-tags").val();
          currentTags = currentTags.split(",");
          currentTags.push(suggestion);
          $("#field-tags").val(currentTags.join(","));
          $("#field-tags").trigger("change.select2");
        };
        var plus = document.createElement("i");
        plus.className = "fa fa-plus";
        pill.appendChild(plus);
        var text = document.createElement("span");
        text.textContent = suggestion;
        pill.appendChild(text);
        loading_suggestions.remove();
        tag_suggestions.append(pill);
      });
    });
}
/* End of Agrovoc tags */

/* only for /dataset/edit/xxx or /dataset/new */
if (
  window.location.pathname.includes("/dataset/edit/") ||
  window.location.pathname === "/dataset/new"
) {
  $(document).ready(function () {
    var countryDropdown = $("#field-country");

    /* Country list */
    fetch("/api/2/util/countries")
      .then((response) => response.json())
      .then((data) => {
        // Populate the dropdown with countries
        data.forEach((country) => {
          var option = document.createElement("option");
          option.value = country.code;
          option.textContent = country.name;
          countryDropdown.append(option);
        });
      });
    /* End of Country list */

    /* Agrovoc tags */
    $("#field-tags").on("change.select2", function () {
      const selectedTags = $(this).val();
      var tag_suggestions = $("#tag-suggestions");
      tag_suggestions.empty();
      var loading_suggestions = document.createElement("div");
      loading_suggestions.id = "loading-tag-suggestions";
      loading_suggestions.className = "text-muted";
      loading_suggestions.textContent = "Loading suggestions...";
      tag_suggestions.append(loading_suggestions);
      handleTagChange(selectedTags.split(","));
      handleTagChange(selectedTags.split(","), "&category=children");
    });
    /* End of Agrovoc tags */
  });
}
