//显示站点的信息
//function animateControl(dom,array){
//$(dom).on('click',function(ev){
//  if(dom.indexOf("circle")>=0){
//    var name;
//    if($(dom).attr('name').indexOf("-")>0){
//      name = "宜山路";
//    }else{
//      name = $(dom).attr('name');
//    }
//    var info = name+':'+array[0][name]
//    $("#stationInfoBox").html(info);
//  }
//});
//}

//颜色关系功能
function colorClass(target,num,b){
  var color;
  if(b<target&&target<=num*0.1+b){
    return color = '#CCFF00'
  }else if(num*0.1+b<target&&target<=num*0.2+b){
    return color = '#D2E300'
  }else if(num*0.2+b<target&&target<=num*0.3+b){
    return color = '#D7C600'
  }else if(num*0.3+b<target&&target<=num*0.4+b){
    return color = '#DDAA00'
  }else if(num*0.4+b<target&&target<=num*0.5+b){
    return color = '#E38E00'
  }else if(num*0.5+b<target&&target<=num*0.6+b){
    return color = '#E87100'
  }else if(num*0.6+b<target&&target<=num*0.7+b){
    return color = '#EE5500'
  }else if(num*0.7+b<target&&target<=num*0.8+b){
    return color = '#F43900'
  }else if(num*0.8+b<target&&target<=num*0.9+b){
    return color = '#F91C00'
  }else if(num*0.9+b<target){
    return color = '#FF0000'
  }
}
//生成渐变色的功能
function createLinear(opt){
  var c1 = opt["c1"],
      c2 = opt["c2"],
      x1 = opt["x1"],
      x2 = opt["x2"],
      y1 = opt["y1"],
      y2 = opt["y2"],
      id = opt["id"]
  var defs = svgCreate('defs');
  var dx = Math.abs(x1-x2);
  var dy = Math.abs(y1-y2);
  var zx1 = parseInt(x1);
  var zx2 = parseInt(x2);
  var zy1 = parseInt(y1);
  var zy2 = parseInt(y2);
  var linearGradient;
  if(dx>dy){
    linearGradient = svgCreate('linearGradient',{'id':id,'x1':'0%','y1':'0%','x2':'100%','y2':'0%'});
    if(zx1>zx2){
      linearGradient.append(createStop(c2,c1)["stop1"]);
      linearGradient.append(createStop(c2,c1)["stop2"]);
    }else{
      linearGradient.append(createStop(c1,c2)["stop1"]);
      linearGradient.append(createStop(c1,c2)["stop2"]);
    }
  }else{
    linearGradient = svgCreate('linearGradient',{'id':id,'x1':'0%','y1':'0%','x2':'100%','y2':'0%','gradientTransform':'rotate(90)'});
    if(zy1>zy2){
      linearGradient.append(createStop(c2,c1)["stop1"]);
      linearGradient.append(createStop(c2,c1)["stop2"]);
    }else{
      linearGradient.append(createStop(c1,c2)["stop1"]);
      linearGradient.append(createStop(c1,c2)["stop2"]);
    }
  }
  defs.append(linearGradient);
  return defs;
}
//创建渐变STOP
function createStop(c1,c2){
  var stop1 = svgCreate('stop',{'offset':'0%'});
  $(stop1).attr('stop-color',c1);
  var stop2 = svgCreate('stop',{'offset':'100%'});
  $(stop2).attr('stop-color',c2);
  return {stop1,stop2}
}
//创建svg标签对象的函数
function svgCreate(tag,attrs){
var element = document.createElementNS("http://www.w3.org/2000/svg",tag);
for(var k in attrs){
    var xmlns_xlink;
    if(k.indexOf(":")<0){
      xmlns_xlink = null;
    }else{
      xmlns_xlink = "http://www.w3.org/1999/xlink";
    }
    element.setAttributeNS(xmlns_xlink,k,attrs[k]);
}
return element
}