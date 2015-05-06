app.directive("rightSidebar", function(){
	return{
		require: "clusterSlider",
		restrict:"E",
		templateUrl:"/static/partials/RightSidebar.html",
		controller:function($scope, $location, $http, MessageServer){
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
			$scope.moreAuthorPapers = true;
			$scope.moreCoAuthors = true;
			$scope.paperAuthorsHolder = [];
			$scope.showAuthorClusters = false;
			$scope.showCitationClusters = false;
			
			$http.get("static/json/author_clusters.json")
				.then(function(res){ $scope.authorClusters = res.data; });
			$http.get("static/json/citation_clusters.json")
				.then(function(res){ $scope.citationClusters = res.data; });

			// angular.element gets the controls, then we call the function on the control
			// Definitely not the angular way, but this makes the most sense design-wise
			$scope.toggleAuthorClustering = function(){
				angular.element($("#author-graph")).scope().toggleClustering($scope.authorClusters);
				$scope.showAuthorClusters = !$scope.showAuthorClusters;
			};
			$scope.toggleCitationClustering = function(){
				angular.element($("#citation-graph")).scope().toggleClustering($scope.citationClusters);
				$scope.showCitationClusters = !$scope.showCitationClusters;
			};

			/*adding similar authors here*/
			$scope.moreSimAuthors = true;
			// #scope.

			$scope.chooseCentrality = function(typeCent){
				if(typeCent === "degreeCentrality"){
					return "Degree";
				}
				if(typeCent === "closenessCentrality"){
					return "Closeness";
				}
				if(typeCent === "betweennessCentrality"){
					return "Betweenness";
				}
				if(typeCent === "eigenvectorCentrality"){
					return "EigenVector";
				}
				if(typeCent === "group"){
					return "Group";
				}
			};

			/* Function used for click.  Sends node to service to tell
				the controllers which node to highlight in the graph. */
			$scope.showPaperInGraph = function(doi){
				$scope.messageServer.setHighlight("#"+doi);
				console.log("#"+doi);
				if($location.path() !== "/citationNetwork"){
					$location.path("/citationNetwork");
				}
			};

			$scope.authorClicked = function(author){
				//remove all the spaces in the authors name
				console.log(author)
				var domId = "#"+ author.name.replace(/\s+/g, '');
				$(domId).d3Click();
			}
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
				// console.log(node);
				//don't need to do $apply, becuase $scope is passed to the function. 
				$scope.messageServer.queryPaper(node['id']);
				$scope.name = node['name'];
				$scope.centrality = $scope.chooseCentrality(node['centrality']);
				$scope.centralityScore = node['score'];
				$scope.degree = node['degree'];
				$scope.betweenness = node['betweenness'];
				$scope.closeness = node['closeness'];
				$scope.eigen = node['eigen'];
				$scope.group  = node['group'];
				
			});
			$scope.$on("AuthorNodeClicked", function(event, node){
				$scope.messageServer.queryAuthors(node['id']);
				$scope.name = node['name'];
				$scope.centrality = $scope.chooseCentrality(node['centrality']);
				$scope.centralityScore = node['score'];
				$scope.degree = node['degree'];
				$scope.betweenness = node['betweenness'];
				$scope.closeness = node['closeness'];
				$scope.eigen = node['eigen'];
				$scope.group  = node['group'];
			});
			$scope.$watch("messageServer.getPaperQueries()", function(newVal, oldVal){
				if(newVal === oldVal){
					return;
				}
				// console.log(newVal)
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
				$scope.selectAmountOfInfo('moreAuthorPapers', 'authorPapers', 'authorPapersHolder', 2);
				$scope.authorAffiliates = queryInfo['affiliates'];
				$scope.selectAmountOfInfo('moreCoAuthors', 'authorAffiliates', 'authorAffiliatesHolder', 2);
				/*adding in similar peers*/
				$scope.similarAuthors = queryInfo['peers'];
				$scope.selectAmountOfInfo('moreSimAuthors', 'similarAuthors', 'simAuthorAffiliatesHolder', 2);

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
			scope.$on("tabClicked", function(){
				if(scope.rightOpened){
					scope.rightClose();
				}
			})
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