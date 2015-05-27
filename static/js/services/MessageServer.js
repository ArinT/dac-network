app.service("MessageServer", function($http){
	var myNodes = null;
	var citationNodes = null;
	var authorPapers = null;
	var paperQueries = null;
	var sent = false;
	var highlight = null;
	var clusters = null;
	var myData;
	// var similarAuthors = null;

	this.getCitationNodes = function(){
		return citationNodes;
	};

	this.getNodes = function(){
		return myNodes;
	};

	this.getAuthorQueries = function(){
		return authorPapers;
	};

	this.getPaperQueries = function(){
		return paperQueries;
	};

	this.emailSent = function(){
		return sent;
	};

	this.getHighlight = function(){
		if( $(highlight).length ){
			return highlight;
		}
		else{
			return null;
		}
	};

	this.getClusters = function() {
		return clusters;
	}

	this.queryAuthors = function(authorId){
		var myData = {'author_id':authorId};
		var csrf = "{% csrf_token %}"
		$http({
			method: 'POST',
			url: "/query_author",
			data:myData,
			headers:{'X-CSRFToken': csrf}
		}).success(function(data, status, headers, config){
			authorPapers = data;
		}).error(function(data, status, headers, config){
			console.log("error");
			console.log(data, status);
		})
	};
	this.queryPaper = function(paperId){
		var myData = {'paper_id':paperId};
		$http.post("/query_paper", myData)
			.success(function(data, status, headers, config){
				if(data !== null){
					paperQueries = data;
				}
				
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};
	this.queryClusters = function(clusSize, clusCoef, graphType, upToYear){
		myData = {
			"clusSize" : clusSize,
			"clusCoef" : clusCoef,
			"graphType" : graphType
		}
		if (upToYear !== null) {
			myData["upToYear"] = upToYear;
		}

		$http.post("/get_clusters", myData)
			.success(function(data, status, headers, config){
				if(data !== null){
					clusters = data;
				}
				
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};
	this.queryClustersYearUpdate = function(upToYear) {
		this.queryClusters(myData.clusSize, myData.clusCoef, myData.graphType, upToYear);
	};
	/** 
	 *	reads the authors.json file so that when a user searches for an author
	 *	the javascript has an array to filter through.
	 */
	this.readNodes = function(){
		$http.get("../../static/json/authors.json")
			.success(function(data, status, headers, config){
				myNodes = data.nodes;
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};

	this.readCitationsJson = function(){
		$http.get("../../static/json/citations.json")
			.success(function(data, status, headers, config){
				citationNodes = data.nodes;
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};

	this.sendEmail = function(msg){
		$http.post("/send_email", {'message': msg})
			.success(function(data, status, headers, config){
				if(data.success){
					sent = true;
					console.log("email response came back")
				}
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};

	this.setHighlight = function(doi){
		highlight = doi;
	};
});
