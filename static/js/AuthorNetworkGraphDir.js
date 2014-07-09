app.controller("authorGraphCtrl", function($scope){
	$scope.typeGraph = "degreeCentrality";
	$scope.chosenScore = 0;
	$scope.loaded = false;
	$scope.$watch("chosenScore", function(val, oldVal){
		if(val !== oldVal){
			$scope.loaded = false;
			$scope.$broadcast("NewGraph");
		}
	});
	$scope.$watch("typeGraph", function(newVal, oldVal){
		if(newVal !== oldVal){
			$scope.loaded = false;
			$scope.$broadcast("NewGraph");
		}
	});
	$scope.$on("GraphLoaded", function(){
		$scope.$apply(function(){
			$scope.loaded = true;
		});
	});
});

app.directive("authorGraph", function(){
	return {
		restrict:"A",
		controller:"authorGraphCtrl",
		link:function(scope, elem, attrs){
			var fileName = "../../static/json/authors.json";
			var dom = "#author-graph";
			drawGraph(scope, scope.chosenScore,scope.typeGraph,fileName, dom, -100, "AuthorNodeClicked");
			
			scope.$on("NewGraph",function(){
				$("svg").remove();
	  			drawGraph(scope, scope.chosenScore, scope.typeGraph,fileName, dom, -100, "AuthorNodeClicked");
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