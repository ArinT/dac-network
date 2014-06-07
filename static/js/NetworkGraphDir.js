app.directive("graph", function(){
	return {
		restrict:"A",
		controller:function($scope){

		},
		link:function(scope, elem, attrs){
			var width = 1000,
			    height = 1000;

			var color = d3.scale.category20b();

			var force = d3.layout.force()
			    .charge(-50)
			    .linkDistance(25)
			    .size([width, height]);
			    force.gravity(0.25);

			var svg = d3.select("#graph").append("svg")
			    .attr("width", width)
			    .attr("height", height)
			    .append("g")
			    .call(d3.behavior.zoom().scaleExtent([1, 8]).on("zoom", zoom))
			    .append("g");
			    
			function zoom() {
			  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
			}

			d3.json("../../static/json/author.json", function(error, graph) {
				force
					.nodes(graph.nodes)
					.links(graph.links)
					.start();
			      
			    
				var link = svg.selectAll(".link")
					.data(graph.links)
					.enter().append("line")
					.attr("class", "link")
					.style("stroke-width", function(d){ return Math.sqrt(d.value);});

			  	var node = svg.selectAll(".node")
			  		.data(graph.nodes)
			  		.enter().append("circle")
			  		.attr("class", "node")
			  		.attr("r", 5)
			  		.style("fill", function(d){
			  			if(d.centralityScore == -1){
			  				return "hsl(120,100% ,50%)";
			  			}
			  			var hue = Math.round((d.centralityScore) * 100);
			  			return "hsl("+hue+",100% ,50%)";
			  		})
			  		// .style("fill",color(2))
			  		.on("click", function(d){
			  			scope.$emit("clicked", d);
			  			// document.getElementById("demo").value=d.name+"\n Score "+d.centralityScore;
			  		});
			  	node.append("title")
			  		.text(function(d){ 
			  			return d.name+"\n Score "+d.centralityScore; 
			  		});
			  	link.append("title")
			  		.text(function(d){
			        	return "number of papers:"+d.value;          
			      	});

			  	force.on("tick", function() {
			  		link.attr("x1", function(d) { return d.source.x; })
			        	.attr("y1", function(d) { return d.source.y; })
			        	.attr("x2", function(d) { return d.target.x; })
			        	.attr("y2", function(d) { return d.target.y; });

			    node.attr("cx", function(d) { return d.x; })
			        .attr("cy", function(d) { return d.y; });
			  	});
			});
		}
	}
});