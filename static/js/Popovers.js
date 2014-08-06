$(document).ready(function(){

	$("#degree-popover").popover({'html':true,
								'trigger': 'hover',
								'container':'#degree-popover',
								'placement':'top',
								'title':"Degree Centrality",
								'content': "<div class='box'>The one who has many collaborators is most important. For more information click <a href='/#/authorCitation'>here</a></div>"
							});
	$("#between-popover").popover({'html':true,
								'trigger': 'hover',
								'container':'#between-popover',
								'placement':'top',
								'title':"Betweenness Centrality",
								'content': "<div>Author connecting more authors together is the central actor. For more information click <a href='/#/authorCitation'>here</a></div>"
							});
	$("#closeness-popover").popover({'html':true,
								'trigger': 'hover',
								'container':'#closeness-popover',
								'placement':'top',
								'title':"Closeness Centrality",
								'content':"<div>A central author is characterized by many, short connections to other authors in the networks. For more information click <a href='/#/authorCitation'>here</a></div>"
							});
	$("#eigenvector-popover").popover({'html':true,
								'trigger': 'hover',
								'container':'#eigenvector-popover',
								'placement':'top',
								'title':"Eigenvector Centrality",
								'content': "<div>Maybe not too many neighbors, but if you are connected to important people, you are important! For more information click <a href='/#/authorCitation'>here</a></div>"
							});
	$("#group-popover").popover({'html':true,
								'trigger': 'hover',
								'container':'#group-popover',
								'placement':'top',
								'title':"Group Centrality",
								'content': "<div>Groups of nodes that are clustered together. For more information click <a href='/#/authorCitation'>here</a></div>"
							});
});