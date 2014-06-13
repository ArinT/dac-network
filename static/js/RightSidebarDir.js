app.directive("rightSidebar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/RightSidebar.html",
		controller:function($scope, MessageServer){
			$scope.messageServer = MessageServer;
			$scope.authorPapers = null;
			$scope.rightOpened = false;
			$scope.$watch("messageServer.getAuthorPapers()", function(newVal, oldVal){
				$scope.authorPapers = newVal;
				if($scope.authorPapers !== null){
					$scope.rightOpened = true;
					$scope.rightOpen();
				}
				else{
					$scope.rightOpened = false;
				}
			});
			// $scope.messageServer = MessageServer;
			$scope.arrowPosition = 100;
			// $scope.postAuthorId = function(id){
			// 	$scope.messageServer.queryAuthors(id);
			// };
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