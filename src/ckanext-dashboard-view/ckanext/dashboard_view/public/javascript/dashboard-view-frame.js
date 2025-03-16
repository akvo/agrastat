const datastoreURL = "/api/3/action/datastore_search";
const echartsConfig = {
  axisLabel: {
    interval: 0,
    formatter: function (value) {
      return value.length > 10 ? value.slice(0, 10) + "..." : value;
    },
  },
  color: ["#08743f", "#f2c500"],
  axisTick: {
    alignWithLabel: true,
  },
};

function fetch_all_records(
  resource_id,
  config,
  columnTypes = [],
  current = [],
) {
  const limit = 100;
  const offset = current.length;
  let url = `${datastoreURL}?resource_id=${resource_id}&limit=${limit}&offset=${offset}`;
  if (config.visualizationType === "number") {
    url += `&fields=${config.numberColumn}`;
  } else {
    url += `&fields=${config.xAxis},${config.yAxis}`;
  }
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
      containLabel: true,
    },
    color: echartsConfig.color,
  };
  if (stringAxis === config.xAxis) {
    options.xAxis = {
      type: "category",
      data: chartData.map((record) => record.key),
      axisLabel: {
        rotate: 45,
        ...echartsConfig.axisLabel,
      },
    };
    options.yAxis = {
      type: "value",
    };
    options.series = [
      {
        name: config.yAxis,
        type: config.chartType,
        data: chartData.map((record) => record.value),
      },
    ];
  } else {
    options.yAxis = {
      type: "category",
      data: chartData.map((record) => record.key),
      axisLabel: echartsConfig.axisLabel,
    };
    options.xAxis = {
      type: "value",
    };
    options.series = [
      {
        name: config.xAxis,
        type: config.chartType,
        data: chartData.map((record) => record.value),
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
    if (config.chartType === "bar" || config.chartType === "line") {
      myChart.setOption(options_barline(data, config));
    } else if (config.chartType === "scatter") {
      myChart.setOption(options_scatter(data, config));
    }
  });
}

function render_number(res_id, config, container) {
  const data = fetch_all_records(res_id, config).then((data) => {
    if (config.numberType === "total") {
      const total = _.sumBy(data.result, config.numberColumn);
      countUp(config.id, total);
    } else if (config.numberType === "avg") {
      const avg = _.meanBy(data.result, config.numberColumn);
      countUp(config.id, avg.toFixed(2));
    } else if (config.numberType === "count") {
      countUp(config.id, data.result.length).start();
    } else if (config.numberType === "max") {
      const max = _.maxBy(data.result, config.numberColumn)[
        config.numberColumn
      ];
      countUp(config.id, max);
    } else if (config.numberType === "min") {
      const min = _.minBy(data.result, config.numberColumn)[
        config.numberColumn
      ];
      countUp(config.id, min);
    }
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
      render_chart(resource_id, config, container);
    } else {
      render_number(resource_id, config, container);
    }
  });
});
