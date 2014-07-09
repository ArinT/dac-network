app.directive("citationGraph", function(){
	return {
		restrict:"A",
		controller:function($scope){
				$scope.typeGraph = "degreeCentrality";
				$scope.chosenScore = 0;
				$scope.loaded = false;
				$scope.$watch("chosenScore", function(val, oldVal){
					if(val !== oldVal){
						$scope.$broadcast("NewGraph");
					}
				});
				$scope.$watch("typeGraph", function(newVal, oldVal){
					console.log($scope.typeGraph)
					if(newVal !== oldVal){
						$scope.$broadcast("NewGraph");
					}
				});
				$scope.$on("GraphLoaded", function(){
					$scope.$apply(function(){
						$scope.loaded = true;
					});
				});
		},
		link:function(scope, elem, attrs){
			var fileName = "../../static/json/citations.json";
			var dom = "#citation-graph";
			drawGraph(scope, scope.chosenScore,scope.typeGraph,fileName, dom, -100, "AuthorNodeClicked");
			
			scope.$on("NewGraph",function(){
				$("svg").remove();
	  			drawGraph(scope, scope.chosenScore, scope.typeGraph,fileName, dom, -100, "AuthorNodeClicked");
	  		});
			
		}//end link
	}
});
