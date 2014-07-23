
function drawGraph(scope, isCitationNetwork, score, centrality, jsonFile, domId, charge, nodeClicked){
	var width = $(domId).width();
	var height = $(window).height();
	if( $("#menu") !== null ){
		height = $(window).height() - $("#menu").height() - $("mynav").height();
	}

	var color = d3.scale.category20b();

	var force = d3.layout.force()
	    .charge(-500)
	    .linkDistance(70)
	    .size([width, height]);
	    force.gravity(0.6);
	    
	var svg = d3.select(domId).append("svg")
	    .attr({
			"width": "100%",
			"height": "86%"
		})
		.attr("viewBox", "0 0 " + width + " " + height )
		.attr("preserveAspectRatio", "xMidYMid meet")
	    .call(d3.behavior.zoom().scaleExtent([0, 8]).on("zoom", zoom))
		.append("g")
		.attr("id", "transformme");
	    
	if (isCitationNetwork){
		svg.append('svg:defs').append('svg:marker')
		    .attr('id', 'end-arrow')
		    .attr('viewBox', '0 -5 10 10')
		    .attr('refX', 6)
		    .attr('markerWidth', 5)
		    .attr('markerHeight', 5)
		    .attr('orient', 'auto')
		  .append('svg:path')
		    .attr('d', 'M0,-5L10,0L0,5')
		    .attr('fill', '#000');

		svg.append('svg:defs').append('svg:marker')
		    .attr('id', 'start-arrow')
		    .attr('viewBox', '0 -5 10 10')
		    .attr('refX', 4)
		    .attr('markerWidth', 5)
		    .attr('markerHeight', 5)
		    .attr('orient', 'auto')
		  .append('svg:path')
		    .attr('d', 'M10,-5L0,0L10,5')
		    .attr('fill', '#000');
	}

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
				var edge = graph.links[i];			
				var src = graph.nodes[edge.source];
				var tgt = graph.nodes[edge.target];
				
				if(src[centrality] >= score && tgt[centrality]>= score){
					if (edge.year == undefined)
					{
						edgeArr.push(graph.links[i]);
					}
					else
					{
						START = "2002";
						END = "2012";
						if (edge.year >= START && edge.year <= END)
						{
							edgeArr.push(graph.links[i]);
						}					
					}
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
	    
	    for(var i = 160; i>0; --i){
	    	force.tick();
	    }
	    force.stop();
	    scope.$broadcast("GraphLoaded");
		var link = svg.append('svg:g');
			
		if(isCitationNetwork){
			link.selectAll("path").data(graph.links)
			.enter().append("path")
			.attr("class", "link")
			.attr("d",function(d){
				var deltaX = d.target.x - d.source.x,
				deltaY = d.target.y - d.source.y,
				dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
				normX = deltaX / dist,
				normY = deltaY / dist,
				sourcePadding = 0; //d.left ? 17 : 12,
				targetPadding =  12;// : 12,
				sourceX = d.source.x + (sourcePadding * normX),
				sourceY = d.source.y + (sourcePadding * normY),
				targetX = d.target.x - (targetPadding * normX),
				targetY = d.target.y - (targetPadding * normY);
				if(sourceX){
					return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;

				}
					// return 'M'+d.source.x+','+d.source.y+'L'+d.target.x+','+d.target.y;
			})
			.style('marker-end', function(d) { return 'url(#end-arrow)'; });
		}
		else{
			link.selectAll("line").data(graph.links)
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
			.style("stroke-width", function(d){ return d.value;});

		}

	  	var node = svg.append("svg:g").selectAll("g")
	  		.data(graph.nodes)
	  		.enter().append("circle")
	  		.attr("class", "node")
	  		.attr("id", function(d){
	  			return d["name"].replace(/\s+/g, '');
	  		})
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
				var hue = 0;
				switch  (centrality){
					case "group":
						hue = d[centrality] * 10;
						break;
					case "degreeCentrality":
						if (!isCitationNetwork)
						{
							hue = 100-Math.round((1/(d[centrality])));
						}
						else if (d[centrality] != 0)
						{
							hue = (Math.log(d[centrality])+4)*30;
						}
						else
						{
							hue = 0;
						}				
						break;
					case "betweennessCentrality":
						if (!isCitationNetwork && d[centrality] != 0)
						{
							hue = (Math.log(d[centrality])+13)*10;
						}
						else if (d[centrality] != 0)
						{
							hue = (Math.log(d[centrality])+12)*10;
						}
						break;
					case "closenessCentrality":
						if (!isCitationNetwork && d[centrality] != 0)
						{
							hue = (Math.log(d[centrality])+6)*15;
						}
						else if (d[centrality] != 0)
						{
							if (Math.log(d[centrality])>-1)
							{
								hue = (Math.log(d[centrality])+1)*120;
							}
							else
							{
								hue = 0;
							}
						}
						break;
					case "eigenvectorCentrality":
						if (d[centrality] != 0 && Math.log(d[centrality])>-12)
						{
							
							hue = (Math.log(d[centrality])+12)*10;
						}
						else
						{
							hue = 0;
						}
						break;
					default:
						hue = 0;
					}				
	  			return "hsl("+hue+",100% ,50%)";
	  		})
	  		.on("click", function(d){
	  			if(d[centrality] >= score  || d[centrality] <= 0 ){
	  			
	  				scope.$emit(nodeClicked, {
	  					'name': d['name'],
	  					'id': d['id'],
	  					'centrality': centrality,
	  					'score': d[centrality]
	  				});
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
