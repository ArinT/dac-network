function getAttrCentrality(centrality){
	if(centrality === "degreeCentrality"){
		return "degree";
	}
	if(centrality === "betweennessCentrality"){
		return "between";
	}
	if(centrality === "closenessCentrality"){
		return "close";
	}
	if(centrality === "eigenvectorCentrality"){
		return "eigen";
	}
	if(centrality === "group"){
		return "group";
	}
}

app.controller("authorGraphCtrl", ["$scope", "$http", "GraphService", function($scope, $http, GraphService){
	$scope.typeGraph = "degreeCentrality";
	$scope.chosenScore = 0;
	$scope.filterScore = 0; // repr of last chosenscore actually updated to newgraph
	$scope.loaded = false;
	$scope.jsonFile = "authors.json";
	$scope.graphService = GraphService;
	$scope.graphService.setWindowHeight($(window).height());
	$scope.http = $http;
	$scope.authorCheckboxId = "#authorShowClustering";
	$scope.$watch("jsonFile", function(newVal, oldVal){
		if(newVal === oldVal){
			return;
		}
		$scope.$broadcast("NewGraph");
	});
	$scope.buttonPress = function() {
		if ($scope.filterScore !== $scope.chosenScore) {
			$scope.filterScore = $scope.chosenScore;
			$scope.$broadcast("NewGraph");
			$scope.loaded = false;
		}
	};
	$scope.$watch("typeGraph", function(newVal, oldVal){
		if(newVal !== oldVal){
			$(".node").each(function( index, element ){
				var attr = getAttrCentrality(newVal);
				var centralityScore = $(element).attr(attr);
				var hue = $scope.graphService.getNodeHue(centralityScore, $scope.typeGraph, false);
				if(attr === "group"){
	  				hue = centralityScore * 10;
	  			}
				$(this).css("fill", "hsl(" + hue + ",100% ,50%)");
			});
		}
	});
	$scope.$on("GraphLoaded", function(){
		$scope.$apply(function(){
			$scope.loaded = true;
		});
	});
}]);

app.directive("authorGraph", function(){
	return {
		restrict:"A",
		controller:"authorGraphCtrl",
		link:function(scope, elem, attrs){
			var fileName = "../../static/json/" ;
			var dom = "#author-graph";
			scope.http.get("static/json/author_clusters.json")
				.then(function(res){ scope.clusters = res.data; });
			scope.graphService.drawGraph(scope, false, scope.chosenScore, scope.typeGraph,fileName+scope.jsonFile, dom, -100, "AuthorNodeClicked");
			/*if ($(scope.authorCheckboxId).length !== 0) {
				var checked = $(scope.authorCheckboxId)[0].checked;
				if (checked === true) {
					scope.toggleClustering(scope.clusters);
				}
			}*/
			
			scope.$on("NewGraph",function(){
				$("svg").remove();
				scope.loaded = false;
				console.log(scope.chosenScore);
				console.log(typeof(scope.chosenScore));
				// We can only cluster if we're using a preset dataset, so can't when we filter out some nodes
				if (scope.chosenScore === 0) {
					console.log("wtf");
					scope.graphService.setCanClusterAuthor(true);
					checked = scope.graphService.getAuthorClusteringEnabled();
					if (checked) {
						scope.toggleClustering(scope.clusters, true);
					}
				} else {
					scope.graphService.setCanClusterAuthor(false);
				}
	  			scope.graphService.drawGraph(scope, false,  scope.chosenScore, scope.typeGraph,fileName+scope.jsonFile, dom, -100, "AuthorNodeClicked");
	  		});
		}//end link
	}//end return
});
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
