//绘制svg地铁图
function drawSVG(opt) {
	$.getJSON("./jsonData/Underground-geo.json", function(json) {
		var mapId = opt["mapId"];
		var mapNum = opt["mapNum"];
		var isAnimate = opt["animate"];
		var isColor = opt["lineColor"];
		var isError = opt["error"];
		var isStationInfo = opt["stationInfo"];
		var isSetError = opt["setError"];

		//站名列表[{"xx":坐标},{"xx":坐标},{"xx":坐标},...]
		var g = new Array();
		//线路名list['line01','line02',...]
		var lineName = new Array();
		var stationGeo = new Object();

		//读取站名到 g, 线路名到 lineName
		$.each(json, function(i, field) {
			g.push(field["upline"]);
			lineName.push(field["lineName"]);
		});
		//读取各条线路包含的车站到 stationGeo
		//{line01:{{"xx":坐标},{"xx":坐标},{"xx":坐标},...},line02:{{"xx":坐标},{"xx":坐标},{"xx":坐标},...},...}
		for(var i = 0; i < json.length; i++) {
			stationGeo[json[i]["lineName"]] = json[i]["upline"];
			//    if(i<json.length-1){
			//      var name1 = json[i]["lineName"].substring(0,5);
			//      var name2 = json[i+1]["lineName"].substring(0,5);
			//      if(json[i]["lineName"].indexOf('-')&&name1==name2){
			//
			//      }
			//    }
		}

		var sit = new Array();
		var siteName = new Array();
		var p = new Array();
		var pathData = new Array();
		var stationData = new Array();
		var stationTF = new Array();
		var linePathArray = new Object();

		for(var i = 0; i < g.length; i++) {
			sit[i] = new Array();
			siteName[i] = new Array();
			p[i] = new Array();
			pathData[i] = new Array();
			stationData[i] = new Array();
			stationTF[i] = new Array();
			linePathArray[i] = new Object;
		}
		//生成路径
		var options1 = {
			g,
			p,
			sit,
			pathData,
			stationData,
			siteName,
			linePathArray,
			stationTF
		};
		getLineContact(options1);
		//生成地铁路径
		var linePathData = new Array();
		for(var i = 0; i < pathData.length; i++) {
			linePathData[i] = new Array();
			for(var j = 0; j < pathData[i].length; j++) {
				if(j % 2 == 0) {
					linePathData[i].push(pathData[i][j]);
				}
			}
		}
		//svg分组
		var lineGroup = svgCreate('g', {
			id: 'linePath' + mapNum
		});
		$(mapId).append(lineGroup);
		var sitGroup = svgCreate('g', {
			id: 'sitePoint' + mapNum
		});
		$(mapId).append(sitGroup);
		var linearColor = svgCreate('g', {
			id: 'linearColor' + mapNum
		});
		$(mapId).append(linearColor);
		//		//填充内容
		//		//设置移动路径
		//		if(isAnimate) {
		//			animatePath(linePathArray, lineName, mapId, mapNum);
		//		}
		//		//故障显示
		//		if(isError) {
		//			getErrorStation(mapId, stationGeo);
		//		}
		//		//站点信息显示
		//		if(isStationInfo) {
		//			var options = {
		//				mapId,
		//				mapNum,
		//				g,
		//				sit,
		//				siteName,
		//				lineName
		//			};
		//			stationDom(options);
		//			getStationInfo(mapNum);
		//		}
		//		//设置模拟故障
		//		if(isSetError) {
		//			setFaultStation(stationGeo);
		//		}
		//设置站点名
		getStationNotes(mapId, mapNum);
		//绘制地铁路线和地铁站点
		var options2 = {
			g,
			linePathData,
			stationTF,
			lineName,
			mapNum
		};
		var options3 = {
			g,
			sit,
			siteName,
			lineName,
			mapNum
		};
		var options4 = {
			options2,
			options3
		};
		setStationAndColor(options4, isColor);
	})
}