//
var viewbox_width = window.screen.width*2;
var viewbox_height = window.screen.height;

var svg = d3.select("svg#data")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0  "+viewbox_width+" "+viewbox_height)
      .classed("svg-content", true);

var width = +svg.node().getBoundingClientRect().width;
var height = +svg.node().getBoundingClientRect().height;

var xoffset = width*0.03; //define horizontal offset of nodes

var legendRectSize = 18,
    legendSpacing = 4,
    duration = 750,
    baseYear = 1990; // Initial year


var uniqueKeys = [];
var color;
var treeData;
var nodes;
var scale;


// load csv
d3.csv(my_url, function(error, _graph) {
  if (error) throw error;

  // Add a fake root node
  _graph.push({
  "ID": "0",
  "ancestor":"",
   "cell type":"PC",
   "year": "1990",
   "URL": ""
  })


  var maxyear = 0;

  var keys = [];
  // Iterate over the dataset
  for(var i =0; i< _graph.length; i++){

    if(_graph[i].year>maxyear){
        maxyear=_graph[i].year;
    }

    keys.push(_graph[i]["cell type"]);

  }

    // make an array with elements baseYear to maxyear at +1 interval
    var yeardata = Array.from({length: maxyear-baseYear}, (x, i) => i+baseYear);

    // Create scale
    scale = d3.scaleLinear()
                  .domain([d3.min(yeardata)*100, 100*(d3.max(yeardata)+1)])
                  .range([0, height/1.5]);


   uniqueKeys = Array.from(new Set(keys)); //get unique keys

    // color scale
    color = d3.scaleOrdinal()
    .domain(uniqueKeys)
    .range(d3.schemeCategory10);


  treeData = d3.stratify()
    .parentId(function (d) { return d["ancestor"];})
    .id(function (d) {return d["ID"];})
    (_graph);


// Assigns parent, children, height, depth
var root = d3.hierarchy(treeData, function(d) { return d.children; });
root.x0 = width/2;
root.y0 = 0;

update(root);

// Collapse the node and all it's children
function collapse(d) {
  if(d.children) {
    d._children = d.children
    d._children.forEach(collapse)
    d.children = null
  }
}

function update(source) {
    // Add scales to axis
    var x_axis = d3.axisRight()
                   .scale(scale)
                   .tickSize(5000)
                   .tickFormat(function(d) { return d/100; });

    var svg_scale = d3.select("svg#data").attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", "0 0  "+viewbox_width+" "+viewbox_height)
            .append("g")
             .attr('class', 'axis')
           .call(x_axis);

   // declares a tree layout and assigns the size
    var treemap = d3.tree().size([height, width]);

  // Assigns the x and y position for the nodes
  var treeData = treemap(root);

  // Compute the new tree layout.
  nodes = treeData.descendants(),
      links = treeData.descendants().slice(1).filter(function(d) {
        //filter out the fake root node links
        return d.data.data.ancestor != 0;
       });


  // Normalize for fixed-depth.
  nodes.forEach(function(d){
     var year = d.data.data.year * 100; // we multiply by 100 here to avoid floats
     if(d.parent!= null){
         if(d.data.data.year==d.parent.data.data.year){
           //if the child was made the same year as a parent, assume it was made 6 months later
           year += 50; // TODO scale this to number of children in the same year
         }
     }
         d.y = scale(year);
         d.x= (d.x*4)+xoffset;
     });

  // ****************** Nodes section ***************************


  // Update the nodes...
  var node = svg.selectAll('g.node')
      .data(nodes, function(d) {return d.id || (d.id = ++i); })
      .style("fill", function(d) {
        //console.log(d.data.data["cell type"])
          return color(d.data.data["cell type"]);
      }).attr("data-legend",function(d) { return d.data.data["cell type"]});

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append('g')
      .attr('class', 'node')
      .attr("transform", function(d) {
        return "translate(" + source.x0 + "," + source.y0 + ")";
    })          .attr("title",function(d) {
            console.log(d.data.data.comment)
          return d.data.data.comment;
      })
         .on("mouseover", mouseover)
    .on("mouseleave", mouseleave)
    .on('click', click);


  // Add Circle for the nodes
  nodeEnter.append('circle')
      .attr('class', 'node')
      .attr('r', 10)
      .style("fill", function(d) {
          return color(d.data.data["cell type"]);
      })
      .attr('cursor', 'pointer');

  // Add labels for the nodes
  nodeEnter.append('text')
      .attr("dy", ".35em")
      .attr("x", function(d) {
          return d.children || d._children ? 10 : 10;
      })
      .attr("text-anchor", function(d) {
          return d.children || d._children ? "start" : "start";
      })
      .text(function(d) {  return d.data.id /*d.data.data.comment;*/ ;})
      .style("transform", function(d) {
        return "rotate(" + 20 + "deg)";
       });


  // UPDATE
  var nodeUpdate = nodeEnter.merge(node);

  // Transition to the proper position for the node
  nodeUpdate.transition()
    .duration(duration)
    .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
     });

    // Open paper in new tab on node click
  function click(d) {
   window.open(d.data.data["URL (OSB/ModelDB/PubMed)"]);
  }


    // function function that change the "tooltip" when user hover / leave a cell
  function mouseover(d) {
    d3.select("span#paperTitle").text(function() { return d.data.data.comment; })
   }

  function mouseleave(d) {
    d3.select("span#paperTitle").text(function() { return ""; })
  }





  // ****************** links section ***************************

  // Update the links...
  var link = svg.selectAll('path.link')
      .data(links, function(d) { if(d.height != "0"){return d.id}; });

  // Enter any new links at the parent's previous position.
  var linkEnter = link.enter().insert('path', "g")
      .attr("class", "link")
      .attr('d', function(d){

        //console.log(source)
        var o = {x: source.x0, y: source.y0}
        return diagonal(o, o)

      });

  // UPDATE
  var linkUpdate = linkEnter.merge(link);

  // Transition back to the parent element position
  linkUpdate.transition()
      .duration(duration)
      .attr('d', function(d){ return diagonal(d, d.parent) });


  // Store the old positions for transition.
  nodes.forEach(function(d){
    d.x0 = d.x;
    d.y0 = d.y;
  });

  // Creates a curved (diagonal) path from parent to the child nodes
  function diagonal(s, d) {

    path = `M ${s.x} ${s.y}
            C ${s.x} ${s.y},
              ${d.x} ${d.y},
              ${d.x+1} ${d.y}`

    return path
  }


}






