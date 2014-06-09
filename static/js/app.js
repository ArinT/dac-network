var app = angular.module('CitationNetwork',[]).config(function($interpolateProvider) {
	//this is added because django and angular have similar ways of placing variable on a page
	//angular variable should be used like: {$ myVar $}
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
	});
app.service("MessageServer", function($http){
	var myNodes = null;
	var authorInfo = null;

	this.getNodes = function(){
		return myNodes;
	}
	this.queryAuthors = function(authorId){
		console.log("got request");
		$http.post("/query_author",{'author_id':authorId})
			.success(function(data, status, headers, config){
				
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	}
	/** 
	 *	reads the authors.json file so that when a user searches for an author
	 *	the javascript has an array to filter through.
	 */
	this.readNodes = function(){
		console.log("read nodes called");
		$http.get("../../static/json/authors_centrality.json")
			.success(function(data, status, headers, config){
				myNodes = data.nodes;
				console.log(myNodes[0]);
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};
});
app.controller("myCtrl", ["$rootScope", "$scope", "MessageServer", function($rootScope, $scope, MessageServer){
	//set a scope varialbe equal to service, so the scope can watch for a change in value.
	$scope.messageServer = MessageServer;
	$scope.messageServer.readNodes();
	$scope.nodes = null;
	$scope.search = null;
	$scope.openAboutAuthor = false;	

	$scope.$watch("messageServer.getNodes()", function(newVal, oldVal){
		$scope.nodes = newVal;
	})
	$scope.author = null;
	$scope.$on("searching", function(event, search){
		$scope.search = search;
	})
	//this is what will happen when a node on the graph is clicked.
	$scope.$on("clicked", function(event, node){
		$scope.$apply(function(){
			$scope.author = node.name;
			console.log($scope.author);
		});
	});
}]);

