app.service("MessageServer", function($http){
	var myNodes = null;
	var authorPapers = null;

	this.getNodes = function(){
		return myNodes;
	};
	this.getAuthorPapers = function(){
		return authorPapers;
	};
	this.queryAuthors = function(authorId){
		var myData = {'author_id':authorId};
		$http.post("/query_author", myData)
			.success(function(data, status, headers, config){
				if(data !== null){
					authorPapers = data;
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
		console.log("read nodes called");
		$http.get("../../static/json/authors_centrality.json")
			.success(function(data, status, headers, config){
				myNodes = data.nodes;
				console.log(myNodes[0]);
			})
			.error(function(data, status, headers, config){
				console.log("error");
			});
	};
});