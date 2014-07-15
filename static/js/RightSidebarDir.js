app.directive("rightSidebar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/RightSidebar.html",
		controller:function($scope, MessageServer){
			$scope.messageServer = MessageServer;
			$scope.messageServer.readNodes();
			$scope.authorPapers = null;
			$scope.rightOpened = false;
			$scope.authorNodes = null;
			$scope.affiliateSelected = function(name){
				var authorObj = "";
				for(var i = 0; i<$scope.authorNodes.length; i++){
					if($scope.authorNodes[i]['name'] === name){
						authorObj = $scope.authorNodes[i]['name'];
						break;
					}
				}
				console.log(name);
			};
			$scope.$watch("messageServer.getNodes()", function(newVal, oldVal){
				$scope.authorNodes = newVal;
			})
			$scope.$on("AuthorNodeClicked", function(event, node){
				console.log(node['id'])
				$scope.$apply(function(){
					$scope.messageServer.queryAuthors(node['id']);
					$scope.authorName = node['name'];
					$scope.centrality = chooseCentrality(node['centrality']);
					$scope.centralityScore = node['score'];
				});
			});
			$scope.$watch("messageServer.getAuthorPapers()", function(queryInfo, oldVal){
				//this is the initialization of the variables
				if(queryInfo === oldVal){
					return;
				}
				$scope.authorPapers = queryInfo['credits'];
				$scope.authorAffiliates = queryInfo['affiliates'];
				if($scope.authorPapers !== null){
					if( !$scope.rightOpened ){
						$scope.rightOpen();
					}
					$scope.rightOpened = true;
				}
				// else{
				// 	$scope.rightOpened = false;
				// }
			});
			$scope.arrowPosition = 100;
			
		},
		link: function(scope, elem, attr){
			
			scope.rightOpen = function(){

				shiftRight = new ShiftBar(98, 1, "left", "#right-container");
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.rightOpened = true;
			};
			scope.rightClose = function(){
				shiftRight = new ShiftBar(90, -1, "left", "#right-container");
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.rightOpened = false;
			};
		}
	}
});