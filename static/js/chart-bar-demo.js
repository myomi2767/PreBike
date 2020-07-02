// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// datapass from index.html

$("#indexTable").DataTable({
  // 표시 건수기능 숨기기
  lengthChange: false,
  // 검색 기능 숨기기
  searching: false,
  // 정렬 기능 숨기기
  ordering: false,
  // 정보 표시 숨기기
  info: false,
  // 페이징 기능 숨기기
  paging: false,
  scrollY: 320
});

// Bar Chart Example
const aaa = document.getElementById("myBarChart");
// Chart.defaults.global.defaultFontColor = 'blue';
Chart.defaults.global.defaultFontFamily = 'Arial';
const myBarChart = new Chart(aaa, {
  type: 'bar',
  data: {
    //labels: ["January", "February", "March", "April", "May", "June"],
    labels: ["1st week", "2nd week", "3rd week", "4th week"],
    datasets: [{
      label: "대여대수",
      backgroundColor: "rgba(255, 99, 132, 1)",
      borderColor: "rgba(255 99, 132, 1)",
      fill: true,
      data: [],
    },{
      label: "반납대수",
      backgroundColor: "rgba(75, 192, 192, 1)",
      bordercolor: "rgba(75, 192, 192, 1)",
      fill: true,
      data: [],
    }]
  },
  options: {
    maintainAspectRatio: false,
    title: {
      display: true,
      text: '주별 대여와 반납대수',
      fontColor : '#000000',
      fontSize : 18,
    },
    scales: {
      xAxes: [{
        time: {
          //unit: 'month'
          unit: 'week'
        },
        gridLines: {
          display: true,
          color:"black"
        },
        ticks: {
          maxTicksLimit: 12
        },
        scaleLabel: {
          display: true,
          labelString: '주',
        }
      }],
      yAxes: [{
        ticks: {
          beginAtZero: true,
          min: 0,
          max: 1100,
          maxTicksLimit: 20
        },
        gridLines: {
          display: true
        },
        scaleLabel: {
          display: true,
          labelString: '대여/반납대수',
        }
      }],
    },
    legend: {
      display: true,
      labels: {
        fontColor: 'black'
      }
    }
  }
});

//select 의 id를 찾아서 정보를 가져온다.
const selectedgu = document.querySelector('#rent_Gu')
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
        const selecteddong = document.querySelector('#rent_Dong')
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
const selectedDong = document.querySelector('#rent_Dong')
selectedDong.addEventListener('change', function(event1) {
    tempdong = event1.target.value
    const selectedGu = document.querySelector('#rent_Gu').value
    axios.get(`/board/search/`, {
        "params": {
            "rentGu" : selectedGu,
            "rentDong" : tempdong,
        }
    })
    .then(function(response) {
        const selStation = document.querySelectorAll('.station_Name tr')
        selStation.forEach(data => {
            data.remove()
        })
        response.data.station.forEach(data => {    
            const selstationname = document.querySelector('.station_Name')
            const trTableTag = document.createElement('tr')
            selstationname.append(trTableTag)
            const tableTag = document.createElement('td')
            tableTag.innerText = data.stationname
            tableTag.id = data.stationnum
            trTableTag.append(tableTag)
        })
    })
    .then(response => {
        const selStations = document.querySelectorAll('.station_Name tr td')
        selStations.forEach(selStationName =>{
            selStationName.addEventListener('click', function(event) {
                tempname = event.target.id
                
                const detail = document.querySelector('#detailStationNum')
                detail.value = tempname

                axios.get(`/board/barcharts/`, {
                    "params": {
                        "stationNum" : tempname
                    }
                })
                .then(function(response) {
                    console.log('********station*********')
                    console.log(response)
                    console.log('*********datasets*********')
                    console.log(myBarChart.data.datasets)
                    myBarChart.data.datasets[1].data = response.data.recedeplacelist
                    myBarChart.data.datasets[0].data = response.data.rentplacelist
                    if(Math.max(...response.data.recedeplacelist)>Math.max(...response.data.rentplacelist)){
                      myBarChart.options.scales.yAxes[0].ticks.max = Math.round(Math.max(...response.data.recedeplacelist)*1.1)
                    }else{
                      myBarChart.options.scales.yAxes[0].ticks.max = Math.round(Math.max(...response.data.rentplacelist)*1.1)
                    }
                    myBarChart.options.title.text = response.data.chartStationName
                    myBarChart.update()        
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

