var app = angular.module('CitationNetwork',['ngRoute','ngCookies','ui.slider','ui.bootstrap'], function( $routeProvider){
	$routeProvider.when('/authorNetwork', {templateUrl: '/static/partials/AuthorGraph.html', controller:"authorGraphCtrl"});
	$routeProvider.when('/citationNetwork', {templateUrl: '/static/partials/CitationGraph.html'});
	$routeProvider.when('/staticAuthor', {templateUrl: '/static/partials/StaticAuthorGraph.html'});
	$routeProvider.when('/chrono', {templateUrl: '/static/partials/chronologicalGraph.html'});
	$routeProvider.when('/freqplot', {templateUrl: '/static/partials/freqplot.html'});
	$routeProvider.when('/feedback', {templateUrl: '/static/partials/Feedback.html', controller:"FeedbackCtrl"});
	$routeProvider.otherwise({redirectTo: '/authorNetwork'});
}).run(function($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
}).config(function($interpolateProvider, $httpProvider) {
		//this is added because django and angular have similar ways of placing variable on a page
		//angular variable should be used like: {$ myVar $}
	    $interpolateProvider.startSymbol('{$');
	    $interpolateProvider.endSymbol('$}');
	    //needed to send post requests to django
	    // $httpProvider.defaults.headers.post['X-CSRFToken'] = '{% csrf_token %}'
	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

	});

	
app.controller("myCtrl", ["$rootScope", "$scope", "MessageServer", "$location", function($rootScope, $scope, MessageServer, $location){
	//set a scope varialbe equal to service, so the scope can watch for a change in value.
	$scope.messageServer = MessageServer;
	$scope.messageServer.readNodes();
	$scope.messageServer.readCitationsJson();
	$scope.myLocation = $location;
	$scope.authorNodes = null;
	$scope.citationNodes = null;
	$scope.search = null;
	$scope.openAboutAuthor = false;	
	$scope.showSidebars = true;
	$scope.changeCentrality = function(type){
		console.log(type);
		var temp = "changed";
		$scope.$broadcast(temp);
	}
	$scope.$watch("messageServer.getCitationNodes()", function(newVal, oldVal){
		if($location.path() === "/citationNetwork"){
			$scope.nodes = newVal;
		}
		$scope.citationNodes = newVal;
	});
	$scope.$watch("messageServer.getNodes()", function(newVal, oldVal){
		if($location.path() === "/authorNetwork"){
			$scope.nodes = newVal;
		}
		$scope.authorNodes = newVal;
	});
	$scope.$watch("myLocation.path()", function(url, oldUrl){
		if(url === "/authorNetwork"){
			$scope.showSidebars = true;
			$scope.nodes = $scope.authorNodes;
		}
		else if(url === "/citationNetwork"){
			$scope.showSidebars = true;
			$scope.nodes = $scope.citationNodes;
		}
		else{
			$scope.showSidebars = false;
		}
	});

	$scope.author = null;
	$scope.$on("searching", function(event, search){
		$scope.search = search;
	});
}]);

