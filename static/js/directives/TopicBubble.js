app.directive("topicbubble", function(){
  return {
    restrict:"A",
    controller:function($scope){

    },
    link:function(scope, elem, attrs){

      var diameter = 960,
          format = d3.format(",d"),
          color = d3.scale.category20c();

      var bubble = d3.layout.pack()
          .sort(null)
          .size([diameter, diameter])
          .padding(1.5);

      var svg = d3.select("#topicbubble").append("svg")
          .attr("width", 1250)
          .attr("height", 1250)
          .attr("class", "bubble");

      d3.json("../static/json/TopicBubble.json", function(error, root) {
        var node = svg.selectAll(".node")
            .data(bubble.nodes(classes(root))
            .filter(function(d) { return !d.children; }))
          .enter().append("g")
            .attr("class", "node")
            .attr("transform", function(d) { return "translate(" + d.x *1.3+ "," + d.y *1.3 + ")"; });

        node.append("title")
            // .style("font-size", "1px")
            .text(function(d) { return d.className + ": " + format(d.value); });

        node.append("circle")
            .attr("r", function(d) { return d.r *1.3; })
            .each(getSize)
            .style("fill", function(d) { return color(d.packageName); });

        node.append("text")
            .attr("dy", ".3em")
            .attr("stroke","none")
            .style("text-anchor", "middle")
            .style("font-size","12px")
            .text(getText)
            // .attr("fill","black")
            // .style("fill", "black")
            // .css("color", "#000000")
            // .css("background-color", "#000000")
            // .each(getSize)
      });

      // Returns a flattened hierarchy containing all leaf nodes under the root.
      function classes(root) {
        var classes = [];

        function recurse(name, node) {
          if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
          else classes.push({packageName: name, className: node.name, value: node.size});
        }

        recurse(null, root);
        return {children: classes};
      }
      function getText(d) {
        if (d.className.length > 1.5* d.r/3) {
          return d.className.substr(0, 1.5* d.r/4) + "..";
        } else {
          return d.className
        }
      }
      function getSize(d) {
          var bbox = this.getBBox(),
              cbbox = this.parentNode.getBBox(),
              scale = Math.min(cbbox.width/bbox.width, cbbox.height/bbox.height);
          d.scale = scale;
        }
      d3.select(self.frameElement).style("height", diameter + "px");

    }//end link function
  } //end return statement
});