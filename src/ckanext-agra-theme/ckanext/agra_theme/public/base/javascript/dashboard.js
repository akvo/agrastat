document.addEventListener("DOMContentLoaded", function () {
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
    }

    // Create a new grid item
    var newGridItem = document.createElement("div");
    newGridItem.classList.add(
      gridSize,
      "grid-item",
      "panel",
      "panel-default",
      "text-center",
    );
    newGridItem.innerHTML = `<div class="panel-body">${content}</div>`;

    // Find the "+" button grid item
    var addButtonGridItem = document.querySelector(".grid-container .col-md-4");

    // Insert the new visual before the add button
    addButtonGridItem.parentNode.insertBefore(newGridItem, addButtonGridItem);

    // Reset form and hide modal
    document.getElementById("visualForm").reset();
    document.getElementById("numberOptions").classList.add("hidden");
    document.getElementById("chartOptions").classList.add("hidden");

    $("#visualModal").modal("hide"); // Close modal for Bootstrap 3/4
  });
});
