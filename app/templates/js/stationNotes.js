function getStationNotes(id,num){
  $.getJSON("./jsonData/stationNotes.json",function(result){
    var notes = svgCreate('g',{'id':'map'+num+'stationNotes'});
    $(id).append(notes);
    var notes = new Array();
    var notesGeo = new Array();
    for(var prop in result){
      notes.push(prop);
      notesGeo.push(result[prop]);
    }
    for(var i=0;i<notes.length;i++){
      var x = notesGeo[i].split(',')[0];
      var y = notesGeo[i].split(',')[1];
      var text = svgCreate('text',{'font-size':'6px','font-weight':'bold','stroke':'#040404','fill':'#808080','stroke-width':.1,'x':x,'y':y});
      var stationName;
      if(notes[i].indexOf("-")>0){
        stationName = '浦电路';
      }else{
        stationName = notes[i];
      }
      var textData = document.createTextNode(stationName);
      text.append(textData);
      $('#map'+num+'stationNotes').append(text);
    }
//    console.log($('#animate'),$('#linePath'))
  })
}
