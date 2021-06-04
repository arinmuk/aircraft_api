
urlstring='https://aircraft-apis.herokuapp.com/summarizecnt'
objdata={}
dataarr=[]
d3.json(urlstring).then(function(sample_m) {
    console.log(sample_m)
     var dataset = sample_m.map(objA => ({y:objA.Count , label :objA.AIRLINE} ))
    console.log(dataset)
    var objdata = sample_m.map(objA => ({x:objA.AIRLINE , value :objA.Count, category :objA.Group_Count} ))
    





    var chart = new CanvasJS.Chart("plot", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title:{
            text: "Top Airline Count"
        },
        axisY: {
            title: "Number "
        },
      
        data: [{        
            type: "column",  
            showInLegend: true, 
            legendMarkerColor: "grey",
            legendText: "top 30 Airlines",
            dataPoints: dataset     
                //{ y: sample_m.map(row=>row.Count), label: sample_m.map(row=>row.AIRLINE) },
                
            
        }]
    });
    chart.render();
    


    var chartdonut = new CanvasJS.Chart("plot2", {
        animationEnabled: true,
        title:{
            text: "Top Airline Count",
            horizontalAlign: "right"
        },
        data: [{
            type: "doughnut",
            startAngle: 60,
            //innerRadius: 60,
            indexLabelFontSize: 17,
            indexLabel: "{label} - #percent%",
            toolTipContent: "<b>{label}:</b> {y} (#percent%)",
            dataPoints: dataset
        }]
    });
    chartdonut.render();
    

    anychart.onDocumentReady(function() {
        var data3 =objdata
      
       // create a tag (word) cloud chart
        var chart3 = anychart.tagCloud(data3);
      
         // set a chart title
        chart3.title('30 of the top Airlines')
        // set an array of angles at which the words will be laid out
        chart3.angles([0])
        // enable a color range
        chart3.colorRange(true);
        // set the color range length
       chart3.colorRange().length('80%');
      
        // display the word cloud chart
        chart3.container("container");
        chart3.draw();
      });


    })
















