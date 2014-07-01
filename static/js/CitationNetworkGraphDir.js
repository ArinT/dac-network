app.directive("citationGraph", function(){
	return {
		restrict:"A",
		controller:function($scope){

		},
		link:function(scope, elem, attrs){
			var width = $(window).width();
			var height = $(window).height();

			var color = d3.scale.category20b();

			var force = d3.layout.force()
			    .charge(-250)
			    .linkDistance(75)
			    .size([width, height]);
			    force.gravity(0.25);

			var svg = d3.select("#citation-graph").append("svg")
			    // .attr("width", width)
			    // .attr("height", height)
				.attr({
					"width": "100%",
					"height": "80%"
				})
				.attr("viewBox", "0 0 " + width + " " + height )
				.attr("preserveAspectRatio", "xMidYMid meet")
			    .append("g")
			    .call(d3.behavior.zoom().scaleExtent([1, 8]).on("zoom", zoom))
			    .append("g");
			    
			function zoom() {
			  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
			}
			setTimeout(function(){
			d3.json("../../static/json/citations.json", function(error, graph) {
				force
					.nodes(graph.nodes)
					.links(graph.links);
					// .start();
			    
			    force.start();
			    for(var i = 1600; i>0; --i){
			    	force.tick();
			    }
			    force.stop();

			    //adding the positions of the lines and nodes here, instead of on "tick" makes it static
				var link = svg.selectAll("line")
					.data(graph.links)
					.enter().append("line")
					.attr("class", "link")
					.attr("x1", function(d) { return d.source.x; })
		        	.attr("y1", function(d) { return d.source.y; })
		        	.attr("x2", function(d) { return d.target.x; })
		        	.attr("y2", function(d) { return d.target.y; })
					.style("stroke-width", function(d){ return Math.sqrt(d.value);});

				svg.append("svg:g")
					.selectAll("circle")
					.data(graph.nodes)
					.enter().append("svg:circle")
					.attr("class","node")
					.attr("cx", function(d) { return d.x })
					.attr("cy", function(d) { return d.y })
					.attr("r", 5)
					.on("click", function(d){
			  			scope.$emit("CitationNodeClicked", d);
				         d3.selectAll(".link")
				            .filter(function(l)
				             {
				                 return (l.source.index!==d.index && l.target.index!==d.index);
				             })
				             .style({'stroke-opacity':0.5,'stroke':'#999'});
				     
				             d3.selectAll(".link")
				            .filter(function(l)
				             {
				                 return (l.source.index===d.index || l.target.index===d.index);
				             })
				             .style({'stroke-opacity':0.8,'stroke':'#F0F'});
			  			
			  		})
			  		.append("title")
			  		.text(function(d){ 
			  			return d.title; 
			  		});


				// svg.append("svg:g")
				// 	.selectAll("")

			  	// var node = svg.selectAll("circle")
			  	// 	.data(graph.nodes)
			  	// 	.enter().append("circle")
			  	// 	.attr("class", "node")
			  	// 	.attr("r", 5)
			  	// 	.style("fill", function(d){
			  	// 		if(d.centralityScore == -1){
			  	// 			return "hsl(120,100% ,50%)";
			  	// 		}
			  	// 		var hue = Math.round((d.centralityScore) * 100);
			  	// 		return "hsl("+hue+",100% ,50%)";
			  	// 	})
			  	// 	// .style("fill",color(2))
			  		// .on("click", function(d){
			  		// 	scope.$emit("clicked", d);
				   //       d3.selectAll(".link")
				   //          .filter(function(l)
				   //           {
				   //               return (l.source.index!==d.index && l.target.index!==d.index);
				   //           })
				   //           .style({'stroke-opacity':0.5,'stroke':'#999'});
				     
				   //           d3.selectAll(".link")
				   //          .filter(function(l)
				   //           {
				   //               return (l.source.index===d.index || l.target.index===d.index);
				   //           })
				   //           .style({'stroke-opacity':0.8,'stroke':'#F0F'});
			  			
			  		// });
			  	// node.append("title")
			  	// 	.text(function(d){ 
			  	// 		return d.title; 
			  	// 	});
			  	

			  	// force.on("tick", function() {
			  	// 	link.attr("x1", function(d) { return d.source.x; })
			   //      	.attr("y1", function(d) { return d.source.y; })
			   //      	.attr("x2", function(d) { return d.target.x; })
			   //      	.attr("y2", function(d) { return d.target.y; });

			   //  	node.attr("cx", function(d) { return d.x; })
			   //      	.attr("cy", function(d) { return d.y; });
			  	// });
			});//end d3 json
			},10);
		}//end link
	}
});
