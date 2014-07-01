app.controller("authorGraphCtrl", function($scope){
	$scope.typeGraph = "degree";
	$scope.chosenScore = 0;
	$scope.chosenCentrality = chooseCentrality($scope.typeGraph);
	$scope.$watch("chosenScore", function(val, oldVal){
		if(val !== oldVal){
			$scope.$broadcast("NewGraph");
		}
	});
	$scope.$watch("typeGraph", function(newVal, oldVal){
		if(newVal !== oldVal){
			$scope.chosenCentrality = chooseCentrality($scope.typeGraph);
			$scope.$broadcast("NewGraph");
		}
	});
});

app.directive("authorGraph", function(){
	return {
		restrict:"A",
		controller:"authorGraphCtrl",
		link:function(scope, elem, attrs){
			drawGraph(scope.chosenScore,"degreeCentrality");
			
			scope.$on("NewGraph",function(){
				$("svg").remove();
	  			drawGraph(scope.chosenScore, scope.chosenCentrality);
	  		});
		}//end link
	}//end return
});
function chooseCentrality(typeCent){
	if(typeCent === "degree"){
		return "degreeCentrality";
	}
	if(typeCent === "closeness"){
		return "closenessCentrality";
	}
	if(typeCent === "betweenness"){
		return "betweennessCentrality";
	}
}//end chooseCentrality()
function zoom(){
	svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}//end zoom()
function drawGraph(score, centrality){
	var width = $(window).width();
	var height = $(window).height();

	var color = d3.scale.category20b();

	var force = d3.layout.force()
	    .charge(-50)
	    .linkDistance(25)
	    .size([width, height]);
	    force.gravity(0.6);
	    
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
	d3.json("../../static/json/authors_centrality.json", function(error, graph) {
		//removing the edges that are between a node with centrality lower than the one specified.
		for(var i = 0; i<graph.links.length; i++){
			if(graph.nodes[graph.links[i].source][centrality]< score 
				|| graph.nodes[graph.links[i].target][centrality]< score){
				graph.links.splice(i,1);
			}
		}
		//CANNOT remove values fromt the node array, because we would have to edit the values of the edges.
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
	  		.attr("r", function(d){
	  			if(d[centrality] < score || d[centrality] <= 0){
	  				return 0;
	  			}
	  			else{
	  				return 5;
	  			}
	  		})
	  		.style("fill", function(d){
	  			var hue = Math.round((1/(d[centrality])));
	  			return "hsl("+hue+",100% ,50%)";
	  		})
	  		.on("click", function(d){
	  			if(d[centrality] < score  && d[centrality] > 0 ){
	  				return;
	  			}
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
  			
	  	node.append("title")
	  		.text(function(d){ 
	  			return d.name+"\n Score "+d[centrality]; 
	  		});
		svg.selectAll(".node")
	  		.style("fill", function(d){
	  			if(d[centrality] < score || d[centrality] <= 0 ){
	  				return "rgb(255,255,255)";
	  			}
	  			var hue = Math.round((1/(d[centrality])));
	  			return "hsl("+hue+",100% ,50%)";
	  		});
  		svg.selectAll("title")
	  		.text(function(d){ 
	  			return d.name+"\n Score: "+d[centrality]; 
	  		});
	  	force.on("tick", function() {
	  		link.attr("x1", function(d) { 
		  			if(d.source[centrality] >= score 
		  				&& d.target[centrality] >= score
		  				&& d.source[centrality] > 0
		  				&& d.target[centrality] > 0){
		  				return d.source.x;
		  			} 
	  			})
	        	.attr("y1", function(d) { 
		  			if(d.source[centrality] >= score 
		  				&& d.target[centrality] >= score
		  				&& d.source[centrality] > 0
		  				&& d.target[centrality] > 0){
		  				return d.source.y;
		  			} 
		  		})
	        	.attr("x2", function(d) { 
		  			if(d.source[centrality] >= score 
		  				&& d.target[centrality] >= score
		  				&& d.source[centrality] > 0
		  				&& d.target[centrality] > 0){
		  				return d.target.x;
		  			} 
		  		})
	        	.attr("y2", function(d) { 
		  			if(d.source[centrality] >= score 
		  				&& d.target[centrality] >= score
		  				&& d.source[centrality] > 0
		  				&& d.target[centrality] > 0){
		  				return d.target.y;
		  			} 
		  		});

	    	node.attr("cx", function(d) { 
		  			if(d[centrality] >= score){
	    				return d.x; 
	    			}
	    			return 0;
	    		})
	        	.attr("cy", function(d) { 
		  			if(d[centrality] >= score){
	        			return d.y; 
	        		}
	        		return 0;
	        	});
	  	});
	});	
}//end drawGraph()
