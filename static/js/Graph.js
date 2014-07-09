
function drawGraph(scope, score, centrality, jsonFile, domId, charge, nodeClicked){
	var width = $(domId).width();
	var height = $(window).height();
	if( $("#menu") !== null ){
		height = $(window).height() - $("#menu").height() - $("mynav").height();
	}

	var color = d3.scale.category20b();

	var force = d3.layout.force()
	    .charge(charge)
	    .linkDistance(25)
	    .size([width, height]);
	    force.gravity(0.6);
	    
	var svg = d3.select(domId).append("svg")
	    .attr({
			"width": "100%",
			"height": "86%"
		})
		.attr("viewBox", "0 0 " + width + " " + height )
		.attr("preserveAspectRatio", "xMidYMid meet")
	    .append("g")
	    .call(d3.behavior.zoom().scaleExtent([1, 8]).on("zoom", zoom))
	    .append("g");
	function zoom(){
		svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
	}//end zoom()
	setTimeout(function(){
	d3.json(jsonFile, function(error, graph) {
		var edgeArr = [];
		var holdEdges = [];
		var edges = [];
		//only going to be called by the AUTHOR NETWORK graph
		if(score !== null){
			//removing the edges that are between a node with centrality lower than the one specified.
			for(var i = 0; i<graph.links.length; i++){
				if(graph.nodes[graph.links[i].source][centrality] >= score 
					&& graph.nodes[graph.links[i].target][centrality]>= score){
					edgeArr.push(graph.links[i]);
				}
			}
			for(var i = 0; i<edgeArr.length; i++){
				if(!holdEdges[edgeArr[i].source]){
					holdEdges[edgeArr[i].source] = [];
				}
				holdEdges[edgeArr[i].source][edgeArr[i].target] = edgeArr[i];
			}
			for(var i in holdEdges){
				for(var j in holdEdges[i]){
					edges.push(holdEdges[i][j]);
				}
			}
			graph.links = edges;
		}
		force
			.nodes(graph.nodes)
			.links(graph.links)
			.start();
	    	console.log(1);
	    for(var i = 160; i>0; --i){
	    	force.tick();
	    }
	    force.stop();
	    scope.$broadcast("GraphLoaded");
		var link = svg.selectAll(".link")
			.data(graph.links)
			.enter().append("line")
			.attr("class", "link")
			.attr("x1", function(d) { 
		  			return getEdgeCoord(centrality, d, score, d.source.x);
  			})
        	.attr("y1", function(d) { 
	  			return getEdgeCoord(centrality, d, score, d.source.y);
	  		})
        	.attr("x2", function(d) { 
	  			return getEdgeCoord(centrality, d, score, d.target.x);
	  		})
        	.attr("y2", function(d) { 
	  			return getEdgeCoord(centrality, d, score, d.target.y);
	  		})
			.style("stroke-width", function(d){ return Math.sqrt(d.value);});

	  	var node = svg.selectAll(".node")
	  		.data(graph.nodes)
	  		.enter().append("circle")
	  		.attr("class", "node")
	  		.attr("cx", function(d) { 
	  			return getNodeCoord(centrality, d, score, d.x);
	  			
    		})
        	.attr("cy", function(d) { 
	  			return getNodeCoord(centrality, d, score, d.y);
	  			
        	})
	  		.attr("r", function(d){
	  			if(d[centrality] < score){
	  				return 0;
	  			}
	  			else{
	  				return 5;
	  			}
	  		})
	  		.style("fill", function(d){

	  			var hue = Math.round((1/(d[centrality])));
	  			if(centrality === "group"){
	  				hue = d[centrality] * 10;
	  			}
	  			return "hsl("+hue+",100% ,50%)";
	  		})
	  		.on("click", function(d){
	  			if(d[centrality] >= score  || d[centrality] <= 0 ){
	  			
	  				scope.$emit(nodeClicked, d);
			        d3.selectAll(".link")
			        	.filter(function(l){
			                 return (l.source.index!==d.index && l.target.index!==d.index);
			             })
			             .style({'stroke-opacity':0.5,'stroke':'#999'});
			     
					d3.selectAll(".link")
						.filter(function(l){
							return (l.source.index===d.index || l.target.index===d.index);
			            })
			            .style({'stroke-opacity':0.8,'stroke':'#F0F'});
		  		}

	  		});
  			
	  	node.append("title")
	  		.text(function(d){ 
	  			if(d.title){
	  				return d.title;
	  			}
	  			return d.name+"\n Score "+d[centrality]; 
	  		});
		// svg.selectAll(".node")
	 //  		.style("fill", function(d){
	 //  			if(d[centrality] < score || d[centrality] <= 0 ){
	 //  				return "rgb(255,255,255)";
	 //  			}
	 //  			var hue = Math.round((1/(d[centrality])));
	 //  			return "hsl("+hue+",100% ,50%)";
	 //  		});
  		svg.selectAll("title")
	  		.text(function(d){ 
	  			return d.name+"\n Score: "+d[centrality]; 
	  		});
	
	});	
	}, 10);
}//end drawGraph()
function getNodeCoord(centrality, d, score, retVal){
	if(centrality === null){
		return retVal;
	}
	if(d[centrality] >= score){
		return retVal; 
	}
	return 0;
}
function getEdgeCoord(centrality, d, score, retVal){
	if(centrality === null){
		return retVal;
	}
	if(d.source[centrality] >= score 
			&& d.target[centrality] >= score
			&& d.source[centrality] >= 0
			&& d.target[centrality] >= 0){
			return retVal;
		} 
}
function chooseCentrality(typeCent){
	if(typeCent === "degreeCentrality"){
		return "Degree";
	}
	if(typeCent === "closenessCentrality"){
		return "Closeness";
	}
	if(typeCent === "betweennessCentrality"){
		return "Betweenness";
	}
	if(typeCent === "eigenvectorCentrality"){
		return "EigenVector";
	}
	if(typeCent === "group"){
		return "Group";
	}
}//end chooseCentrality()
