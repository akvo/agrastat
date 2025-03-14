// dashboard-view.js

document.addEventListener("DOMContentLoaded", function () {
  // Toggle visibility of options based on visualization type
  document.getElementById("visualType").addEventListener("change", function () {
    var type = this.value;
    document
      .getElementById("numberOptions")
      .classList.toggle("hidden", type !== "number");
    document
      .getElementById("numberValue")
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

    // Create the configuration object for the new visualization
    var newConfig = {
      grid_size: gridSize,
      title: title,
      visualization_type: visualType,
    };

    if (visualType === "chart") {
      newConfig.chart_type = document.getElementById("chartType").value;
      newConfig.x_axis =
        document.getElementById("xAxis").value || "X-Axis Placeholder";
      newConfig.y_axis =
        document.getElementById("yAxis").value || "Y-Axis Placeholder";
    } else if (visualType === "number") {
      newConfig.number_type =
        document.getElementById("numberType").value || "Average";
      newConfig.number_column = document.getElementById("numberColumn").value;
    }

    // Step 2: Collect all existing configurations
    var existingConfigs = [];
    try {
      // Parse the current value of the hidden input field
      existingConfigs = JSON.parse(
        document.getElementById("columns-input").value,
      );
    } catch (e) {
      // If parsing fails (e.g., empty or invalid JSON), start with an empty array
      existingConfigs = [];
    }

    // Step 3: Add the new configuration to the list
    existingConfigs.push(newConfig);

    // Step 4: Serialize the updated list and update the hidden input field
    document.getElementById("columns-input").value =
      JSON.stringify(existingConfigs);

    // Step 5: Create a new grid item in the UI
    var content = `<strong>${title}</strong>`;
    if (visualType === "chart") {
      content += `<br><small>Type: ${newConfig.chart_type}</small><br>
                <small>X-Axis: ${newConfig.x_axis}</small><br>
                <small>Y-Axis: ${newConfig.y_axis}</small>`;
    } else if (visualType === "number") {
      content += `<br><small>Type: Number (${newConfig.number_type})</small><br>
                <small>Value: ${newConfig.number_column}</small>`;
    }

    var newGridItem = document.createElement("div");
    newGridItem.classList.add(gridSize);
    newGridItem.setAttribute("data-config", JSON.stringify(newConfig)); // Store config as a data attribute
    newGridItem.innerHTML = `
    <div class="grid-item panel panel-default text-center visualization-grid-item">
      <div class="panel-body">${content}</div>
    </div>
  `;

    // Find the "+" button grid item
    var addButtonGridItem = document.querySelector(
      ".dashboard-view-grid-base .add-visualization-container",
    );

    // Insert the new visual before the add button
    addButtonGridItem.parentNode.insertBefore(newGridItem, addButtonGridItem);

    // Reset form and hide modal
    $("#visualModal").modal("hide");
  });
});
