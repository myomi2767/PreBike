// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var bbb = document.getElementById("myPieChart");
var myPieChart = new Chart(bbb, {
  type: 'pie',
  data: {
    labels: ["Blue", "Red", "Yellow", "Green"],
    datasets: [{
      data: [11410, 22540, 35462, 4054],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745', '#ba577f',
                      '#a97a1d', '#aaba36', '#0cded7', '#e67bed', '#2b47d9',
                      '#736e59', '#fb4a38', '#583d68', '#bb641e', '#0bda33',
                      '#bd6532', '#a2e131', '#2b3156', '#9a2e44', '#8419a6',
                      '#0249c9', '#7321a9', '#71a854', '#24bead', '#fa4417',
                      '#51e804', '#fb6f89', '#214366', '#9ca6a9', '#f70ca2',
                      '#841f48', '#1f86ea', '#065163', '#bd6723', '#ba3b8d',
                      '#27a93a', '#40f6e2', '#b31df9', '#eba176', '#379d6c',
                      '#fcd224', '#bf5592', '#6d10b4', '#06eeec', '#e9b86a'
                      ],
    }],
  },
});

//select 의 id를 찾아서 정보를 가져온다.
const pie_selectedgu = document.querySelector('#piechart_rent_Gu')
//가져온 정보를 addeventListener를 통해 출력해준다.
pie_selectedgu.addEventListener('change', function(event) {
    console.log('&&&&&&&&&&&')
    console.log(event.target.value)
    temp = event.target.value
    axios.get(`/board/piecharts/`, {
        "params": {
            "rentGu" : temp
        }
    })
    .then(function(response) {
        console.log('@@@@@********@@@@@@')
        console.log(response)
        const dongDatasets = []
        const countDatasets = []
        response.data.countedDong.forEach(data => {
          dongDatasets.push(data.rentDong)
          countDatasets.push(data.rent__count)
        })
        myPieChart.data.datasets[0].data = countDatasets
        myPieChart.data.labels = dongDatasets
        myPieChart.update()
    })
})



// .then(function(response) {
//   const selStation = document.querySelectorAll('.station_Name tr')
//   selStation.forEach(data => {
//       data.remove()
//   })
//   response.data.station.forEach(data => {    
//       const selstationname = document.querySelector('.station_Name')
//       const trTableTag = document.createElement('tr')
//       selstationname.append(trTableTag)
//       const tableTag = document.createElement('td')
//       tableTag.innerText = data.stationname
//       tableTag.id = data.stationnum
//       trTableTag.append(tableTag)
//   })
// })