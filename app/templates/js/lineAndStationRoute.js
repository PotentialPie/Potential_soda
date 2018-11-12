var color_base = 50
var color_range = 300

//绘制地铁路线
function setLinePathRoute(options,r){
  var g = options["g"],
      pathData = options["linePathData"],
      lineName = options["lineName"],
      stationTF = options["stationTF"],
      num = options["mapNum"];
  $("#linePath"+num).html('');//重置
  $("#linearColor"+num).html('');//重置
  for(var i=1;i<g.length+1;i++){
    var pathLine = svgCreate('g',{id:'map'+num+'Line-'+lineName[i-1]});
    $("#linePath"+num).append(pathLine);
    var linearLine = svgCreate('g',{id:'map'+num+'linearLine-'+i});
    $("#linearColor"+num).append(linearLine);
    for(var j=0;j<pathData[i-1].length;j++){
      //设置渐变色
      var linearPath = svgCreate('g',{id:'map'+num+'linearPath'+i+'-'+j});
      $('#map'+num+'linearLine-'+i).append(linearPath);
      var snt = stationTF[i-1][j].split('x')[0];
      var snf = stationTF[i-1][j].split('x')[1];
      var x1 = g[i-1][snt].split(',')[0];
      var y1 = g[i-1][snt].split(',')[1];
      var x2 = g[i-1][snf].split(',')[0];
      var y2 = g[i-1][snf].split(',')[1];
      var strokeColor1 = colorClass(r[snt],color_range,color_base)||'#142f3a';
      var strokeColor2 = colorClass(r[snf],color_range,color_base)||'#142f3a';
      var options = {
        id:'map'+num+'defs-'+i+'-'+j,
        x1:x1,
        y1:y1,
        x2:x2,
        y2:y2,
        c1:strokeColor1,
        c2:strokeColor2
      }
      var defs=createLinear(options);
      linearPath.append(defs);
      var strokeLinear = "url("+'#map'+num+'defs-'+i+'-'+j+")";
      //设置路径属性
      var path = svgCreate('path',{'d':pathData[i-1][j],'stroke':strokeLinear,'stroke-width':2,'fill':'none','id':'map'+num+lineName[i-1]+j,'name':stationTF[i-1][j]});
      $('#map'+num+'Line-'+lineName[i-1]).append(path);
    }
  }
}

//绘制地铁站点
function getStationPassengerRoute(options,r){
  var g = options["g"],
      sit = options["sit"],
      siteName = options["siteName"],
      lineName = options["lineName"],
      num = options["mapNum"];
  $("#sitePoint"+num).html('');//重置
  for(var i=0;i<g.length;i++){
    var fillColor;
    var siteNode = svgCreate('g',{'id':'map'+num+'Sit-'+lineName[i]});
    $("#sitePoint"+num).append(siteNode);
    for(var j = 0;j<sit[i].length;j++){
      var cx = sit[i][j].split(',')[0];
      var cy = sit[i][j].split(',')[1];
      fillColor = colorClass(r[siteName[i][j]],color_range,color_base)||'#446670';
      //设置站点属性
      var circle = svgCreate('circle',{'id':'map'+num+'circle-'+i+'c'+j,'cx':cx,'cy':cy,'r':2.5,'fill':fillColor,'stroke':'#091c22','stroke-width':1,'name':siteName[i][j]});
      $('#map'+num+'Sit-'+lineName[i]).append(circle);
    }
  }
}

//设置站点标记
function stationDomRoute(options){
  var id = options["mapId"],
      num = options["mapNum"],
      g = options["g"],
      sit = options["sit"],
      siteName = options["siteName"],
      lineName = options["lineName"];
  var sitDom = svgCreate('g',{id:'siteDomPoint'+num});
  $(id).append(sitDom);
  for(var i=0;i<g.length;i++){
    var color = 'url(#red_none2)';
    var sitDomNode = svgCreate('g',{'id':'map'+num+'SitDom-'+lineName[i]});
    sitDom.append(sitDomNode);
    for(var j=0;j<sit[i].length;j++){
      var cx = sit[i][j].split(',')[0];
      var cy = sit[i][j].split(',')[1];
      var path = 'M'+cx+','+cy;
      var circleDom = svgCreate('circle',{'id':'map'+num+'circleDom-'+i+'c'+j,'cx':0,'cy':0,'r':3,'fill':'transparent','name':siteName[i][j]});
      sitDomNode.append(circleDom);
      var domPath = svgCreate('animateMotion',{'path':path});
      circleDom.append(domPath);
      $(circleDom).on('click',function(){
        $(this).parents().eq(1).children().find('circle').remove('animateTransform').attr('fill','transparent');
        var domScale = svgCreate('animateTransform',{'attributeName':'transform','type':'scale','from':1,'to':5,'begin':'0','dur':'1s','repeatCount':'indefinite'});
        $(this).attr('fill',color).append(domScale);
      })
    }
  }
}
