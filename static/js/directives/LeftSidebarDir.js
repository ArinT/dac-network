jQuery.fn.d3Click = function () {
	console.log("d3click called")
  this.each(function (i, e) {
	console.log("inside each()");
    var evt = document.createEvent("MouseEvents");
    evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);

    e.dispatchEvent(evt);
  });
};
app.directive("leftSidebar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/LeftSidebar.html",
		controller:function($scope, MessageServer, $location){
			$scope.messageServer = MessageServer;
			$scope.messageServer.readNodes();
			$scope.messageServer.readCitationsJson();
			$scope.location = $location;
			$scope.leftOpened = false;
			$scope.arrowPosition = 100;
		
			$scope.searchItemSelected = function(node){
				console.log(node);
				var domId = null;
				if($location.path() === "/citationNetwork"){
					domId = "#" + node.doi;
				}
				else{
					//remove all the spaces in the authors name.
					domId = "#"+ node.name.replace(/\s+/g, '');
				}
				console.log("in left sidebar searchItemSelected()" + domId);
				console.log($(domId));
				// var xLoc = $(domId).attr("cx");
				// var yLoc = $(domId).attr("cy");
				// $("#transformme").attr("position", "2");
				$(domId).d3Click();
				if($location.path() === "/citationNetwork"){
					$scope.messageServer.queryPaper(node.id);
				}
				else{
					$scope.messageServer.queryAuthors(node.id);
				}
			};
		},
		link: function(scope, elem, attr){
			
			scope.leftOpen = function(){

				shiftRight = new ShiftBar(98, 1, "right", "#left-container");
				ShiftBar.prototype.interval = setInterval(function(){
					shiftRight.shift();
				}, 1);
				scope.leftOpened = true;
			};
			scope.leftClose = function(){
				shiftRight = new ShiftBar(85, -1, "right", "#left-container");
				ShiftBar.prototype.interval = setInterval(function(){
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
			$(this.elem).css(side, "98%");
			$(this.elem).css("overflow", "hidden");
			clearInterval(this.interval);
		}
		else if(this.loc <85){
			$(this.elem).css(side, "85%");
			$(this.elem).css("overflow", "auto");
			clearInterval(this.interval);
		}
		else{
			$(this.elem).css(side, ""+this.loc+"%");
			this.loc-=this.val;
		}
	};
}