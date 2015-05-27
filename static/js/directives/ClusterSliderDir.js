app.controller("clusterSliderCtrl", ["$scope", "$attrs", function($scope, $attrs) {
	$scope.showClusters = false;
	if ($attrs.clusterType === "author") {
		$scope.clusSize = 2;
		$scope.initialClusSize = 2;
		$scope.clusCoef = 1.08;
		$scope.initialClusCoef = 1.08;
	} else if ($attrs.clusterType === "citation") {
		$scope.clusSize = 3;
		$scope.initialClusSize = 3;
		$scope.clusCoef = .91;
		$scope.initialClusCoef = .91;
	} else {
		$scope.clusSize = 2;
		$scope.initialClusSize = 2;
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
		$scope.$emit("clusterParamChange", [$scope.clusCoef, $scope.clusSize, $attrs.clusterType]);
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
				if (attrs.clusterType==="author") {
					scope.showClusters = e;
					if (e === true) {
						scope.$emit("clusterParamChange", [scope.clusCoef, scope.clusSize, attrs.clusterType]);
					}
				}
			});
			scope.$on("toggleCitationClustering", function(event, e) {
				if (attrs.clusterType==="citation") {
					scope.showClusters = e;
					if (e === true) {
						scope.$emit("clusterParamChange", [scope.clusCoef, scope.clusSize, attrs.clusterType]);
						console.log("hi");
					}
				}
			});
		}
	}//end return
});