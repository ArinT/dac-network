app.controller("FeedbackCtrl", function($scope, MessageServer) {
	$scope.message = null;
	$scope.messageServer = MessageServer;
	$scope.sent = false;
	$scope.sendEmail = function(){
		$scope.messageServer.sendEmail(""+$scope.message);
	};

	$scope.$watch("messageServer.emailSent()", function(newVal, oldVal){
		if(newVal === oldVal){
			return;
		}
		$scope.sent = true;
	});
})