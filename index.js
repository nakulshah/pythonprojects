new gridjs.Grid({
  columns: ["date", "station_name", "day_type", "rides"],
  server: {
    url: 'http://127.0.0.1:5000/ctalrides',
    then: data => data
  }
}).render(document.getElementById("wrapper"));