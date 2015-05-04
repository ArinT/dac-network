app.service("GraphService", function($http){
	this.height = $(window).height(); // This is not correct, change using setWindowHeight before using!!
	this.force;
	this.svg;
	
	this.getNodeHue = function(score, centrality, isCitationNetwork){
		var hue = 0;
		switch  (centrality){
			case "group":
				return score * 10;
			case "degreeCentrality":
				if (!isCitationNetwork)
				{
					return 100-Math.round((1/(score)));
				}
				else if (score != 0)
				{
					return (Math.log(score)+4)*30;
				}
				else
				{
					return 0;
				}	
			case "betweennessCentrality":
				if (!isCitationNetwork && score != 0)
				{
					return (Math.log(score)+13)*10;
				}
				else if (score != 0)
				{
					return (Math.log(score)+12)*10;
				}
				return 0;
			case "closenessCentrality":
				if (!isCitationNetwork && score != 0)
				{
					return (Math.log(score)+6)*15;
				}
				else if (score != 0)
				{
					if (Math.log(score)>-1)
					{
						return (Math.log(score)+1)*120;
					}
					else
					{
						return 0;
					}
				}
				return 0;
			case "eigenvectorCentrality":
				if (score != 0 && Math.log(score)>-12)
				{
					
					return (Math.log(score)+12)*10;
				}
				else
				{
					return 0;
				}
			default:
				return 0;
		}				
	}
	var getNodeHue = this.getNodeHue;
	
	var getYear = function(doi){
		var split = doi.split("-");
		return parseInt(split[0].slice(4));
	}
	
	var getNodeCoord = function(centrality, d, score, retVal, width){
		if(centrality === null){
			return retVal;
		}
		if(d[centrality] >= score){
			return retVal; 
		}
		return 0;
	}
	
	var getEdgeCoord = function(centrality, d, score, retVal){
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

	this.setWindowHeight = function(height) {
		this.height = height;
	}

	this.drawGraph = function(scope, isCitationNetwork, score, centrality, jsonFile, domId, charge, nodeClicked, isChronological){
		var width = $(domId).width();
		// if( $("#menu") !== null ){
		// 	height = $(window).height() - $("#menu").height() - $("mynav").height();
		// }

		var color = d3.scale.category20b();

		var force = d3.layout.force()
		    .charge(-500)
		    .linkDistance(70)
		    .size([width, this.height]);
		    force.gravity(0.6);
		this.force = force;
		    
		var svg = d3.select(domId).append("svg")
		    .attr({
				"width": "100%",
				"height": "86%"
			})
			.attr("viewBox", "0 0 " + width + " " + this.height )
			.attr("preserveAspectRatio", "xMidYMid meet")
		    .call(d3.behavior.zoom().scaleExtent([0, 8]).on("zoom", zoom))
			.append("g")
			.attr("id", "transformme");
		this.svg = svg;
		    
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

		var gradient = svg.append("svg:defs").append("linearGradient")
				.attr("id", "grad2")
				.attr("x1", "0%")
				.attr("y1", "0%")
				.attr("x2", "0%")
				.attr("y2", "100%");
			gradient.append("svg:stop")
				.attr("offset", "0%")
				.style({'stop-color':'rgb(255,0,255)', 'stop-opacity':'1'});
			gradient.append("svg:stop")
				.attr("offset", "100%")
				.style({'stop-color':'rgb(0,0,255)', 'stop-opacity':'1'});


		function zoom(){
			svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
		}//end zoom()

		setTimeout(function(){
			d3.json(jsonFile, function(error, graph) {
				var edgeArr = [];
				var holdEdges = [];
				var edges = [];
				//only going to be called by the AUTHOR NETWORK graph
				//double check this boolean
				console.log(graph.links)
				if(score !== null){
					//removing the edges that are between a node with centrality lower than the one specified.
					for(var i = 0; i<graph.links.length; i++){
						var edge = graph.links[i];			
						var src = graph.nodes[edge.source];
						var tgt = graph.nodes[edge.target];
						// console.log ("source: ");
						// console.log (src);
						// console.log ("target: ");
						// console.log (tgt);
						// console.log ("edge: ");
						// console.log (edge);
						// console.log (" ");
						// console.log (src[centrality]);
						// console.log (score);
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
					// console.log (edgeArr);
					for(var i = 0; i<edgeArr.length; i++){
						if(!holdEdges[edgeArr[i].source]){
							holdEdges[edgeArr[i].source] = [];
						}
						holdEdges[edgeArr[i].source][edgeArr[i].target] = edgeArr[i];
					}
					for(var i in holdEdges){
						for(var j in holdEdges[i]){
							if (holdEdges[i][j] != undefined) edges.push(holdEdges[i][j]);
						}
					}
					// console.log (edges);
					// for (var i in edges){
					// 	console.log (i)
					// }
					console.log ("before d3 force");
					console.log(edges)
					graph.links = edges;
				}
				force
					.nodes(Object.keys(graph.nodes).map(function (k) {return graph.nodes[k]}))
					.links(graph.links)
					.start();
			    
			    for(var i = 160; i>0; --i){
			    	force.tick();
			    }
			    force.stop();

			  	var link = svg.append('svg:g').attr("id", "edges");
					
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
						sourcePadding = 5; //d.left ? 17 : 12,
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
					.style('marker-end', function(d) { return 'url(#end-arrow)'; })
					.style("stroke", function(d){
						if(d.target.backbone && d.source.backbone){
							return "#0000FF";
						}
					})
					.style('stroke-width', function(d){
						if(d.target.backbone && d.source.backbone){
							return 2.5;
						}
					});
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
					.style("stroke-width", function(d){ return d.value;})
					.style("stroke", function(d){
						if(d.target.backbone && d.source.backbone){
							return "#0000FF";
						}
					})
					.style('stroke-width', function(d){
						if(d.target.backbone && d.source.backbone){
							return 2.5;
						}
					});
					
				}
		  		var node = svg.append("svg:g").selectAll("g")
			  		.data(graph.nodes)
			  		.enter().append("circle")
			  		.attr("class", "node")
			  		.attr("degree", function(d){
			  			return d["degreeCentrality"]
			  		})
			  		.attr("between", function(d){
			  			return d["betweennessCentrality"];
			  		})
			  		.attr("close", function(d){
			  			return d["closenessCentrality"];
			  		})
			  		.attr("eigen", function(d){
			  			return d["eigenvectorCentrality"]
			  		})
			  		.attr("group", function(d){
			  			return d["group"]
			  		})
			  		.attr("id", function(d){
			  			if(isCitationNetwork){
			  				return d["doi"];
			  			}
			  			return d["name"].replace(/\s+/g, '');
			  		})
			  		.attr("cx", function(d) {
								  			
						return getNodeCoord(centrality, d, score, d.x, width);
		    		})
		        	.attr("cy", function(d) { 
			  			return getNodeCoord(centrality, d, score, d.y, width);
		        	})
			  		.attr("r", function(d){
			  			if(d[centrality] < score || d["degreeCentrality"] === 0){
			  				return 0;
			  			}
			  			else{
			  				return 5;
			  			}
			  		})
			  		.style("fill", function(d){
						var hue = getNodeHue(d[centrality], centrality, isCitationNetwork);
			  			return "hsl("+hue+",100% ,50%)";
			  		})
			  		.on("click", function(d){
			  			if(d[centrality] >= score  || d[centrality] <= 0 ){
			  			
			  				scope.$emit(nodeClicked, {
			  					'name': d['name'],
			  					'id': d['id'],
			  					'centrality': centrality,
			  					'degree': d["degreeCentralityUnnormalized"],
			  					'betweenness': d["betweennessCentrality"],
			  					'closeness': d["closenessCentralityUnnormalized"],
			  					'eigen': d["eigenvectorCentralityUnnormalized"],
			  					'group': d["group"]
			  				});
					        d3.selectAll(".node")
					        	.filter(function(l){
					        		return (l['id']  === d['id']);
					        	})
					        	.attr("r", 9);
					        d3.selectAll(".node")
					        	.filter(function(l){
					        		return (l['id']  !== d['id']);
					        	})
					        	.attr("r", 6);
					        d3.selectAll(".link")
					        	.filter(function(l){
					                 return (l.source.index!==d.index && l.target.index!==d.index);
					             })
					             .style({'stroke-opacity':0.5,'stroke':'#999', 'stroke-width':'1px'});
					     
							d3.selectAll(".link")
								.filter(function(l){
									return (l.source.index===d.index || l.target.index===d.index);
					            })
					            .style({'stroke-opacity':0.8,'stroke':'#F0F', 'stroke-width':'2.5px'});
					        d3.selectAll(".link")
								.filter(function(l){
									return (l.source.backbone && l.target.backbone);
					            })
					            .style({'stroke-opacity':0.8,'stroke':'#0000FF', 'stroke-width':'2.5px'});
					        d3.selectAll(".link")
					        	.filter(function(l){
					        		return (l.source.backbone && l.target.backbone) && (l.source.index===d.index || l.target.index===d.index);
					        	})
					            .style({'stroke-opacity':0.8,'stroke':'url(#grad2)', 'stroke-width':'2.5px'});
				  		}

			  		});
					
			  	node.append("title")
			  		.text(function(d){ 
			  			if(d.doi){
			  				return d.name+"\n Score: "+d[centrality] + "\nYear: " + getYear(d['doi']); 
			  			}
			  			return d.name+"\n Score "+d[centrality]; 
			  		});
			
			    scope.$broadcast("GraphLoaded");
			
			});	
		}, 10);
	}//end drawGraph()

	// Code adapted from http://bl.ocks.org/donaldh/2920551
	this.toggleClustering = function(e, clusters){
		if (e.checked) {
			// We cluster
			var nodes = force.nodes();
			var groups = d3.nest()
				.key(function(d) { return clusters[n.db_id]; })
				.entries(nodes);
			var groupPath = function(d) {
			    return "M" + 
			      d3.geom.hull(d.values.map(function(i) { return [i.x, i.y]; }))
			        .join("L")
			    + "Z";
			};
			var clusterCenters = groups.rollup(function(leaves) {"x": d3.mean(leaves, function(d) { return d.x; }), "y": d3.mean(leaves, function(d) { return d.y; }))});
			force.on("tick", function(e) {
				var k = 6 * e.alpha;
				nodes.forEach(function(node) {
					node.x += (clusterCenters[clusters[n.db_id]].x - node.x) * k;
					node.y += (clusterCenters[clusters[n.db_id]].y - node.y) * k;
				});

			});
			force.start();
		} else {
			// Turn of clustering
			force.on("tick", null);
			force.start();
		}
	}
});