var DATA = {};
DATA['settings'] = 'words';

function toggleWords() {
  if (DATA['settings'] == 'words') {DATA['settings'] = '';} else
    {DATA['settings'] = 'words'; console.log(DATA['settings']);}
}

function loadConcept() {

  var concept = '';
  var selection = document.getElementById('selector');
  for (var i=0,sel; sel=selector.options[i]; i++) {
    if (sel.selected) {
      concept = sel.value;
      break;
    }
  }
  
  $.ajax({
   dataType: "json",
   async: false,
   url: 'json/'+concept+'.json',
   success: function(data){console.log('sucess');
     for (key in data) {
       DATA[key] = data[key];
     }}
  });
  
  
  var display = document.getElementById('display');
  
  var queue = DATA['order'];
  var txt = '<ul><li id="E_root" style="list-style:none">{root}</li></ul>';
  
  /* iterate over the queue */
  for (var i=0,name; name=queue[i]; i++) {
    var children = DATA[name]['children'];
    
    if (children.length >= 1) {
      if (DATA[name]['consensus'].length > 0) {
	var rep_string = '';
	rep_string += '<div class="node-wrap" onclick="modifyEdge(\''+name+'\');">';

      	for (var j=0,cns; cns=DATA[name]['consensus'][j]; j++) {
	  if (DATA[name]['retention'][j] == '1') {
	    var symbol = '→ ';
	  }
	  else {
	    var symbol = '* ';
	  }
      	  rep_string += '<div oncontextmenu="showAlignment(event,\''+name+'\','+j+')" class="node-element"><div class="node-name"'
      	    +'>'
      	    +symbol + ' '+DATA[name]['paps'][j]+' '
      	    +'</div><div class="node-content" style="border: 5px solid '+DATA[name]['colors'][j]+'">';
    
	  if (DATA['settings'] == 'words') {
	    rep_string += plotWord(cns.join(' '));
	  }
	  else {
	    rep_string += '';
	  }
	  rep_string += ''
      	    +'</div></div>';
      	}
	rep_string += '</div>';
      }
      else {
	var rep_string = '';
	rep_string += '<div onclick="modifyEdge(\''+name+'\');" class="node-wrap">';
	rep_string += '<div title="'+name+'" class="node-name loss"'
	  + '>'
	  + name
	  + '</div><div class="node-content">';
	rep_string += ''
	  + '</div>'
	  + '</div>';
      }
    }
    else {
      if (DATA[name]['consensus'].length > 0) {
	var rep_string = '';
      	rep_string += '<div class="leaf-wrap" name="'+name+'">';
      	for (var j=0,cns; cns=DATA[name]['consensus'][j]; j++) {
	  if (DATA[name]['retention'][j] == '1') {
	    var symbol = '→ ';
	  }
	  else {
	    var symbol = '* ';
	  }

      	  rep_string += '<div class="leaf-element"><div class="leaf-name">'
      	    +symbol + ' '+name+' ' + DATA[name]['paps'][j] + ' '
      	    +'</div><div class="leaf-content" style="color:white;border:5px solid '+DATA[name]['colors'][j]+'">';
	  if (DATA['settings'] == 'words') {
	    rep_string += plotWord(cns.join(' '));
	  }
	  else {
	    rep_string += '';
	  }
	  rep_string += ''
      	    +'</div></div>';
      	}
      	rep_string += '</div>';
      }
      else {
	var rep_string = '';
	rep_string += '<div class="leaf-wrap" style="border: 2px dotted black;">';
	rep_string += '' 
	  + '<div class="leaf-name loss">'
	  + name 
	  + '</div><div class="leaf-content">';
	rep_string += ' '
	  + '</div>'
	  + '</div>';
      }
    }
    for (var j=0,child; child = children[j]; j++) {
      rep_string += '<ul><li class="node" id="E_'+child+'">{'+child+'}</li></ul>';
    }
    txt = txt.replace('{'+name+'}',rep_string);
  }
  
  /* add concept to header line */
  document.getElementById('header').innerHTML = "Lexical Evolution of &quot;"+concept+'&quot;';
  
  /* add colors */
  var col = document.getElementById('colors');
  var tmp = '';
  for (key in DATA['colors']) {
    tmp += '<div class="colors" style="background-color:'+DATA['colors'][key]+'">'
      + key
      + '</div>';
  }
  col.innerHTML = tmp;
  
  /* submit the display */
  display.innerHTML = txt; 
}

function modifyEdge(name) {
  var edge = document.getElementById('E_'+name);
  for (var i=1,child; child=edge.childNodes[i]; i++) {
    if (child.style.display == 'none') {
      child.style.display = 'block';
    }
    else {
      child.style.display = 'none';
    }
  }
}

function fakeAlert(text){
  var falert = document.createElement('div');
  falert.id = 'fake';
  var text = '<div class="message"><p>' + text + '</p>';
  text += '<div class="btn btn-primary okbutton" onclick="' + "$('#fake').remove(); document.onkeydown = function(event){basickeydown(event)};" + '")> OK </div></div>';
  falert.className = 'fake_alert';

  document.body.appendChild(falert);
  falert.innerHTML = text;
  document.onkeydown = function(event){$('#fake').remove(); document.onkeydown = function(event){basickeydown(event);};};
}

function showAlignment(event,name,idx) {
  event.preventDefault();
  var alms = DATA[name]['alignments'][idx];
  var txt = '<table>';
  for (var i=0,alm; alm=alms[i]; i++) {
    txt += '<th>'+DATA[name]['taxa'][idx][i]+'</th>';
    txt += '<td>'+plotWord(alm.join(' '),'td')+'</td></tr>';
  }
  txt += '</table>';
  fakeAlert(txt);
}

