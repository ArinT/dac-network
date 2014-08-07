app.directive("mynavbar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/Navbar.html",
		controller:function($scope, $rootScope, $location){
			// $scope.searchType = "Search Author";
			$scope.location = $location;
			$scope.search=null;
			$scope.initialLoc = $location.path();
			switch($scope.initialLoc){
				case "/authorNetwork":
					$("#author-tab").toggleClass("active");
					break;
				case "/citationNetwork":
					$("#citation-tab").toggleClass("active");
					break;
				case "/chrono":
					$("#chrono-tab").toggleClass("active");
					break;
				case "/freqplot":
					$("#freq-tab").toggleClass("active");
					break;
				case "/feedback":
					$("#feedback-tab").toggleClass("active");
					break;
				case "/home":
					$("#home-tab").toggleClass("active");
					break;
			}
			$scope.$watch("location.path()", function(newLocation, oldLocation){
				if(newLocation === "/citationNetwork"){
					$scope.searchType = "Search Paper";
				}
				else if(newLocation === "/authorNetwork"){
					$scope.searchType = "Search Author";
				}
				else{
					$scope.searchType = null;
				}
			});
			$rootScope.$watch("search", function(){
				$scope.$broadcast("searching", $scope.search);
				$scope.$emit("searching", $scope.search);
			});

			/* function might submit to back end or filter front end */
			$scope.tabClicked = function(id){
				$rootScope.$broadcast("tabClicked");
				$("li.active").toggleClass("active");
				$("#"+id).toggleClass("active")
			};
		}
	};
});

