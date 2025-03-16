function render_chart(config, container) {
  // give height to container
  console.log("CHART", config, container);
}

function render_number(config, container) {
  console.log("NUMBER", config, container);
}

document.addEventListener("DOMContentLoaded", function () {
  // data-resource-id
  const resource_id = window.resource_id;
  document.querySelectorAll(".viz-item").forEach(function (el) {
    // get data-viz-type from el
    const config = JSON.parse(el.getAttribute("data-config"));
    const container = document.getElementById(config.id);
    if (config.viz_type === "chart") {
      render_chart(config, container);
    } else {
      render_number(config, container);
    }
  });
});
