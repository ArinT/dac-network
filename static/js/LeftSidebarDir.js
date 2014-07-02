app.directive("leftSidebar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/LeftSidebar.html",
		controller:function($scope, MessageServer){
			$scope.messageServer = MessageServer;
			$scope.leftOpened = false;
			$scope.arrowPosition = 100;
			$scope.postAuthorId = function(id){
				console.log(id);
				$scope.messageServer.queryAuthors(id);
			};
		},
		link: function(scope, elem, attr){
			
			scope.leftOpen = function(){

				shiftRight = new ShiftBar(98, 1, "right", "#left-container");
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.leftOpened = true;
			};
			scope.leftClose = function(){
				shiftRight = new ShiftBar(85, -1, "right", "#left-container");
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.leftOpened = false;
			};
			scope.$on("searching",function(event,search){

				if(search === null || search ==='' ){
					scope.leftClose();
				}
				else{
					if(!scope.leftOpened){
						scope.leftOpen();
					}
				}
			});
		}
	}
});

function ShiftBar(location, value, side, elem) {
	this.orig = location;
	this.elem = elem;
	this.side = side;
	this.loc = location;
	this.val = value;
	this.shift = function(){
		if(this.loc >98){
			// console.log(this.loc);
			$(this.elem).css(side, "98%");
			$(this.elem).css("overflow", "hidden");
			clearInterval(this.interval);
		}
		else if(this.loc <85){
			// console.log(this.loc);
			$(this.elem).css(side, "85%");
			$(this.elem).css("overflow", "auto");
			clearInterval(this.interval);
		}
		else{
			// console.log(""+this.loc+"%");
			$(this.elem).css(side, ""+this.loc+"%");
			this.loc-=this.val;
		}
	};
}