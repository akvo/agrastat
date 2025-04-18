function hideLoading(container) {
  const loader = container.querySelector(".viz-loading");
  // if (loader) loader.style.display = "none";
}

const datastoreURL = "/api/3/action/datastore_search";
const echartsConfig = {
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true,
  },
  axisLabel: {
    interval: 0,
    formatter: function (value) {
      return value.length > 10 ? value.slice(0, 10) + "..." : value;
    },
  },
  axisTick: {
    alignWithLabel: true,
  },
  color: ["#08743f", "#f2c500"],
};

function fetch_aggregated_data(resource_id, config) {
  const { numberColumn, distictColumn, numberType, groupBy } = config;

  // Validate required parameters
  if (!resource_id || !numberType) {
    if (numberType === "count" && !distictColumn) {
      throw new Error(
        "Missing required parameters: resource_id, numberColumn, distictColumn, or numberType.",
      );
    } else if (numberType !== "count" && !numberColumn) {
      throw new Error(
        "Missing required parameters: resource_id, numberColumn, distictColumn, or numberType.",
      );
    }
  }

  // Map numberType to SQL aggregate functions
  const sqlFunctions = {
    total: `SUM("${numberColumn}") AS total`,
    avg: `AVG("${numberColumn}") AS average`,
    count: `COUNT(DISTINCT "${distictColumn}") AS count`,
    min: `MIN("${numberColumn}") AS minimum`,
    max: `MAX("${numberColumn}") AS maximum`,
  };

  // Ensure the numberType is valid
  if (!sqlFunctions[numberType]) {
    throw new Error(
      `Invalid numberType: ${numberType}. Valid options are 'total', 'avg', 'count', 'min', 'max'.`,
    );
  }

  // Construct the base SQL query
  let sqlQuery = `SELECT ${sqlFunctions[numberType]}`;

  // Add GROUP BY clause if groupBy is provided
  if (groupBy) {
    sqlQuery += `, "${groupBy}" FROM "${resource_id}" GROUP BY "${groupBy}"`;
  } else {
    sqlQuery += ` FROM "${resource_id}"`;
  }

  // Send the request to the CKAN API
  return fetch(`${datastoreURL}_sql`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sql: sqlQuery }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((result) => {
      // Handle errors in the CKAN API response
      if (!result.success) {
        throw new Error(`CKAN API error: ${result.error.message}`);
      }
      return result.result.records;
    })
    .catch((error) => {
      console.error("Error fetching aggregated data:", error);
    });
}

function fetch_all_records(
  resource_id,
  config,
  columnTypes = [],
  current = [],
) {
  const limit = 100;
  const offset = current.length;
  let url = `${datastoreURL}?resource_id=${resource_id}&limit=${limit}&offset=${offset}`;
  url += `&fields=${config.xAxis},${config.yAxis}`;
  return fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const records = data.result.records;
      if (_.isEmpty(columnTypes)) {
        columnTypes = data.result.fields;
      }
      if (records.length === 0) {
        return {
          columnTypes,
          result: current,
        };
      }
      return fetch_all_records(
        resource_id,
        config,
        columnTypes,
        current.concat(records),
      );
    });
}

function toFloatForECharts(value) {
  if (value === "") {
    return null;
  }
  // Step 1: Normalize the input by removing commas
  const normalizedValue = _.isString(value) ? value.replace(/,/g, "") : value;

  // Step 2: Parse the value as a float
  const parsedValue = parseFloat(normalizedValue);

  // Step 3: Validate the result
  if (!isNaN(parsedValue) && isFinite(parsedValue)) {
    return parsedValue; // Return the valid float
  }
  return null;
}

function sanitize_data(data, stringAxis, numericAxis) {
  return data.map((record) => {
    // strip out any extra spaces
    const label = record[stringAxis].trim();
    const value = toFloatForECharts(record[numericAxis]);
    return {
      key: label,
      value: value,
    };
  });
}

