// dashboard-view.js
function removeGrid(id) {
  // Step 1: Remove the configuration from the existingConfigs array
  var existingConfigs = [];
  try {
    existingConfigs = JSON.parse(
      document.getElementById("columns-input").value,
    );
  } catch (e) {
    console.error("Error parsing existing configurations:", e);
    existingConfigs = [];
  }

  // Filter out the configuration with the matching ID
  existingConfigs = existingConfigs.filter((config) => config.id !== id);

  // Update the hidden input field with the updated configurations
  document.getElementById("columns-input").value =
    JSON.stringify(existingConfigs);

  // Step 2: Remove the grid item from the DOM
  var gridItemToRemove = document.querySelector(`#viz_grid_${id}`);
  if (gridItemToRemove) {
    gridItemToRemove.remove();
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Check the current value of the select element on page load
  var currentType = document.getElementById("visualType").value;
  document
    .getElementById("numberOptions")
    .classList.toggle("hidden", currentType !== "number");
  document
    .getElementById("chartOptions")
    .classList.toggle("hidden", currentType !== "chart");

  // Toggle visibility of options based on visualization type
  document.getElementById("visualType").addEventListener("change", function () {
    var type = this.value;
    document
      .getElementById("numberOptions")
      .classList.toggle("hidden", type !== "number");
    document
      .getElementById("chartOptions")
      .classList.toggle("hidden", type !== "chart");
  });

  document.getElementById("saveVisual").addEventListener("click", function () {
    // Step 1: Gather form data for the new visualization
    var gridSize = document.getElementById("gridSize").value;
    var title = document.getElementById("visualTitle").value || "Untitled";
    var visualType = document.getElementById("visualType").value;

    // Generate a unique ID for the new visualization
    var id = Math.random().toString(36).substr(2, 9);

    // Create the configuration object for the new visualization
    var newConfig = {
      id: id, // Use the generated ID
      gridSize: gridSize,
      title: title,
      visualizationType: visualType,
    };

    if (visualType === "chart") {
      newConfig.chartType = document.getElementById("chartType").value;
      newConfig.xAxis =
        document.getElementById("xAxis").value || "X-Axis Placeholder";
      newConfig.yAxis =
        document.getElementById("yAxis").value || "Y-Axis Placeholder";
    } else if (visualType === "number") {
      newConfig.numberType =
        document.getElementById("numberType").value || "Average";
      newConfig.numberColumn = document.getElementById("numberColumn").value;
    }

    // Step 2: Collect all existing configurations
    var existingConfigs = [];
    try {
      existingConfigs = JSON.parse(
        document.getElementById("columns-input").value,
      );
    } catch (e) {
      console.error("Error parsing existing configurations:", e);
      existingConfigs = [];
    }

    // Step 3: Add the new configuration to the list
    existingConfigs.push(newConfig);

    // Step 4: Serialize the updated list and update the hidden input field
    document.getElementById("columns-input").value =
      JSON.stringify(existingConfigs);

    // Step 5: Create the outer container (col-md-4)
    var outerContainer = document.createElement("div");
    outerContainer.classList.add(gridSize);
    outerContainer.setAttribute("id", `viz_grid_${id}`); // Unique ID for the container

    // Step 6: Create the grid item container
    var gridItem = document.createElement("div");
    gridItem.classList.add(
      "grid-item",
      "panel",
      "panel-default",
      "text-center",
      "visualization-grid-item",
    );

    // Step 7: Create the panel body
    var panelBody = document.createElement("div");
    panelBody.classList.add("panel-body");

    // Step 8: Build the content
    var content = `<strong>${title}</strong><br>`;
    if (visualType === "chart") {
      content += `<small>Type: ${newConfig.chartType} Chart</small><br>
                <small>X-Axis: ${newConfig.xAxis}</small><br>
                <small>Y-Axis: ${newConfig.yAxis}</small><br>`;
    } else if (visualType === "number") {
      content += `<small>Type: Number (${newConfig.numberType})</small><br>
                <small>Value: ${newConfig.numberColumn}</small><br>`;
    }

    // Append the content to the panel body
    panelBody.innerHTML = content;

    // Step 9: Add the "X" link for removal
    var closeLink = document.createElement("a");
    closeLink.classList.add("remove-grid"); // Add the "remove-grid" class
    closeLink.href = "#"; // Prevent default link behavior
    closeLink.innerHTML = "&times;"; // Unicode for "X"

    // Attach the removeGrid function to the "X" link
    closeLink.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent default link behavior
      removeGrid(id); // Pass the unique ID to the removeGrid function
    });

    // Append the close link to the grid item
    gridItem.appendChild(closeLink);

    // Append the panel body to the grid item
    gridItem.appendChild(panelBody);

    // Append the grid item to the outer container
    outerContainer.appendChild(gridItem);

    // Step 10: Insert the new grid item before the "+" button
    var addButtonGridItem = document.querySelector(
      ".dashboard-view-grid-base .add-visualization-container",
    );
    if (addButtonGridItem && addButtonGridItem.parentNode) {
      addButtonGridItem.parentNode.insertBefore(
        outerContainer,
        addButtonGridItem,
      );
    }

    // Step 11: Reset form and hide modal
    document.getElementById("visualForm").reset();
    $("#visualModal").modal("hide");
  });
});
