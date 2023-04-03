
const DeviceID = JSON.parse(
    document.getElementById('DeviceID').textContent
  );

const links = JSON.parse(
    document.getElementById('links').textContent
  );

const hosts = JSON.parse(
  document.getElementById('hosts').textContent
);

// let's go for d3

var svg = d3.select("#svg1");
// var width = svg.attr("width");
// var height = svg.attr("height");
var width = 1000;
var height = 1000;
// var width = window.innerWidth;
// var height = window.innerHeight;


nodes = []
DeviceID['devices'].forEach(element => {
    a = { name : element, type : 1}
    nodes.push(a)
});

hosts.forEach(element => {
  a = { name : element['hostID'], type : 2}
  nodes.push(a)
});

links.forEach(element => {
   element['type'] = 1 
});

hosts.forEach(element => {
    a = {"source": element["hostID"], "target": element["DeviceID"], "type":2 }
    links.push(a)
  });


var graph = {
    nodes : nodes,
    links : links
}

var simulation = d3
    .forceSimulation(graph.nodes)
    .force(
      "link",
      d3
        .forceLink()
        .id(function(d) {
          return d.name;
        })
        .links(graph.links)
    )

    .force("charge", d3.forceManyBody().strength(-2000))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", ticked);


  
  var link = svg
    .append("g")
    // .attr("class", "links")
    .attr('stroke-opacity',0.6)
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line")
    .attr("stroke-width", function(d) {
      if (d.type == 1) return 4;
      else return 3;
    })
    .attr("stroke", function(d){
        if (d.type == 1)  return "rgb(19, 218, 201)"
        else return "rgb(19, 218, 19)"
    });


    var imageandtext = svg.append("g")
    .selectAll('g').data(graph.nodes).enter()
    .append('g')
    .call(d3
      .drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
      );



      "https://cdn-icons-png.flaticon.com/512/5761/5761095.png"
    var image = imageandtext
      .append("image")
      .attr("class", 'image')
      .attr("xlink:href", function(d) { 
        
        if(d.type == 1) return "https://cdn-icons-png.flaticon.com/512/5761/5761095.png";
        else return "https://cdn-icons-png.flaticon.com/512/5723/5723238.png"
        
        return})
      .attr("x", -20)
      .attr("y", -20)
      .attr("width", 50)
      .attr("height", 50);
    
      
      var first = 1;
    //  click sur node
      imageandtext.on("click", function(d) {
        // do somthing
        if(first == 1){
          svg
          .append("div")
          .attr("class","info")
          first = 0;
        }
      })


  function ticked() {

    // image.attr("x", d => d.x)
    // image.attr("y", d => d.y)


    // texts.attr("x", d => d.x);
    // texts.attr("y", d => d.y);
    imageandtext.attr("transform",function(d) {
        return "translate("+ d.x + "," + d.y + ")";
    })

    
    link
      .attr("x1", function(d) {
        return d.source.x;
      })
      .attr("y1", function(d) {
        return d.source.y;
      })
      .attr("x2", function(d) {
        return d.target.x;
      })
      .attr("y2", function(d) {
        return d.target.y;
      });

    // node
    //   .attr("cx", function(d) {
    //     return d.x;
    //   })
    //   .attr("cy", function(d) {
    //     return d.y;
    //   });
  }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }