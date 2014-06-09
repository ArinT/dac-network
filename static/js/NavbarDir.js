app.directive("mynavbar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/Navbar.html",
		controller:function($scope, $rootScope){
			
			$scope.searchOption="author";
			$scope.search=null;
			$rootScope.$watch("search", function(){
				$scope.$broadcast("searching", $scope.search);
				$scope.$emit("searching", $scope.search);
			})
			/* function might submit to back end or filter front end */
			$scope.submitSearch = function(){

			};
		}
	};
});

