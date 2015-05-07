app.controller("clusterSliderCtrl", ["$scope", "$attrs", function($scope, $attrs) {
	$scope.showClusters = false;
	if ($attrs.clusterType === "author") {
		$scope.clusSize = 10;
		$scope.initialClusSize = 10;
		$scope.clusCoef = .99;
		$scope.initialClusCoef = .99;
	} else if ($attrs.clusterType === "citation") {
		$scope.clusSize = 4;
		$scope.initialClusSize = 4;
		$scope.clusCoef = .22;
		$scope.initialClusCoef = .22;
	} else {
		$scope.clusSize = 6;
		$scope.initialClusSize = 6;
		$scope.clusCoef = .5;
		$scope.initialClusCoef = .5;
	}

	$scope.hasChanged = function() {
		if ($scope.clusSize !== $scope.initialClusSize || $scope.clusCoef !== $scope.initialClusCoef) {
			return "active";
		} else {
			return "disabled";
		}
	};

	$scope.buttonPress = function() {
		$scope.initialClusCoef = $scope.clusCoef;
		$scope.initialClusSize = $scope.clusSize;
	};
}]);

app.directive("clusterSlider", function(){
	return {
		replace: "true",
		restrict: "A",
		controller: "clusterSliderCtrl",
		templateUrl: "/static/partials/ClusterSlider.html",
		scope: {},
		link: function(scope, elem, attrs) {
			scope.$on("toggleAuthorClustering", function(event, e) {
				console.log(attrs.clusterType);
				console.log(e);
				if (attrs.clusterType==="author") {
					scope.showClusters = e;
					console.log("Changing!");
				}
				console.log(scope.showClusters);
			});
			scope.$on("toggleCitationClustering", function(event, e) {
				console.log(attrs.clusterType);
				console.log(e);
				if (attrs.clusterType==="citation") {
					scope.showClusters = e;
				}
			});
		}
	}//end return
});