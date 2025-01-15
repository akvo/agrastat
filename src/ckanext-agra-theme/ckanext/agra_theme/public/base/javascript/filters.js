/* Agrovoc tags */
function appendTags(suggestion) {
  var tag_suggestions = $("#tag-suggestions");
  var loading_suggestions = $("#loading-tag-suggestions");
  var currentTags = $("#field-tags").val();
  currentTags = currentTags.split(",");
  if (currentTags.includes(suggestion)) {
    return;
  }
  // create tag suggestion using pill
  var pill = document.createElement("div");
  pill.className = "label";
  pill.onclick = function () {
    currentTags.push(suggestion);
    $("#field-tags").val(currentTags.join(","));
    $("#field-tags").trigger("change.select2");
    pill.remove();
  };
  console.log(currentTags);
  var plus = document.createElement("i");
  plus.className = "fa fa-plus";
  pill.appendChild(plus);
  var text = document.createElement("span");
  text.textContent = suggestion;
  pill.appendChild(text);
  loading_suggestions.remove();
  tag_suggestions.append(pill);
}

function handleTagChange(tag, query_params = "") {
  var api_url = "/api/2/util/tag/suggestion?q=" + tag + query_params;
  fetch(api_url)
    .then((response) => response.json())
    .then((data) => {
      data.forEach((suggestion) => {
        appendTags(suggestion);
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
    $("#field-title").on("change", function () {
      /* use title as suggestion if tag is empty */
      var field_tags_is_empty = $("#field-tags").val() === "";
      if (field_tags_is_empty) {
        var titles = $(this).val();
        var tag_suggestions = $("#tag-suggestions");
        tag_suggestions.empty();
        titles.split(" ").forEach((title) => {
          if (title.length > 3) {
            handleTagChange(title);
            appendTags(title);
          }
        });
      }
    });

    $("#field-tags").on("change.select2", function () {
      var field_tags_is_empty = $("#field-tags").val() === "";
      var tag_suggestions = $("#tag-suggestions");
      tag_suggestions.empty();
      const selectedTags = $(this).val();
      var loading_suggestions = document.createElement("div");
      loading_suggestions.id = "loading-tag-suggestions";
      loading_suggestions.className = "text-muted";
      loading_suggestions.textContent = "Loading suggestions...";
      tag_suggestions.append(loading_suggestions);
      var tags = selectedTags.split(",");
      if (tags.length) {
        var tag = tags[tags.length - 1];
        if (tag.length > 3) {
          handleTagChange(tag);
          handleTagChange(tag, "&category=children");
        }
      } else {
        loading_suggestions.remove();
      }
    });
    /* End of Agrovoc tags */
  });
}
