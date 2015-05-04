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

app.controller("authorGraphCtrl", ["$scope", "GraphService", function($scope, GraphService){
	$scope.typeGraph = "degreeCentrality";
	$scope.chosenScore = 0;
	$scope.loaded = false;
	$scope.jsonFile = "authors.json";
	$scope.graphService = GraphService;
	console.log($scope.graphService);
	$scope.graphService.setWindowHeight($(window).height());
	$scope.$watch("jsonFile", function(newVal, oldVal){
		if(newVal === oldVal){
			return;
		}
		$scope.$broadcast("NewGraph");
	});
	$scope.$watch("chosenScore", function(val, oldVal){
		if(val !== oldVal){
			$scope.loaded = false;
			$scope.$broadcast("NewGraph");
		}
	});
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
			$scope.graphService.drawGraph($scope, false, $scope.chosenScore, $scope.typeGraph,fileName+$scope.jsonFile, dom, -100, "AuthorNodeClicked");
			
			$scope.$on("NewGraph",function(){
				$("svg").remove();
				$scope.loaded = false;
	  			$scope.graphService.drawGraph($scope, false,  $scope.chosenScore, $scope.typeGraph,fileName+$scope.jsonFile, dom, -100, "AuthorNodeClicked");
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
