aircraft=[]
  urlstring="https://aircraft-apis-09709e7ae2e9.herokuapp.com/PivotDashData"
  //urlstring="http://127.0.0.1:5000/PivotDashData"
  d3.json(urlstring).then(function(sample_m) {
    var objsample=sample_m
    //console.log(objsample)
    //aircraft=objsample
    objsample.forEach(element=>{
    //console.log(element)
    // })
    //console.log("inside")
  console.log(aircraft)
     aircraft.push(element)
  })
  var pivot = new WebDataRocks({
    container: "#wdr-component",
    toolbar: false,
    "height": 500,
    report: {
        "dataSource": {
            "dataSourceType": "json",
            "data": aircraft
        },
        "slice": {
             "rows": [{
                 "uniqueName": "AIRLINE"
             },
             {
            "uniqueName": "Measures"
            }],
            "columns": [{
                "uniqueName": "month"
            }],
            "measures": [{
                "uniqueName": "profit_loss",
                "aggregation": "sum"
            }]
        }
    },
    reportcomplete: function() {
        pivot.off("reportcomplete");
        createAreaChart();
        createBarChart();
        createPieChart();
    }
});
 

  
  //aircraftData = getJSONData1()
 // console.log(aircraftData)


function createAreaChart() {
    var chart = new FusionCharts({
        type: "area2d",
        renderAt: "fusionchartArea",
        width: "100%",
        height: 500
    });
    pivot.fusioncharts.getData({
    type: chart.chartType(), "slice": {
        "rows": [
            {
                "uniqueName": "[Measures]"
            }
        ],
        "columns": [
            {
                "uniqueName": "month"
            }
        ],
        "measures": [
            {
                "uniqueName": "profit_loss",
                "aggregation": "sum"
            }
        ]
    }
	}, function(data) {
        chart.setJSONData(data);
        chart.setChartAttribute("theme", "fusion");
        chart.setChartAttribute("caption", "Total Profit by Month");
        chart.render();
    });
}

function createBarChart() {
    var chart = new FusionCharts({
        type: "bar2d",
        renderAt: "fusionchartBar",
        width: "100%",
        height: 500
    });
    pivot.fusioncharts.getData({
    type: chart.chartType(), "slice": {
        "rows": [
            {
                "uniqueName": "[Measures]"
            }
        ],
        "columns": [
            {
                "uniqueName": "SIZE"
            }
        ],
        "measures": [
            {
                "uniqueName": "profit_loss",
                "aggregation": "sum"
            }
        ]
    }
	},
	function(data) {
        chart.setJSONData(data);
        chart.setChartAttribute("theme", "fusion");
        chart.setChartAttribute("caption", "Total Revenue for Each Model");
        chart.setChartAttribute("paletteColors", "#bc5cdb, #493999, #8790a8");
        chart.render();
    }

    );
}

function createPieChart() {
    var chart = new FusionCharts({
        type: "pie3d",
        renderAt: "fusionchartPie",
        width: "100%",
        height: 400
    });
    pivot.fusioncharts.getData({
        type: chart.chartType()
        }, function(data) {
        chart.setJSONData(data);
        chart.setChartAttribute("theme", "fusion");
        chart.setChartAttribute("caption", "Total Profit by Airline");
        chart.setChartAttribute("paletteColors", "#9d87f5, #faa27f, #9afa7f, #e37ffa, #7de1fa, #f8fa7f");
        chart.render();
    });
}

 //========
})
