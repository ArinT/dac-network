app.directive("chrono", function(){
  return {
    restrict:"A",
    controller:function($scope){
      $scope.graphColor = "blue";
      //when watching a variable, on first visit to page it thinks the variable changes when we it doesnt
      $scope.firstVisit = true;
    },
    link:function(scope, elem, attrs){
      scope.$watch("graphColor", function(){
        if(scope.firstVisit){
          scope.firstVisit = false;
        }
        else{
          console.log("changed")
          $("svg").remove();
          $(".remove").remove();
          chart("../static/csv/chronological_array_top100.csv", scope.graphColor);
        }
      });
      chart("../static/csv/chronological_array_top100.csv", "blue");

      var datearray = [];
      var colorrange = [];


      function chart(csvpath, color) {

      if (color == "blue") {
        colorrange = ["#045A8D", "#2B8CBE", "#74A9CF", "#A6BDDB", "#D0D1E6", "#F1EEF6"];
      }
      else if (color == "pink") {
        colorrange = ["#980043", "#DD1C77", "#DF65B0", "#C994C7", "#D4B9DA", "#F1EEF6"];
      }
      else if (color == "orange") {
        colorrange = ["#B30000", "#E34A33", "#FC8D59", "#FDBB84", "#FDD49E", "#FEF0D9"];
      }
      strokecolor = colorrange[0];


      var margin = {top: 20, right: 40, bottom: 30, left: 30};
      var width = document.body.clientWidth - margin.left - margin.right;
      var height = 400 - margin.top - margin.bottom;

      var tooltip = d3.select("#chrono")
          .append("div")
          .attr("class", "remove")
          .style("position", "relative")
          .style("z-index", "20")
          .style("visibility", "hidden")
          .style("top", "30px")
          .style("left", "55px");

      var x = d3.time.scale()
          .range([0, width]);
      var getx = d3.time.scale();

      var y = d3.scale.linear()
          .range([height-10, 0]);

      var z = d3.scale.ordinal()
          .range(colorrange);
      var formatAxis = d3.format("  0");
      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom")
          .tickFormat(formatAxis)
          .ticks(11)
          .tickValues([2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012]);

      var yAxis = d3.svg.axis()
          .scale(y);

      var yAxisr = d3.svg.axis()
          .scale(y);

      var stack = d3.layout.stack()
          .offset("silhouette")
          .values(function(d) { return d.values; })
          .x(function(d) { return d.date; })
          .y(function(d) { return d.value; });

      var nest = d3.nest()
          .key(function(d) { return d.key; });

      var area = d3.svg.area()
          .interpolate("cardinal")
          .x(function(d) { return x(d.date); })
          .y0(function(d) { return y(d.y0); })
          .y1(function(d) { return y(d.y0 + d.y); });

      var svg = d3.select("#chrono").append("svg")
          // .attr("width", width + margin.left + margin.right)
          // .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var graph = d3.csv(csvpath, function(data) {
        data.forEach(function(d) {
          d.value = +d.value;
        });

        var layers = stack(nest.entries(data));

        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) { return d.y0 + d.y; })]);

        svg.selectAll(".layer")
            .data(layers)
          .enter().append("path")
            .attr("class", "layer")
            .attr("d", function(d) { return area(d.values); })
            .style("fill", function(d, i) { return z(i); });


        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + width + ", 0)")
            .call(yAxis.orient("right"));

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis.orient("left"));

        svg.selectAll(".layer")
          .attr("opacity", 1)
          .on("mouseover", function(d, i) {
            svg.selectAll(".layer").transition()
            .duration(250)
            .attr("opacity", function(d, j) {
              return j != i ? 0.6 : 1;
          })})

          .on("mousemove", function(d, i) {
            mousex = d3.mouse(this);
            mousex = mousex[0];
            var invertedx = getx(mousex);
      	
            mousedate = Math.floor(invertedx/width*11+2002);
            v = (d.values);
            r = 0;
            for (var k = 0; k < v.length; k++){
          		if (v[k].date == mousedate){
          			r = v[k].value;
          		}
          	}
            
            d3.select(this)
            .classed("hover", true)
            .attr("stroke", strokecolor)
            .attr("stroke-width", "0.5px"),
            tooltip.html( "<p>" + d.key + "<br>" + r + "<br>"+ mousedate + "</p>" ).style("visibility", "visible");

          })
          .on("mouseout", function(d, i) {
           svg.selectAll(".layer")
            .transition()
            .duration(250)
            .attr("opacity", "1");
            d3.select(this)
            .classed("hover", false)
            .attr("stroke-width", "0px"), tooltip.html( "<p>" + d.key + "<br>" + d.value + "<br>"+ d.date+ "</p>" ).style("visibility", "hidden");
        })

        var vertical = d3.select(".chart")
              .append("div")
              .attr("class", "remove")
              .style("position", "absolute")
              .style("z-index", "19")
              .style("width", "1px")
              .style("height", "380px")
              .style("top", "10px")
              .style("bottom", "30px")
              .style("left", "0px")
              .style("background", "#fff");

        d3.select(".chart")
            .on("mousemove", function(){
               mousex = d3.mouse(this);
               mousex = mousex[0] + 5;
               vertical.style("left", mousex + "px" )})
            .on("mouseover", function(){
               mousex = d3.mouse(this);
               mousex = mousex[0] + 5;
               vertical.style("left", mousex + "px")});
      });
    }
}
}
});
