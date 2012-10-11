function navItemClick() {
	$('nav a').removeClass('active');
	$(this).addClass('active');
	var current = $(this).html();
}

function createUserNav() {
	var nav = $("nav");
	var navItem = $('<a href="#" class="active">showAll</a>');
	nav.append(navItem);
	navItem.click(navItemClick);
	
	var current = window.location.hash.substr(1, window.location.hash.length-1);
	$(users).each(function(i, user) {
		navItem = $('<a href="#' + user + '">' + user + '</a>');
		navItem.click(navItemClick);
		nav.append(navItem);
		if (current === user)
			navItemClick.call(navItem);
	});
}

$(document).ready(function() {
		 
	createUserNav();
		 
	var options = {
		xaxis: {
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

	options.xaxis.tickFormatter = function(num) {return parseInt(num).toString();};
	options.xaxis.tickSize = 1;
	$.plot($("#hour"), hourData, options);
	options.xaxis.tickFormatter = null;
	
	options.xaxis.tickFormatter = function(num) {return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][num]};
	$.plot($("#day"), dayData, options);
	
	options.series.pie = { 
					show: true,
                    radius: 5/6,
                	innerRadius: 0.5,
                    label: {
	                    show: true,
	                    radius: 1,
	                    formatter: function(label, series){
	                        return '<div style="padding: 4px;">'+label+'<br/>'+Math.round(series.percent)+'%</div>';
	                    },
	                    threshold: 0.1,
                    	background: { opacity: 0.6 } 
	                }
              	};
	options.legend = {show: false}
	options.xaxis.tickFormatter = null
	options.xaxis.tickSize = null;
	$.plot($("#name"), nameData, options);
	options.series.pie = {show: false};
	options.legend.show = true;
	
	options.zoom = {interactive: true};
	options.pan = {interactive: true};
	options.xaxis.mode = 'time';
	options.xaxis.timeformat = "%d.%m.";
	options.series.bars.barWidth = 24*60*60*1000;
	$.plot($("#date"), overviewData, options);
	
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