app.directive("mynavbar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/Navbar.html",
		controller:function($scope, $rootScope, $location){
			// $scope.searchType = "Search Author";
			$scope.location = $location;
			$scope.search=null;
			$scope.$watch("location.path()", function(newLocation, oldLocation){
				if(newLocation === "/citationNetwork"){
					$scope.searchType = "Search Paper";
				}
				else if(newLocation === "/authorNetwork"){
					$scope.searchType = "Search Author";
				}
				else{
					$scope.searchType = "Search";
				}
			});
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

