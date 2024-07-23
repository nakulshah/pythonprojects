new gridjs.Grid({
  columns: ["date", "day_type", "rides", "station_id", "station_name"],
  data: [
 {
    "date": "01/01/2024",
    "day_type": "U",
    "rides": 299,
    "station_id": 40010,
    "station_name": "Austin-Forest Park"
  },
  {
    "date": "01/02/2024",
    "day_type": "W",
    "rides": 451,
    "station_id": 40010,
    "station_name": "Austin-Forest Park"
  }
  ]
}).render(document.getElementById("wrapper"));