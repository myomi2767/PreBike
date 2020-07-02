// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ccc = document.getElementById("myAreaChart");
var myLineChart = new Chart(ccc, {
  type: 'line',
  data: {
    labels: ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23" ],
    // datasets: [{
    //   label: "Sessions",
    //   lineTension: 0.3,
    //   backgroundColor: "rgba(2,117,216,0.2)",
    //   borderColor: "rgba(2,117,216,1)",
    //   pointRadius: 5,
    //   pointBackgroundColor: "rgba(2,117,216,1)",
    //   pointBorderColor: "rgba(255,255,255,0.8)",
    //   pointHoverRadius: 5,
    //   pointHoverBackgroundColor: "rgba(2,117,216,1)",
    //   pointHitRadius: 50,
    //   pointBorderWidth: 2,
    //   data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451],
    // },{
    // rgba(2,117,216,1)
    datasets: [{
      label: "Sessions",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984],
    },{
      label: "Sessions",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(255, 99, 132, 1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(255, 99, 132, 1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(255, 99, 132, 1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 10,
          maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});

//select 의 id를 찾아서 정보를 가져온다.
const selectedgu = document.querySelector('#chart_rent_Gu')
//가져온 정보를 addeventListener를 통해 출력해준다.
selectedgu.addEventListener('change', function(event) {
    console.log(event.target.value)
    temp = event.target.value
    axios.get(`/board/search/`, {
        "params": {
            "rentGu" : temp
        }
    })
    .then(function(response) {
        const selecteddong = document.querySelector('#chart_rent_Dong')
        selecteddong.innerHTML=""
        //기본 옵션 태그 생성
        const basicOptionTag = document.createElement('option')
        basicOptionTag.innerText = '-----동 선택-----'
        //동 옵션 태그 리스트에 추가해준다.
        selecteddong.append(basicOptionTag)
        response.data.rentdong.forEach(data => {
            const optionTag = document.createElement('option')
            optionTag.innerText = data          
            selecteddong.append(optionTag)
        })        
        //selecteddong.innerText = response.data
    })
    .catch(function(error) {
        console.log(error);
    });
})
const selectedDong = document.querySelector('#chart_rent_Dong')
selectedDong.addEventListener('change', function(event1) {
    tempdong = event1.target.value
    const selectedGu = document.querySelector('#chart_rent_Gu').value
    axios.get(`/board/search/`, {
        "params": {
            "rentGu" : selectedGu,
            "rentDong" : tempdong,
        }
    })
    .then(function(response) {
        const selStation = document.querySelectorAll('#chart_station_Name tr')
        selStation.forEach(data => {
            data.remove()
        })
        response.data.station.forEach(data => {    
            const selstationname = document.querySelector('#chart_station_Name')
            const trTableTag = document.createElement('tr')
            selstationname.append(trTableTag)
            const tableTag = document.createElement('td')
            tableTag.innerText = data.stationname
            tableTag.id = data.stationnum
            trTableTag.append(tableTag)
        })
    })
    .then(response => {
      const selStations = document.querySelectorAll('#chart_station_Name tr td')
      selStations.forEach(selStationName =>{
          selStationName.addEventListener('click', function(event) {
              tempname = event.target.id
              axios.get(`/board/areacharts/`, {
                  "params": {
                      "chart_stationNum" : tempname
                  }
              })
              .then(function(response) {
                  console.log('********station*********')
                  console.log(response)
                  console.log('*********datasets*********')
                  console.log(myLineChart.data.datasets)
                  myLineChart.data.datasets[0].data = response.data.hour_rentplacelist
                  myLineChart.data.datasets[1].data = response.data.hour_recedeplacelist
                  myLineChart.update()        
              })
              .catch(function(error) {
                console.log(error);
              });
          })
      })
  })
  .catch(function(error) {
      console.log(error);
  });

})




