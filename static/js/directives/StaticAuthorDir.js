app.directive("staticAuthor", function(){
	return {
		restrict:"A",
		controller:function($scope){

		},
		link:function(scope, elem, attrs){
			var width = 800; //$("#author-graph").width();
			var height = 800; //1000; //$("#author-graph").height();

			var color = d3.scale.category20b();

			var force = d3.layout.force()
			    .charge(-50)
			    .linkDistance(25)
			    .size([width, height]);
			    force.gravity(0.4);
			    
			var svg = d3.select("#static-author").append("svg")
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

			setTimeout(function(){
			d3.json("../../static/json/authors_centrality.json", function(error, graph) {
				console.log(graph.nodes[0])
				force
					.nodes(graph.nodes)
					.links(graph.links)
					// .start();
			    force.start();
			    for(var i = 100; i>0; --i){
			    	force.tick();
			    }
			    force.stop();

			    
				var link = svg.selectAll("line")
					.data(graph.links)
					.enter().append("line")
					.attr("class", "link")
					.attr("x1", function(d) { return d.source.x; })
		        	.attr("y1", function(d) { return d.source.y; })
		        	.attr("x2", function(d) { return d.target.x; })
		        	.attr("y2", function(d) { return d.target.y; })
					.style("stroke-width", function(d){ return Math.sqrt(d.value);});

			  	var node = svg.append("svg:g")
					.selectAll("circle")
					.data(graph.nodes)
					.enter().append("svg:circle")
					.attr("class","node")
					.attr("cx", function(d) { return d.x })
					.attr("cy", function(d) { return d.y })
					.attr("r", 5)
			  		.style("fill", function(d){
			  			if(d.degreeCentrality == -1){
			  				return "hsl(120,100% ,50%)";
			  			}
			  			var hue = Math.round((d.degreeCentrality) * 100);
			  			return "hsl("+hue+",100% ,50%)";
			  		})
			  		// .style("fill",color(2))
			  		.on("click", function(d){
			  			scope.$emit("AuthorNodeClicked", d);
			  			 // document.getElementById("demo").value=d.name+"\n Score "+d.centralityScore;
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
			  			// document.getElementById("demo").value=d.name+"\n Score "+d.centralityScore;
			  		});
			  	node.append("title")
			  		.text(function(d){ 
			  			return d.name+"\n Score "+d.degreeCentrality; 
			  		});
			  	link.append("title")
			  		.text(function(d){
			        	return "number of papers:"+d.value;          
			      	});

			  	// force.on("tick", function() {
			  	// 	link.attr("x1", function(d) { return d.source.x; })
			   //      	.attr("y1", function(d) { return d.source.y; })
			   //      	.attr("x2", function(d) { return d.target.x; })
			   //      	.attr("y2", function(d) { return d.target.y; });

			   //  	node.attr("cx", function(d) { return d.x; })
			   //      	.attr("cy", function(d) { return d.y; });
			  	// });
			});
			},10);
		}
	}
});