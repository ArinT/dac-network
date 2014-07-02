app.service("MessageServer", function($http){
	var myNodes = null;
	var authorPapers = null;
	var topFive = null;
	var sent=false;

	this.getNodes = function(){
		return myNodes;
	};

	this.getAuthorPapers = function(){
		return authorPapers;
	};

	this.getTopFive = function(){
		return topFive;
	};

	this.emailSent = function(){
		return sent;
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
		})

		// $http.post("/query_author", myData)
		// 	.success(function(data, status, headers, config){
		// 		if(data !== null){
		// 			authorPapers = data;
		// 		}
				
		// 	})
		// 	.error(function(data, status, headers, config){
		// 		console.log("error");
		// 	});
	};
	this.queryPaper = function(paperId){
		var myData = {'paper_id':paperId};
		$http.post("/query_paper", myData)
			.success(function(data, status, headers, config){
				if(data !== null){
					topFive = data;
				}
				
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};
	/** 
	 *	reads the authors.json file so that when a user searches for an author
	 *	the javascript has an array to filter through.
	 */
	this.readNodes = function(){
		$http.get("../../static/json/authors_centrality.json")
			.success(function(data, status, headers, config){
				myNodes = data.nodes;
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
	}
});
