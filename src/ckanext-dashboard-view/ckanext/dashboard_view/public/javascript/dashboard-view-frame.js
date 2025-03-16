const datastoreURL = "/api/3/action/datastore_search";
const echartsConfig = {
  axisLabel: {
    rotate: 45,
    interval: 0,
    formatter: function (value) {
      return value.length > 10 ? value.slice(0, 10) + "..." : value;
    },
  },
  color: ["#08743f", "#f2c500"],
};

function fetch_all_records(
  resource_id,
  config,
  columnTypes = {},
  current = [],
) {
  const limit = 100;
  const offset = current.length;
  return fetch(
    `${datastoreURL}?resource_id=${resource_id}&fields=${config.xAxis},${config.yAxis}&limit=${limit}&offset=${offset}`,
  )
    .then((response) => response.json())
    .then((data) => {
      const records = data.result.records;
      if (_.isEmpty(columnTypes)) {
        columnTypes = data.result.fields.reduce((acc, field) => {
          acc[field.type] = field.id;
          return acc;
        }, columnTypes);
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

function render_chart(res_id, config, container) {
  const data = fetch_all_records(res_id, config).then((data) => {
    const stringAxis = data.columnTypes["text"];
    const groupedData = _.groupBy(data.result, stringAxis);
    const chartData = Object.keys(groupedData).map((key) => {
      return {
        x: key,
        y: groupedData[key].reduce(
          (acc, record) => acc + record[data.columnTypes["numeric"]],
          0,
        ),
      };
    });
    // create echart
    const myChart = echarts.init(container);
    const option = {
      xAxis: {
        type: "category",
        data: chartData.map((d) => d.x),
        axisLabel: echartsConfig.axisLabel,
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          data: chartData.map((d) => d.y),
          type: config.chartType,
        },
      ],
      color: echartsConfig.color,
    };
    myChart.setOption(option);
  });
}

function render_number(config, container) {
  return;
  // console.log("NUMBER", config, container);
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
