app.controller("authorGraphCtrl", function($scope){
	$scope.typeGraph = "degreeCentrality";
	$scope.chosenScore = 0.2;
	$scope.popoverBody = "<a href='#'>hello</a>"
	$scope.$watch("chosenScore", function(val, oldVal){
		if(val !== oldVal){
			$scope.$broadcast("NewGraph");
		}
	});
	$scope.$watch("typeGraph", function(newVal, oldVal){
		if(newVal !== oldVal){
			$scope.$broadcast("NewGraph");
		}
	});
});

app.directive("authorGraph", function(){
	return {
		restrict:"A",
		controller:"authorGraphCtrl",
		link:function(scope, elem, attrs){
			var fileName = "../../static/json/authors_centrality.json";
			var dom = "#author-graph";
			drawGraph(scope, scope.chosenScore,"degreeCentrality",fileName, dom, -100, "AuthorNodeClicked");
			scope.$on("NewGraph",function(){
				$("svg").remove();
	  			drawGraph(scope, scope.chosenScore, scope.typeGraph,fileName, dom, -100, "AuthorNodeClicked");
	  		});
		}//end link
	}//end return
});
function chooseCentrality(typeCent){
	if(typeCent === "degreeCentrality"){
		return "degree";
	}
	if(typeCent === "closenessCentrality"){
		return "closeness";
	}
	if(typeCent === "betweennessCentrality"){
		return "betweenness";
	}
}//end chooseCentrality()

