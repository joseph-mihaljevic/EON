/*
 * Parse the data and create a graph with the data.
 */

 function parseData(createGraph,From,To,step,csvFile, title,x_axis,y_axis) {
 	Papa.parse(csvFile, {
 		download: true,
 		complete: function(results) {
 			createGraph(results.data,From,To,step, title,x_axis,y_axis);
 		}
 	});
 }


function createGraph(data,From,To,step, title,x_axis,y_axis) {
	var years = [];
	var silverMinted = ["I"];
	for (var i = From; i < To; i+=step) {

		silverMinted.push(data[i][3]);
	}

	var chart = c3.generate({
		bindto: '#chart',
    data: {
      columns: [
      	silverMinted
      ]
    },
    axis: {
      y: {
        label: {
          text: x_axis,
          position: 'outer-middle'
        }
      },
      x: {
        label: {
          text: y_axis,
          position: 'outer-middle'
        }
      }
    },
    zoom: {
    	enabled: true
  	},
    legend: {
      position: 'right'
    }
	});

	var chartdivadsjja = d3.select('#chart').append('p')
					.text(title)
					.attr('style', 'position: absolute; display: block; top: 0; left: 50%; z-index: 100; transform: translateX(-50%);');
}

//parseData(createGraph,50,1);
