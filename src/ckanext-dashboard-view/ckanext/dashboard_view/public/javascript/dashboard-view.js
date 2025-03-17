const maxVisualizations = 9;
// dashboard-view.js
function getExistingConfigs() {
  let existingConfigs = [];
  try {
    existingConfigs = JSON.parse(
      document.getElementById("columns-input").value,
    );
  } catch (e) {
    console.error("Error parsing existing configurations:", e);
    existingConfigs = [];
  }
  console.log("Existing Configs", existingConfigs);
  return existingConfigs;
}

function toggleAddButton(currentExistingConfigs = null) {
  const existingConfigs = currentExistingConfigs || getExistingConfigs();
  console.log("Existing Configs", existingConfigs.length, maxVisualizations);
  const addButton = document.querySelector(".add-visualization-container");
  if (addButton) {
    addButton.classList.toggle(
      "hidden",
      existingConfigs.length >= maxVisualizations,
    );
  }
}

function removeGrid(id) {
  // Step 1: Remove the configuration from the existingConfigs array
  let existingConfigs = getExistingConfigs();

  // Filter out the configuration with the matching ID
  existingConfigs = existingConfigs.filter((config) => config.id !== id);

  // Update the hidden input field with the updated configurations
  document.getElementById("columns-input").value =
    JSON.stringify(existingConfigs);

  // Step 2: Remove the grid item from the DOM
  const gridItemToRemove = document.querySelector(`#viz_grid_${id}`);
  if (gridItemToRemove) {
    gridItemToRemove.remove();
  }
  toggleAddButton(existingConfigs);
}

function resetFormFields() {
  const currentType = document.getElementById("visualType").value;
  document
    .getElementById("numberOptions")
    .classList.toggle("hidden", currentType !== "number");
  document
    .getElementById("chartOptions")
    .classList.toggle("hidden", currentType !== "chart");
  if (currentType === "chart") {
    const chartType = document.getElementById("chartType").value;
    if (chartType === "pie") {
      document.getElementById("axisData").classList.add("hidden");
      document.getElementById("pieData").classList.remove("hidden");
    } else {
      document.getElementById("axisData").classList.remove("hidden");
      document.getElementById("pieData").classList.add("hidden");
    }
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Check the current value of the select element on page load
  resetFormFields();
  toggleAddButton();
  // Toggle visibility of options based on visualization type
  document.getElementById("visualType").addEventListener("change", function () {
    resetFormFields();
  });
  document.getElementById("chartType").addEventListener("change", function () {
    resetFormFields();
  });

  // Add event listener to the "Save Visualization" button

  document.getElementById("saveVisual").addEventListener("click", function () {
    // Step 1: Gather form data for the new visualization
    const gridSize = document.getElementById("gridSize").value;
    const title = document.getElementById("visualTitle").value || "Untitled";
    const visualType = document.getElementById("visualType").value;

    // Generate a unique ID for the new visualization
    const id = Math.random().toString(36).substr(2, 9);

    // Create the configuration object for the new visualization
    let newConfig = {
      id: id, // Use the generated ID
      gridSize: gridSize,
      title: title,
      visualizationType: visualType,
    };

    if (visualType === "chart") {
      newConfig.chartType = document.getElementById("chartType").value;
      if (newConfig.chartType === "pie") {
        newConfig.pieValue = document.getElementById("pieValue").value;
        newConfig.pieGroup = document.getElementById("pieGroup").value;
      } else {
        newConfig.xAxis = document.getElementById("xAxis").value;
        newConfig.yAxis = document.getElementById("yAxis").value;
      }
    } else if (visualType === "number") {
      newConfig.numberType =
        document.getElementById("numberType").value || "avg";
      newConfig.numberColumn = document.getElementById("numberColumn").value;
    }

    // Step 2: Collect all existing configurations
    let existingConfigs = getExistingConfigs();

    // Step 3: Add the new configuration to the list
    existingConfigs.push(newConfig);

    // Step 4: Serialize the updated list and update the hidden input field
    document.getElementById("columns-input").value =
      JSON.stringify(existingConfigs);

    // Step 5: Create the outer container (col-md-4)
    const outerContainer = document.createElement("div");
    outerContainer.classList.add(gridSize);
    outerContainer.setAttribute("id", `viz_grid_${id}`); // Unique ID for the container

    // Step 6: Create the grid item container
    const gridItem = document.createElement("div");
    gridItem.classList.add(
      "grid-item",
      "panel",
      "panel-default",
      "text-center",
      "visualization-grid-item",
    );

    // Step 7: Create the panel body
    const panelBody = document.createElement("div");
    panelBody.classList.add("panel-body");

    // Step 8: Build the content
    let icon = "fa fa-info-circle";
    if (visualType === "chart") {
      icon = `fa fa-${newConfig.chartType}-chart`;
      if (newConfig.chartType === "scatter") {
        icon = "fa fa-dot-circle-o";
      }
    }
    let content = `<strong><i class="${icon}"></i> ${title}</strong><br>`;
    if (visualType === "chart") {
      const ctype = document.getElementById("chartType").value;
      if (ctype === "pie") {
        content += `<small>Value: ${newConfig.pieValue}</small><br>
                <small>Group: ${newConfig.pieGroup}</small><br>`;
      } else {
        content += `<small>Type: ${newConfig.chartType}</small><br>
                  <small>X-Axis: ${newConfig.xAxis}</small><br>
                  <small>Y-Axis: ${newConfig.yAxis}</small><br>`;
      }
    } else if (visualType === "number") {
      content += `<small>Data: ${newConfig.numberColumn}</small><br>
                <small>Value: ${newConfig.numberType}</small><br>`;
    }

    // Append the content to the panel body
    panelBody.innerHTML = content;

    // Step 9: Add the "X" link for removal
    const closeLink = document.createElement("a");
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
    const addButtonGridItem = document.querySelector(
      ".dashboard-view-grid-base .add-visualization-container",
    );
    if (addButtonGridItem && addButtonGridItem.parentNode) {
      addButtonGridItem.parentNode.insertBefore(
        outerContainer,
        addButtonGridItem,
      );
      toggleAddButton(existingConfigs);
    }

    resetFormFields();
    $("#visualModal").modal("hide");
    const allFields = ["visualTitle"];
    allFields.forEach((field) => {
      document.getElementById(field).value = "";
    });
  });
});
