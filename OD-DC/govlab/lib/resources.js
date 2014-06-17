function get_google_doc_data(doc_id){
  var doc_url = "https://docs.google.com/spreadsheet/pub?key=" + doc_id + "&output=csv";
  return $.ajax({
      url: doc_url
  });
}

// For testing, only.
function get_the_data(url){
  var doc_url = "http://sahuguet.com/GovLab/OD-DC/OD-DC-attendees.csv";
  return $.ajax({
      url: doc_url
  });
}



function removeQuotes(str) {
    // Removes `"` at the beginning and the end.
    if (str.search('"') == 0) {
	str = str.substring(1, str.length-1);
    }
    return str;
}

function processQuery(str) {
    var regex = /(\w+[:](?:\w+|["][^"]+["]))|([\w_&#]+|["][^"]+["])/g;
    // group #1 => special operator + content
    //             operator = 1+ character(s)
    // group #2 => regular string
    var filters = { "keywords": [] };
    while (match = regex.exec(str)) {
	var op, content;
	if (match[1]) {
	    op_content = match[1].split(':');
	    op = op_content[0];
	    content = removeQuotes(op_content[1]);
	    if (!(op in filters)) {
		filters[op] = [];
	    }
	    filters[op].push(content);
	};

	if (match[2]) {
	    content = removeQuotes(match[2]);
	    filters['keywords'].push(content);
	}
    }
    return filters;
}

jQuery.fn.dataTableExt.afnFiltering.push(
    
    function( settings, data, dataIndex ) {
	query = $('input[aria-controls="open-data-table"]').val();

	var mapping = $.map($('#open-data-table th'), function(v, i) {return [$(v).text().toLowerCase().replace(/\s+/g, '_'), i];}) ;

	var columns = {};
	for(var i=0; i < mapping.length; i++) {
	    columns[mapping[i]] = mapping[++i];
	}

	filters = processQuery(query);
	for (filter in filters) {
	    if (filter == "keywords") {
		continue;
	    }
	    // We remove tags from the data.
	    var colIndex = columns[filter];
	    the_data = data[colIndex].replace(/<\/?[^>]+(>|$)/g, "");
	    var default_ = false;
	    for (item in filters[filter]) {
		query_term = filters[filter][item];
		default_ = default_ || (the_data.match( new RegExp(query_term, "i")) != null);
	    }
	    if (default_ == false) {
		return false;
	    }
	}
	if (filters['keywords'].length == 0) {
	    return true;
	}
	var default_ = true;
	for (item in filters['keywords']) {
	    query_term = filters['keywords'][item];
	    default_ = default_ && (data.join(" ").match( new RegExp(query_term, "i")) != null);
	};
		
	if (default_ != true) {
	    return false;
	}
	return true;
    }
);

function populate_table(doc_id, table_el, count_el, template, dt_sorting, dt_columns, search_qs){
  //$.when(get_the_data(doc_id)).then(
$.when(get_google_doc_data(doc_id)).then(
    function(csv){
      var json = $.csv.toObjects(csv);
      var data_count = 0;
	console.log(json);
      $.each(json, function(i, obj){
	  obj['test'] = [1,2,3];
          if(obj.title != ""){
            data_count++;
	      $("#" + table_el + " tbody").append(can.view("people-table", obj));
          }
      });

      $('#' + count_el).html(data_count);

      // initialize datatables
      data_table = $('#' + table_el).dataTable( {
        "aaSorting": dt_sorting,
        "aoColumns": dt_columns,
        "bInfo": false,
        "bPaginate": false
      });
      new $.fn.dataTable.FixedHeader(data_table);

	$("div.dataTables_filter input").unbind();
	$("div.dataTables_filter input").keypress(function( event ) {
	    if ( event.which == 13 ) {
		event.preventDefault();
		ga('send', {
		'hitType': 'event',          // Required.
		'eventCategory': 'UI',   // Required.
		'eventAction': 'user search',      // Required.
		'eventLabel': $('#' + table_el + '_filter input').val(),
		'eventValue': 1
	    });
		console.log("Sending GA event.");
	    }
	    

	    data_table.fnFilter("");
	});

	var search_tips = $('<div id="search-tips" style="font-size:60%;">Search operators you can use to filter for a given column: </div>');
	operators = $.map($('#open-data-table th'), function(v, i) {return "<u>" + $(v).text().toLowerCase().replace(/\s+/g, '_') + ":</u>" ;}) ;
	search_tips.append(operators.join("&nbsp;"));
	$('#open-data-table_filter').append(search_tips);

$('input[aria-controls="open-data-table"]').css('width', '400px')

      // allows linking directly to searches
      if ($.address.parameter(search_qs) != undefined) {
        data_table.fnFilter( $.address.parameter(search_qs) );
        $('#' + table_el + '_filter input').ScrollTo();
      }

      // when someone types a search value, it updates the URL
      $('#' + table_el + '_filter input').keyup(function(e){
        $.address.parameter(search_qs, $('#' + table_el + '_filter input').val());
        return false;
      });
    }
  )
}

SHEET_URL = "0AmQp1hhKRsszdC1UMm9tMnJhME1ORUpkRWVjX2NvbXc";
populate_table(SHEET_URL, "open-data-table", "data-count", "people-table", [ [0,'asc'] ], [ null, null, null, null, null ], 'data-search');



