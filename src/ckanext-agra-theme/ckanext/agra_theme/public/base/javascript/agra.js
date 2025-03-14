// if landing page .masthead backgroun should be transparent

function createBarOption(data, override = {}) {
  data = data.sort((a, b) => a.value - b.value);
  return {
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      top: "3%",
      containLabel: true,
    },
    xAxis: {
      type: "value",
      show: false, // Hide the x-axis
    },
    yAxis: {
      type: "category",
      data: data.map((x) => ({
        value: x.name,
        textStyle: {
          color: "#08743f",
          fontWeight: "bold",
          fontFamily: "Poppins",
        },
      })),
      axisLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
    },
    series: [
      {
        name: "Datasets",
        type: "bar",
        data: data.map((x) => x.value),
        label: {
          show: true,
          position: "insideLeft",
          formatter: "{c} Datasets",
          color: "#fff",
          offset: [10, 0],
          fontWeight: "bold",
          fontFamily: "Poppins",
        },
        itemStyle: {
          // Optional: Adjust bar colors for better label visibility
          borderRadius: [0, 5, 5, 0],
          color: "#08743f",
        },
      },
    ],
    ...override,
  };
}
function createRadarOption(data) {
  const max = data.reduce((acc, curr) => Math.max(acc, curr.value), 0);
  const option = {
    radar: {
      // shape: 'circle',
      indicator: data.map((x) => ({
        name: `${x.name}[${x.value}]`,
        max: max,
      })),
      axisName: {
        color: "#08743f",
        fontWeight: "bold",
        fontFamily: "Poppins",
        formatter: (value) => {
          // break string into words and new line after 10 characters
          const words = value.split(" ");
          const lines = [];
          let line = "";
          for (let i = 0; i < words.length; i++) {
            if (line.length + words[i].length > 10) {
              lines.push(line);
              line = words[i];
            } else {
              line += " " + words[i];
            }
          }
          lines.push(line);
          return lines.join("\n");
        },
      },
    },
    series: [
      {
        name: "Budget vs spending",
        type: "radar",
        data: [
          {
            value: data.map((x) => x.value),
            name: "Dataset Count",
          },
        ],
      },
    ],
    color: ["#08743f"],
  };
  return option;
}

function renderChart(orgName = null) {
  const header = document.querySelector(".masthead");
  const navLinks = document.querySelectorAll(".masthead .nav > li > a");
  header.style.backgroundColor = "rgba(114,191,68,.7)";
  navLinks.forEach((link) => {
    link.style.color = "white";
  });
  const extraEndpoint = orgName ? `organization=${orgName}` : "";
  // fetch stat data from the api api/2/statistic/countries
  fetch("/api/2/statistic/countries?limit=10&" + extraEndpoint)
    .then((response) => response.json())
    .then((data) => {
      /* example of response {name:'uganda', value: 1}  */
      // create echarts instance in div id = chart-bar-country
      const chart = echarts.init(document.getElementById("chart-countries"));
      chart.setOption(createBarOption(data));
    });

  if (document.getElementById("chart-business-lines")) {
    fetch("/api/2/statistic/business_lines" + `?${extraEndpoint}`)
      .then((response) => response.json())
      .then((data) => {
        const chart = echarts.init(
          document.getElementById("chart-business-lines"),
        );
        chart.setOption(createRadarOption(data));
      });
  }

  // if impact areas div is available
  if (document.getElementById("chart-impact-areas")) {
    fetch("/api/2/statistic/impact_areas" + `?${extraEndpoint}`)
      .then((response) => response.json())
      .then((data) => {
        const chart = echarts.init(
          document.getElementById("chart-impact-areas"),
        );
        chart.setOption(createRadarOption(data));
      });
  }

  if (document.getElementById("chart-value-chains")) {
    fetch("/api/2/statistic/value_chains" + `?${extraEndpoint}`)
      .then((response) => response.json())
      .then((data) => {
        const chart = echarts.init(
          document.getElementById("chart-value-chains"),
        );
        chart.setOption(createRadarOption(data));
      });
  }
}

if (window.location.pathname === "/") {
  renderChart();
} else {
  window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar-static-top");
    if (window.scrollY > 0) {
      navbar.classList.add("sticky");
    } else {
      navbar.classList.remove("sticky");
    }
  });
}

function getOrganizationNameFromURL() {
  const path = window.location.pathname;
  const match = path.match(/\/organization\/stats\/([^\/]+)/);
  if (match) {
    renderChart(match[1]);
  }
}

if (window.location.pathname.includes("/organization/stats/")) {
  const orgName = getOrganizationNameFromURL();
  console.log("Organization Name:", orgName);
}

if (window.location.pathname === "/contact") {
  const form = document.querySelector("form");
  const title = document.querySelector("#field-title");
  const subject = document.querySelector("#field-subject");
  const bussinessLine = document.querySelector("#field-business-line");

  subject.value = bussinessLine.value;

  bussinessLine.addEventListener("change", (e) => {
    const titleValue = title.value;
    const value = e.target.value;
    if (titleValue === "") {
      subject.value = value;
    } else {
      subject.value = `${titleValue} - ${value}`;
    }
  });

  title.addEventListener("change", (e) => {
    const value = e.target.value;
    const businessLineValue = bussinessLine.value;
    subject.value = `${value} - ${businessLineValue}`;
  });
}

// if user is on the resource page and the file uploaded is a tabular data
// show an alert to the user to proceed to the converter page
if (
  window.location.pathname.includes("/resource/") ||
  window.location.pathname.includes("/resource/")
) {
  const fileInput = document.querySelector("#field-resource-upload");
  const alertDiv = document.querySelector("#info-alert");
  if (fileInput) {
    fileInput.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (
        file.name.endsWith(".xls") ||
        file.name.endsWith(".xlsx") ||
        file.name.endsWith(".dta")
      ) {
        alertDiv.style.display = "block";
        alertDiv.innerHTML = `You are uploading a tabular data that does not support preview. Please proceed to <a target="_blank" href="/convert"><b>converter page</b></a> to convert the file`;
      }
    });
  }
}
