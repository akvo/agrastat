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

  // Save visualization and add it to the grid
  document.getElementById("saveVisual").addEventListener("click", function () {
    var gridSize = document.getElementById("gridSize").value;
    var title = document.getElementById("visualTitle").value || "Untitled";
    var visualType = document.getElementById("visualType").value;
    var content = `<strong>${title}</strong>`;

    if (visualType === "chart") {
      var chartType = document.getElementById("chartType").value;
      var xAxis =
        document.getElementById("xAxis").value || "X-Axis Placeholder";
      var yAxis =
        document.getElementById("yAxis").value || "Y-Axis Placeholder";

      content += `<br><small>Type: ${chartType}</small><br>
                  <small>X-Axis: ${xAxis}</small><br>
                  <small>Y-Axis: ${yAxis}</small>`;
    } else if (visualType === "number") {
      var numberType = document.getElementById("numberType").value || "Average";
      content += `<br><small>Type: Number (${numberType})</small>`;
      var numberColumn = document.getElementById("numberColumn").value;
      content += `<br><small>Value: ${numberColumn}</small>`;
    }

    // Create a new grid item
    var newGridItem = document.createElement("div");
    newGridItem.classList.add(gridSize);
    newGridItem.innerHTML = `<div class="grid-item panel panel-default text-center visualization-grid-item"><div class="panel-body">${content}</div></div>`;

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
