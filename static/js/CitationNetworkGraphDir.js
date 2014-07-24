app.directive("citationGraph", function(){
	return {
		restrict:"A",
		controller:function($scope, MessageServer){
			$scope.messageServer = MessageServer;
			$scope.typeGraph = "degreeCentrality";
			$scope.chosenScore = 0;
			$scope.loaded = false;
			$scope.highlightPaper = null;
			// $scope.$watch("messageServer.getHighlight()", function(newVal, oldVal){
			// 	var domId = "#" + newVal;
			// 	if(newVal !== oldVal){
			// 		console.log("paperId:"+newVal);
			// 		console.log($(domId));
			// 		$(domId).d3Click();
			// 	}
			// 	console.log("paperId:"+newVal);
			// });
			$scope.$watchCollection('[messageServer.getHighlight(), loaded]', function(newValues, oldValues){
				//if there is a node that should be highlighted, and the graph has loaded
				console.log(newValues[0]);
				console.log(newValues[1]);
				if(newValues[1] === true){
					console.log("got into if statement");
					$(newValues[0]).d3Click();
				}
			});

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
			$scope.$on("GraphLoaded", function(){
				$scope.$apply(function(){
					$scope.loaded = true;
				});
			});
		},
		link:function(scope, elem, attrs){
			var fileName = "../../static/json/citations.json";
			var dom = "#citation-graph";
			drawGraph(scope, true, scope.chosenScore,scope.typeGraph,fileName, dom, -100, "AuthorNodeClicked");
			
			scope.$on("NewGraph",function(){
				$("svg").remove();
	  			drawGraph(scope, true, scope.chosenScore, scope.typeGraph,fileName, dom, -100, "AuthorNodeClicked");
	  		});
			
		}//end link
	}
});
