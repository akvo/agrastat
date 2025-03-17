const maxVisualizations = 9;
let editModeId = null;
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
  return existingConfigs;
}

function toggleAddButton(currentExistingConfigs = null) {
  const existingConfigs = currentExistingConfigs || getExistingConfigs();
  const addButton = document.querySelector(".add-visualization-container");
  if (addButton) {
    addButton.classList.toggle(
      "hidden",
      existingConfigs.length >= maxVisualizations,
    );
  }
}

function updateGrid(configs) {
  // Clear the grid
  const gridBase = document.querySelector(".dashboard-view-grid-base");
  gridBase.innerHTML = "";

  // Rebuild the grid
  configs.forEach((config) => {
    const outerContainer = document.createElement("div");
    outerContainer.classList.add(config.gridSize);
    outerContainer.setAttribute("id", `viz_grid_${config.id}`);

    const gridItem = document.createElement("div");
    gridItem.classList.add(
      "grid-item",
      "panel",
      "panel-default",
      "text-center",
      "visualization-grid-item",
    );

    const panelBody = document.createElement("div");
    panelBody.classList.add("panel-body");

    let icon = "fa fa-info-circle";
    if (config.visualizationType === "chart") {
      icon = `fa fa-${config.chartType}-chart`;
      if (config.chartType === "scatter") {
        icon = "fa fa-dot-circle-o";
      }
    }
    let content = `<strong><i class="${icon}"></i> ${config.title}</strong><br>`;
    if (config.visualizationType === "chart") {
      if (config.chartType === "pie") {
        content += `<small>Value: ${config.pieValue}</small><br>
                <small>Group: ${config.pieGroup}</small><br>`;
      } else {
        content += `<small>Type: ${config.chartType}</small><br>
                  <small>X-Axis: ${config.xAxis}</small><br>
                  <small>Y-Axis: ${config.yAxis}</small><br>`;
      }
    } else if (config.visualizationType === "number") {
      content += `<small>Data: ${config.numberColumn}</small><br>
                <small>Value: ${config.numberType}</small><br>`;
    }

    panelBody.innerHTML = content;

    const closeLink = document.createElement("a");
    closeLink.classList.add("remove-grid");
    closeLink.href = "#";
    closeLink.innerHTML = "<i class='fa fa-times'></i>";
    closeLink.addEventListener("click", function (event) {
      event.preventDefault();
      removeGrid(config.id);
    });

    const editLink = document.createElement("a");
    editLink.classList.add("edit-grid");
    editLink.href = "#";
    editLink.innerHTML = "<i class='fa fa-pencil'></i>";
    editLink.addEventListener("click", function (event) {
      event.preventDefault();
      editGrid(config.id);
    });

    gridItem.appendChild(closeLink);
    gridItem.appendChild(editLink);
    gridItem.appendChild(panelBody);
    outerContainer.appendChild(gridItem);
    gridBase.appendChild(outerContainer);
  });

  // Add the "+" button back to the grid
  if (configs.length < maxVisualizations) {
    const addButton = document.querySelector(".add-visualization-container");
    gridBase.appendChild(addButton);
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

function editGrid(id) {
  // Step 1: Find the configuration with the matching ID
  const existingConfigs = getExistingConfigs();
  const configToEdit = existingConfigs.find((config) => config.id === id);

  if (!configToEdit) {
    console.error("Visualization not found for editing:", id);
    return;
  }

  // Set the edit mode ID
  editModeId = id;

  // Step 2: Populate the form fields with the configuration data
  document.getElementById("gridSize").value = configToEdit.gridSize;
  document.getElementById("visualTitle").value = configToEdit.title;
  document.getElementById("visualType").value = configToEdit.visualizationType;

  // Step 3: Toggle the form fields based on the visualization type
  resetFormFields();

  if (configToEdit.visualizationType === "chart") {
    document.getElementById("chartType").value = configToEdit.chartType;
    if (configToEdit.chartType === "pie") {
      document.getElementById("pieValue").value = configToEdit.pieValue;
      document.getElementById("pieGroup").value = configToEdit.pieGroup;
    } else {
      document.getElementById("xAxis").value = configToEdit.xAxis;
      document.getElementById("yAxis").value = configToEdit.yAxis;
    }
  } else if (configToEdit.visualizationType === "number") {
    document.getElementById("numberType").value = configToEdit.numberType;
    document.getElementById("numberColumn").value = configToEdit.numberColumn;
  }

  // Step 4: Show the modal
  $("#visualModal").modal("show");
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
    // Gather form data for the visualization
    const gridSize = document.getElementById("gridSize").value;
    const title = document.getElementById("visualTitle").value || "Untitled";
    const visualType = document.getElementById("visualType").value;

    // Create the configuration object
    let newConfig = {
      id: editModeId || Math.random().toString(36).substr(2, 9), // Use existing ID or generate a new one
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

    // Collect all existing configurations
    let existingConfigs = getExistingConfigs();

    if (editModeId) {
      // Update the existing visualization
      const index = existingConfigs.findIndex(
        (config) => config.id === editModeId,
      );
      if (index !== -1) {
        existingConfigs[index] = newConfig; // Replace the old configuration
      } else {
        console.error("Visualization not found for editing:", editModeId);
      }

      // Reset edit mode
      editModeId = null;
    } else {
      // Add the new visualization
      existingConfigs.push(newConfig);
    }

    // Serialize the updated list and update the hidden input field
    document.getElementById("columns-input").value =
      JSON.stringify(existingConfigs);

    // Update the grid in the DOM
    updateGrid(existingConfigs);

    // Reset the form and hide the modal
    resetFormFields();
    $("#visualModal").modal("hide");
  });
});
