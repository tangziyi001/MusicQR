google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

function drawChart(){
	var data = new google.visualization.DataTable();
	data.addColumn('number','Day');
	data.addColumn('number', 'Rank');
	
	data.addRows([
		[1,2],
		[2,5],
		[3,11],
		[4,6],
		[5,8],
		[6,3],
		[7,9]
	]);
	var option = {
		chart: {title:'Number of Downloads Daily Rank'},
		width: 900,
		height: 500,
		axes: {
			x:{0: {side:'bottom'}}
		}
		
	}
	var chart = new google.charts.Line(document.getElementById('line_top_x'));
	chart.draw(data, options);
	
}
