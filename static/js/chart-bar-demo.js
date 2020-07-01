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
  scrollY: 330
});

//select 의 id를 찾아서 정보를 가져온다.
const selectedgu = document.querySelector('#rent_Gu')
console.log('***************************')
console.log(selectedgu)
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
        console.log('******$$$$$$*******')
        console.log(response);
        const selecteddong = document.querySelector('#rent_Dong')
        selecteddong.innerHTML=""
        const basicOptionTag = document.createElement('option')
        basicOptionTag.innerText = '-----동 선택-----'
        selecteddong.append(basicOptionTag)
        response.data.rentdong.forEach(data => {
            const optionTag = document.createElement('option')
            optionTag.innerText = data
            
            selecteddong.append(optionTag)
        })
        //console.log('*********########*********')
        //console.log(response.data)
        //selecteddong.innerText = response.data
    })
    .catch(function(error) {
        console.log(error);
    });
})
const selectedDong = document.querySelector('#rent_Dong')
console.log('*********@@@@@@@@*******')
console.log(selectedDong)
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
        console.log('******%%%%%%******')
        console.log(response);
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

                axios.get(`/board/charts/`, {
                    "params": {
                        "stationNum" : tempname
                    }
                })
            })
        })
    })
    .catch(function(error) {
        console.log(error);
    });
})



// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    //labels: ["January", "February", "March", "April", "May", "June"],
    labels: ["1st", "2nd", "3rd", "4th"],
    datasets: [{
      label: "Revenue",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",


      //data: [4215, 5312, 6251, 7841, 9821, 14984],
      data: [6251, 7841, 9821, 14984],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          //unit: 'month'
          unit: 'week'
        },
        gridLines: {
          display: false,
          color:"black"
        },
        ticks: {
          maxTicksLimit: 12
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 15000,
          maxTicksLimit: 5
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
