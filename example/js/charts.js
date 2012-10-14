function cloneArray(arr) {
	var a = new Array(); 
	for (var property in arr) {
		a[property] = typeof (arr[property]) == 'object' ? cloneArray(arr[property]) : arr[property]
	} return a
}

function navItemClick() {
	$('nav a').removeClass('active');
	$(this).addClass('active');
	var current = $(this).html();
	if (current === 'showAll')
		current = null;
	plotCharts(current);
}

function createUserNav() {
	var current = window.location.hash.substr(1, window.location.hash.length-1);
	var nav = $("nav");
	var navItem = $('<a href="#overview" class="active">showAll</a>');
	var overviewItem = navItem;
	nav.append(navItem);
	navItem.click(navItemClick);
		
	var user = false;
	$(users).each(function(i, user) {
		navItem = $('<a href="#' + user + '">' + user + '</a>');
		navItem.click(navItemClick);
		nav.append(navItem);
		if (current === user) {
			navItemClick.call(navItem);
			user = true;
		}
	});
	
	if (!user) 
		navItemClick.call(overviewItem);
}	

function normalizeBubbles(plot, series, datapoints) {
	var referenceEntries = series.data;
//	var referenceEntries = dayhourData[0].data;
	var overviewEntries = dayhourData[0].data;

	var max = 0;
	for (var i = 0; i < referenceEntries.length; i++) {
		if (referenceEntries[i][2] > max)
			max = referenceEntries[i][2];
	}
	var dataEntries = series.data
    for (var i = 0; i < dataEntries.length; i++)
    	dataEntries[i][2] = dataEntries[i][2] / max * 1.2;
}
	
var dateOptions = {
	zoom: { interactive: true },
	pan: { interactive: true },
	xaxis: {
		zoomRange: null,  // or [number, number] (min range, max range) or false
		panRange: null,   // or [number, number] (min, max) or false
		mode: 'time',
		timeformat: "%d.%m."
	},
	yaxis: {
		zoomRange: false,  // or [number, number] (min range, max range) or false
		panRange: false,   // or [number, number] (min, max) or false
		tickDecimals: 0
	},
	series: {
		stack: true,
		bars: { show: true, fill: 0.6, lineWidth: 0, align: 'center', barWidth: 24*60*60*1000 }
	},
	grid: { hoverable: true }
};
	
var dayhourOptions = {
	xaxis: {
		zoomRange: null,  // or [number, number] (min range, max range) or false
		panRange: null,   // or [number, number] (min, max) or false
		tickSize: 1,
		tickDecimals: 0
	},
	yaxis: {
		zoomRange: false,  // or [number, number] (min range, max range) or false
		panRange: false,   // or [number, number] (min, max) or false
		tickFormatter: function(num) { return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', ''][num] },
		tickDecimals: 0,
		tickSize: 1
	},
	series: {
		bubbles: {
			active: true,
			show: true,
			fill: true,
			lineWidth: 0
		}
	},
	grid: { hoverable: true },
	hooks: {
		processDatapoints: [normalizeBubbles]
	}
};

var hourOptions = {
	xaxis: {
		tickFormatter: function(num) { return parseInt(num).toString(); },
		tickSize: 1,
		zoomRange: null,  // or [number, number] (min range, max range) or false
		panRange: null   // or [number, number] (min, max) or false
	},
	yaxis: {
		zoomRange: false,  // or [number, number] (min range, max range) or false
		panRange: false,   // or [number, number] (min, max) or false
		tickDecimals: 0
	},
	series: {
		stack: true,
		bars: { show: true, fill: 0.6, lineWidth: 0, align: 'center' }
	},
	grid: { hoverable: true }
};
var dayOptions = {
	xaxis: {
		tickFormatter: function(num) { return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][num] },
		tickSize: 1,
		zoomRange: null,  // or [number, number] (min range, max range) or false
		panRange: null   // or [number, number] (min, max) or false
	},
	yaxis: {
		zoomRange: false,  // or [number, number] (min range, max range) or false
		panRange: false,   // or [number, number] (min, max) or false
		tickDecimals: 0
	},
	series: {
		stack: true,
		bars: { show: true, fill: 0.6, lineWidth: 0, align: 'center' }
	},
	grid: { hoverable: true}
};
var nameOptions = {
	legend: {
		show: false
	},
	series: {
		show: true,
		pie: {
			show: true,
			radius: 5/6,
			innerRadius: 0.5,
			label: {
				show: true,
				radius: 1,
				formatter: function(label, series) {
					return '<div style="padding: 4px;">'+label+'<br/>'+Math.round(series.percent)+'%</div>';
				},
				threshold: 0.1,
				background: { opacity: 0.6 } 
			}
		}
	},
	grid: { hoverable: true }
};

function plotCharts(user=null) {
	var userHourData = hourData;
	var userDayData = dayData;
	var userDateData = overviewData;
	var userDayhourData = [cloneArray(dayhourData[0].data)];
	var color = null;
	
	if (user != null) {
		$(hourData).each(function (i, data) {
			if (data['label'] === user)
				userHourData = [data];
		});
		$(overviewData).each(function (i, data) {
			if (data['label'] === user)
				userDateData = [data];
		});
		$(dayData).each(function (i, data) {
			if (data['label'] === user)
				userDayData = [data];
		});
		$(dayhourData).each(function (i, data) {
			if (data['label'] === user)
				userDayhourData = [cloneArray(data)];
		});
		
		color = users.indexOf(user);
	} 
	
	hourOptions.series.color = color;
	dayOptions.series.color = color;
	dateOptions.series.color = color;
	if (color === null)
		color = '#888888';
	dayhourOptions.series.color = color;
	$.plot($("#hour"), userHourData, hourOptions);
	$.plot($("#dayhour"), userDayhourData, dayhourOptions);
	$.plot($("#day"), userDayData, dayOptions);
	$.plot($("#date"), userDateData, dateOptions);
	$.plot($("#name"), nameData, nameOptions);
}

$(document).ready(function() {
		 
	createUserNav();
	
	function showTooltip(x, y, contents) {
		$('<div id="tooltip">' + contents + '</div>').css( {
			position: 'absolute',
			display: 'none',
			top: y + 5,
			left: x + 5,
			border: '1px solid #fdd',
			padding: '2px',
			'background-color': '#fee',
			opacity: 0.80
		}).appendTo("body").fadeIn(100);
	}
	
	var previousPoint = null;
	$("#date, #day, #hour").bind("plothover", function (event, pos, item) {
		if (item) {
			if (previousPoint != item.datapoint) {
				previousPoint = item.datapoint;

				$("#tooltip").remove();
				var x = item.datapoint[0],
					y = Math.round((item.datapoint[1] - item.datapoint[2]) * 10) / 10.0;

				showTooltip(item.pageX, item.pageY, item.series.label + ": " + y);
			}
		}
		else {
			$("#tooltip").remove();
			previousPoint = null;            
		}
	});
	
});