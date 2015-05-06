app.controller("clusterSliderCtrl", ["$scope", "$attrs", function($scope, $attrs) {
	if ($attrs.clusterType==="author") {
		$scope.clusSize=10;
		$scope.clusCoef=.99;
	} else if ($attrs.clusterType==="citation") {
		$scope.clusSize=4;
		$scope.clusCoef=.22;
	} else {
		$scope.clusSize=6;
		$scope.clusCoef=.5;
	}
}]);

app.directive("clusterSlider", function(){
	return {
		replace: "true",
		restrict: "A",
		controller: "clusterSliderCtrl",
		templateUrl: "/static/partials/ClusterSlider.html"
	}//end return
});