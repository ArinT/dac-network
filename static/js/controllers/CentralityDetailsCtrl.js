app.controller("centralityDetailsCtrl", function($scope, $location, $anchorScroll, $route){
	// $route.reload();
	if($location.hash()){
		$anchorScroll();
	}

});