var legend = d3.select("svg#legend").attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0  "+175+" "+width*0.02).selectAll('.legend')                     // NEW
          .data(uniqueKeys)                                   // NEW
          .enter()                                                // NEW
          .append('g')                                            // NEW
          .attr('class', 'legend')                                // NEW
          .attr('transform', function(d, i) {                     // NEW
            var heightz = legendRectSize + legendSpacing;          // NEW
            var offset =  heightz *uniqueKeys.length / 2;     // NEW
            var horz = legendRectSize;                       // NEW
            var vert = i * heightz;                       // NEW
            return 'translate(' + horz + ',' + vert + ')';        // NEW
          });                                                     // NEW

        legend.append('rect')                                     // NEW
          .attr('width', legendRectSize)                          // NEW
          .attr('height', legendRectSize)                         // NEW
          .style('fill',  function(d, i) {console.log(d); return color(d) })                                   // NEW
          .style('stroke', function(d, i) {console.log(d); return color(d) });                                // NEW

        legend.append('text')                                     // NEW
          .attr('x', legendRectSize + legendSpacing)              // NEW
          .attr('y', legendRectSize - legendSpacing)              // NEW
          .text(function(d) { return d; });                       // NEW


});



// update size-related info on window resize
d3.select(window).on("resize", function(){
    width = +svg.node().getBoundingClientRect().width;
    height = +svg.node().getBoundingClientRect().height;

     viewbox_width = window.screen.width*2;
     viewbox_height = window.screen.height;
    svg.attr("viewBox", "0 0  "+viewbox_width+" "+viewbox_height);
    nodes.forEach(function(d){ d.y =  ((d.data.data.year-1990)*30); d.x= (d.x*2)+xoffset;});

});



