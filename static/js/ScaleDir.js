app.directive("graphScale", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/Scale.html",
		controller: function($scope){
			$scope.hueValue = [];
			$scope.hue2 = [];
			$scope.hue3 = [];
			$scope.hue4 = [];

			for(var i = 0; i <121; i++){
				$scope.hueValue.push(i);
			}

			$scope.setColor = function(hue){
				return { 'background-color': "hsl(" + hue + ",100%,50%)" };
			};
		},
		link: function(scope, elem, attr){

		}
	}
});