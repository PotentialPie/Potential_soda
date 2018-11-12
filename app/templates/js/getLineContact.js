//获得站点之间的链接路径
function getLineContact(options){
  var g = options["g"],
      p = options["p"],
      sit = options["sit"],
      pathData = options["pathData"],
      stationData = options["stationData"],
      siteName = options["siteName"],
      linePathArray = options["linePathArray"],
      stationTF = options["stationTF"];
  for(var i=0;i<g.length;i++){
    //将拐点标记
    $.each(g[i],function(name,geo){
      if(name.indexOf("break")==0){
        p[i].push("L"+g[i][name])
      }else{
        p[i].push(g[i][name])
      }
      if(name.indexOf("break")<0){
        sit[i].push(geo);
        siteName[i].push(name);
      }
    });
    //获取站点之间的来往路径
    for(var j=1;j<p[i].length;j++){
      if(p[i][j].indexOf("L")==0){
        if(p[i][j-1].indexOf("L")<0){
          var forPath = "M"+p[i][j-1]+" "+p[i][j];
          var backPath = " "+p[i][j]+" L"+p[i][j-1];
          var x=1;
          while(p[i][j+x].indexOf("L")==0){
            forPath+=" "+p[i][j+x];
            backPath = " "+p[i][j+x]+backPath;
            x++;
          }
          var fPath = forPath+" L"+p[i][j+x];
          var bPath = "M"+p[i][j+x]+backPath;
          pathData[i].push(fPath);
          pathData[i].push(bPath);
        }
      }else{
        if(p[i][j-1].indexOf("L")<0){
          pathData[i].push("M"+p[i][j-1]+" L"+p[i][j]);
          pathData[i].push("M"+p[i][j]+" L"+p[i][j-1]);
        }
      }
    }
    //获取站点之间的起始点名称
    for(var j = 0;j<siteName[i].length;j++){
      if(j<siteName[i].length-1){
        var ft = siteName[i][j]+'-'+siteName[i][j+1];
        var tf = siteName[i][j+1]+'-'+siteName[i][j];
        var stf = siteName[i][j]+'x'+siteName[i][j+1];
        stationTF[i].push(stf);
        stationData[i].push(ft);
        stationData[i].push(tf);
      }
    }
    //将起始点与对应路径链接
    for(var j=0;j<stationData[i].length;j++){
      linePathArray[i][stationData[i][j]] = pathData[i][j]
    }
  }
}