function options_barline(data, config) {
  const chartType = config.chartType !== "area" ? config.chartType : "line";
  const stringAxis = data.columnTypes.find((field) => field.type === "text").id;
  const numericAxis = data.columnTypes.find(
    (field) => field.id !== stringAxis,
  ).id;
  const sanitizedData = sanitize_data(data.result, stringAxis, numericAxis);
  const groupedData = _.groupBy(data.result, stringAxis);
  const chartData = Object.keys(groupedData).map((key) => {
    return {
      key,
      value: _.sumBy(groupedData[key], numericAxis),
    };
  });
  // create echart
  const options = {
    grid: echartsConfig.grid,
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
    },
    color: echartsConfig.color,
  };
  if (stringAxis === config.xAxis) {
    options.xAxis = {
      name: config.xAxis,
      type: "category",
      data: chartData.map((record) => record.key),
      axisLabel: {
        rotate: 45,
        ...echartsConfig.axisLabel,
      },
      axisTick: echartsConfig.axisTick,
    };
    options.yAxis = {
      name: config.yAxis,
      type: "value",
    };
    options.series = [
      {
        name: config.yAxis,
        type: chartType,
        data: chartData.map((record) => record.value),
        areaStyle: config.chartType === "area" ? {} : null,
      },
    ];
  } else {
    options.yAxis = {
      name: config.yAxis,
      type: "category",
      data: chartData.map((record) => record.key),
      axisLabel: echartsConfig.axisLabel,
      axisTick: echartsConfig.axisTick,
    };
    options.xAxis = {
      name: config.xAxis,
      type: "value",
    };
    options.series = [
      {
        name: config.xAxis,
        type: chartType,
        data: chartData.map((record) => record.value),
        areaStyle: config.chartType === "area" ? {} : null,
      },
    ];
  }
  return options;
}

function options_scatter(data, config) {
  const sanitizedData = data.result.map((record) => {
    return [
      toFloatForECharts(record[config.xAxis]),
      toFloatForECharts(record[config.yAxis]),
    ];
  });
  const options = {
    xAxis: {
      name: config.xAxis,
      type: "value",
    },
    yAxis: {
      name: config.yAxis,
      type: "value",
    },
    emphasis: {
      label: {
        show: true,
        formatter: function (param) {
          const html = [];
          html.push(config.xAxis + ": " + param.data[0]);
          html.push(config.yAxis + ": " + param.data[1]);
          return html.join("\n");
        },
        position: "top",
      },
    },
    series: [
      {
        data: sanitizedData,
        type: "scatter",
      },
    ],
  };
  return options;
}

function render_chart(res_id, config, container) {
  const data = fetch_all_records(res_id, config).then((data) => {
    const myChart = echarts.init(container);
    if (
      config.chartType === "bar" ||
      config.chartType === "line" ||
      config.chartType === "area"
    ) {
      hideLoading(container);
      myChart.setOption(options_barline(data, config));
    } else if (config.chartType === "scatter") {
      hideLoading(container);
      myChart.setOption(options_scatter(data, config));
    }
  });
}

function render_number(res_id, config, container) {
  fetch_aggregated_data(res_id, config).then((data) => {
    const res = data[0];
    if (config.numberType === "total") {
      countUp(config.id, res.total);
    } else if (config.numberType === "avg") {
      countUp(config.id, parseFloat(res.average).toFixed(2));
    } else if (config.numberType === "count") {
      countUp(config.id, res.count);
    } else if (config.numberType === "max") {
      countUp(config.id, res.maximum);
    } else if (config.numberType === "min") {
      countUp(config.id, res.minimum);
    }
    hideLoading(container);
  });
}

function render_pie(res_id, config, container) {
  const queryConfig = {
    numberColumn: config.pieValue,
    numberType: "total",
    groupBy: config.pieGroup,
  };
  fetch_aggregated_data(res_id, queryConfig).then((data) => {
    const chartData = data.map((record) => {
      return {
        name: record[config.pieGroup],
        value: record.total,
      };
    });
    const myChart = echarts.init(container);
    hideLoading(container);
    myChart.setOption({
      tooltip: {
        trigger: "item",
        formatter: "{a} <br/>{b} : {c} ({d}%)",
      },
      series: [
        {
          name: config.pieGroup,
          type: "pie",
          data: chartData,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
          },
        },
      ],
    });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  // data-resource-id
  const resource_id = window.resource_id;
  document.querySelectorAll(".viz-item").forEach(function (el) {
    // get data-viz-type from el
    const config = JSON.parse(el.getAttribute("data-config"));
    const container = document.getElementById(config.id);
    if (config.visualizationType === "chart") {
      if (config.chartType === "pie") {
        render_pie(resource_id, config, container);
      } else {
        render_chart(resource_id, config, container);
      }
    } else {
      render_number(resource_id, config, container);
    }
  });
});
