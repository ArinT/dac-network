var app = angular.module('CitationNetwork',[]).config(function($interpolateProvider) {
	//this is added because django and angular have similar ways of placing variable on a page
	//angular variable should be used like: {$ myVar $}
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
	});

