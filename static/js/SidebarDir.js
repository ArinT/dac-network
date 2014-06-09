app.directive("sidebar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/Sidebar.html",
		controller:function($scope, MessageServer){
			$scope.messageServer = MessageServer;
			$scope.opened = false;
			$scope.arrowPosition = 100;
			$scope.postAuthorId = function(id){
				$scope.messageServer.queryAuthors(id);
			};
		},
		link: function(scope, elem, attr){
			
			scope.open = function(){

				shiftRight = new ShiftBar(99.5, 1);
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.opened = true;
			};
			scope.close = function(){
				shiftRight = new ShiftBar(85, -1);
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.opened = false;
			};
			scope.$on("searching",function(event,search){
				if(search === null || search ==='' ){
					scope.close();
				}
				else{
					scope.open();
				}
			});
		}
	}
});

function ShiftBar(location, value) {
	this.loc = location;
	this.val = value;
	this.shift = function(){
		if(this.loc >99.5){
			// console.log(this.loc);
			$(".container").css("right", "99.5%");
			$(".container").css("overflow", "hidden");
			clearInterval(this.interval);
		}
		else if(this.loc <85){
			// console.log(this.loc);
			$(".container").css("right", "85%");
			$(".container").css("overflow", "auto");
			clearInterval(this.interval);
		}
		else{
			// console.log(""+this.loc+"%");
			$(".container").css("right", ""+this.loc+"%");
			this.loc-=this.val;
		}
	};
}