var app = angular.module('CitationNetwork',['ngRoute'], function( $routeProvider){
	$routeProvider.when('/authorNetwork', {templateUrl: '/static/partials/AuthorGraph.html'});
	$routeProvider.when('/citationNetwork', {templateUrl: '/static/partials/CitationGraph.html'});
	$routeProvider.otherwise({redirectTo: '/authorNetwork'});
}).config(function($interpolateProvider, $httpProvider) {
	//this is added because django and angular have similar ways of placing variable on a page
	//angular variable should be used like: {$ myVar $}
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
    //needed to send post requests to django
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

	

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

