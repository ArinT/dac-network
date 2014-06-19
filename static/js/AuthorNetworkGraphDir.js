app.controller("authorGraphCtrl", function($scope){
	$scope.typeGraph = "degree";
	$scope.$watch("typeGraph", function(newVal, old){
		$scope.$broadcast(newVal);
	});
});
app.directive("authorGraph", function(){
	return {
		restrict:"A",
		controller:"authorGraphCtrl",
		link:function(scope, elem, attrs){
			var width = $(window).width();
			var height = $(window).height();

			var color = d3.scale.category20b();

			var force = d3.layout.force()
			    .charge(-50)
			    .linkDistance(25)
			    .size([width, height]);
			    force.gravity(0.4);
			    
			var svg = d3.select("#author-graph").append("svg")
			    .attr({
					"width": "100%",
					"height": "86%"
				})
				.attr("viewBox", "0 0 " + width + " " + height )
				.attr("preserveAspectRatio", "xMidYMid meet")
			    .append("g")
			    .call(d3.behavior.zoom().scaleExtent([1, 8]).on("zoom", zoom))
			    .append("g");
			    
			function zoom() {
			  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
			}

			d3.json("../../static/json/authors_centrality.json", function(error, graph) {
				console.log(graph.nodes[0])
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
			  			var hue = Math.round((1/d.degreeCentrality));
			  			return "hsl("+hue+",100% ,50%)";
			  		})
			  		.on("click", function(d){
			  			scope.$emit("AuthorNodeClicked", d);
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
			  		});
		  		scope.$on("closeness",function(){
					svg.selectAll(".node")
					  		.style("fill", function(d){
					  			var hue = Math.round((1/d.closenessCentrality));
					  			return "hsl("+hue+",100% ,50%)";
					  		});
			  		svg.selectAll("title")
				  		.text(function(d){ 
				  			return d.name+"\n Score: "+d.closenessCentrality; 
				  		});

		  		});
		  		scope.$on("degree",function(){
					svg.selectAll(".node")
					  		.style("fill", function(d){
					  			var hue = Math.round((1/d.degreeCentrality));
					  			return "hsl("+hue+",100% ,50%)";
					  		});
			  		svg.selectAll("title")
				  		.text(function(d){ 
				  			return d.name+"\n Score: "+d.degreeCentrality; 
				  		});

		  		});
		  		scope.$on("betweenness",function(){
					svg.selectAll(".node")
					  		.style("fill", function(d){
					  			var hue = Math.round((1/d.betweennessCentrality));
					  			return "hsl("+hue+",100% ,50%)";
					  		});
			  		svg.selectAll("title")
				  		.text(function(d){ 
				  			return d.name+"\n Score: "+d.betweennessCentrality; 
				  		});

		  		});	
			  	node.append("title")
			  		.text(function(d){ 
			  			return d.name+"\n Score "+d.degreeCentrality; 
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
