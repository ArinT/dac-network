app.directive("sidebar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/Sidebar.html",
		controller:function($scope){
			$scope.opened = false;
			$scope.arrowPosition = 100;
		},
		link: function(scope, elem, attr){
			scope.open = function(){
				shiftRight = new ShiftBar(0, 1);
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1)
			}
		}
	}
});

function ShiftBar(location, value) {
	this.loc = location;
	this.val = value;
	this.shift = function(){
		if(this.loc >250){
			$(".open-close").css("left", 250);
			clearInterval(this.interval);
		}
		else if(this.loc <0){
			$(".open-close").css("left", 0);
			clearInterval(this.interval);
		}
		else{
			$(".open-close").css("left", this.loc);
			this.loc+=2.5;
		}
	};
}