var app = angular.module('CitationNetwork',[]).config(function($interpolateProvider) {
	//this is added because django and angular have similar ways of placing variable on a page
	//angular variable should be used like: {$ myVar $}
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
	});
app.service("GetAuthors", function($http){
	var myNodes = null;
	this.getNodes = function(){
		return myNodes;
	}
	this.readNodes = function(){
		$http.get("../../static/json/author.json")
			.success(function(data, status, headers, config){
				myNodes = data.nodes;
				console.log(myNodes[0]);
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};
});
app.controller("myCtrl", ["$scope", "GetAuthors", function($scope, GetAuthors){
	$scope.getAuthors = GetAuthors;
	$scope.getAuthors.readNodes();
	$scope.nodes = null;
	$scope.search = null;

	$scope.$watch("getAuthors.getNodes()", function(newVal, oldVal){
		$scope.nodes = newVal;
	})
	$scope.author = null;
	$scope.$on("searching", function(event, search){
		$scope.search = search;
	})
	$scope.$on("clicked", function(event, node){
		$scope.author = node.name;
		$scope.$apply();
		console.log($scope.author);
	});
}]);

