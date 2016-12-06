google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
document.addEventListener("DOMContentLoaded", main);
function main(){drawChart()}
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
	var options = {
		chart: {title:'Number of Downloads Daily Rank'},
		width: 900,
		height: 500,
		axes: {
			x:{0: {side:'bottom'}}
		},
		vAxis: {minValue:0, direction:-1}
		
	}
	var chart = new google.visualization.LineChart(document.getElementById('line_top_x'));
	chart.draw(data, options);
	
}
