app.directive("rightSidebar", function(){
	return{
		restrict:"E",
		templateUrl:"/static/partials/RightSidebar.html",
		controller:function($scope, $location, MessageServer){
			$scope.messageServer = MessageServer;
			$scope.messageServer.readNodes();
			$scope.authorPapers = null;
			$scope.rightOpened = false;
			$scope.authorNodes = null;
			$scope.viewNumber = 2;
			$scope.moreAuthors = true;
			$scope.moreCited = true;
			$scope.moreCites = true;
			$scope.moreSimilarPapers = true;
			$scope.paperAuthorsHolder = [];
			/* Function used for click.  Sends node to service to tell
				the controllers which node to highlight in the graph. */
			$scope.showPaperInGraph = function(doi){
				$scope.messageServer.setHighlight("#"+doi);
				if($location.path() !== "/citationNetwork"){
					$location.path("/citationNetwork");
				}
			};

			$scope.viewAuthorPapers = function(numberOfPapers){
				var retVal = [];
				if($scope.authorPapers !== null){
					for(var i = 0; i<numberOfPapers; i++){
						//not all people have written two papers
						if($scope.authorPapers[i]){
							retVal.push($scope.authorPapers[i]);
						}
					}
				}
				return retVal;
			};
			$scope.selectAmountOfInfo = function(showConditional, original, holder, amount){
				// $scope.viewNumber = $scope.authorPapers.length;
				if(amount){
					$scope[holder] = [];
					for(var i = 0; i < amount; i++){
						$scope[showConditional] = true;
						if($scope[original][i]){
							$scope[holder].push($scope[original][i]);
						}
					}
				}
				else{
					$scope[showConditional] = false;
					$scope[holder] = $scope[original];
				}
			};
			$scope.hidePapers = function(){
				$scope.viewNumber = 2;
			}
			$scope.affiliateSelected = function(name){
				var authorObj = "";
				for(var i = 0; i<$scope.authorNodes.length; i++){
					if($scope.authorNodes[i]['name'] === name){
						authorObj = $scope.authorNodes[i]['name'];
						break;
					}
				}
			};
			$scope.$watch("messageServer.getNodes()", function(newVal, oldVal){
				$scope.authorNodes = newVal;
			});
			$scope.$on("CitationNodeClicked", function(event, node){
				console.log(node);
				$scope.$apply(function(){
					$scope.messageServer.queryPaper(node['id']);
					$scope.name = node['name'];
					$scope.centrality = chooseCentrality(node['centrality']);
					$scope.centralityScore = node['score'];
					$scope.degree = node['degree'];
					$scope.betweenness = node['betweenness'];
					$scope.closeness = node['closeness'];
					$scope.eigen = node['eigen'];
					$scope.group  = node['group'];
				});
			});
			$scope.$on("AuthorNodeClicked", function(event, node){
				$scope.$apply(function(){
					$scope.messageServer.queryAuthors(node['id']);
					$scope.name = node['name'];
					$scope.centrality = chooseCentrality(node['centrality']);
					$scope.centralityScore = node['score'];
					$scope.degree = node['degree'];
					$scope.betweenness = node['betweenness'];
					$scope.closeness = node['closeness'];
					$scope.eigen = node['eigen'];
					$scope.group  = node['group'];
				});
			});
			$scope.$watch("messageServer.getPaperQueries()", function(newVal, oldVal){
				if(newVal === oldVal){
					return;
				}
				console.log(newVal)
				$scope.paperAuthors = newVal['authors'];
				$scope.selectAmountOfInfo('moreAuthors', 'paperAuthors', 'paperAuthorsHolder', 2);
				$scope.paperCited = newVal['cited'];
				$scope.selectAmountOfInfo('moreCited', 'paperCited', 'paperCitedHolder', 2);
				$scope.paperCites = newVal['cites'];
				$scope.selectAmountOfInfo('moreCites', 'paperCites', 'paperCitesHolder', 2);
				$scope.similarPapers = newVal['similar_papers'];
				$scope.selectAmountOfInfo('moreSimilarPapers', 'similarPapers', 'similarPapersHolder', 2);
				if( !$scope.rightOpened ){
					$scope.rightOpen();
				}
				$scope.rightOpened = true;
			});
			$scope.$watch("messageServer.getAuthorQueries()", function(queryInfo, oldVal){
				//this is the initialization of the variables
				if(queryInfo === oldVal){
					return;
				}
				$scope.authorPapers = queryInfo['credits'];
				$scope.authorAffiliates = queryInfo['affiliates'];
				if($scope.authorPapers !== null){
					if( !$scope.rightOpened ){
						$scope.rightOpen();
					}
					$scope.rightOpened = true;
				}
			});
			$scope.arrowPosition = 100;
			
		},
		link: function(scope, elem, attr){
			
			scope.rightOpen = function(){

				shiftRight = new ShiftBar(98, 1, "left", "#right-container");
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.rightOpened = true;
			};
			scope.rightClose = function(){
				shiftRight = new ShiftBar(90, -1, "left", "#right-container");
				ShiftBar.prototype.interval = setInterval(function(){
					// console.log(shiftRight.loc);
					shiftRight.shift();
				}, 1);
				scope.rightOpened = false;
			};
		}
	}
});