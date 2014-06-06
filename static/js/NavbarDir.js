app.directive("mynavbar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/Navbar.html",
		controller:function($scope){
			$scope.searchOption;
			$scope.search=null;
			/* function might submit to back end or filter front end */
			$scope.submitSearch = function(){

			};
		}
	};
});