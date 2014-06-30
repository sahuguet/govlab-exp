// Helper functions

/* {{#split_comma_section Language}}
 *   {{#each .}}{{this}}<br/>{{/each}}
 * {{/split_comma_section}}
 */ 
can.stache.registerHelper('split_comma_section', function(str, options) {
    return options.fn(str.split(","));
});

// Removes `"` at the beginning and the end.
function removeQuotes(str) {
    if (str.search('"') == 0) {
	str = str.substring(1, str.length-1);
    }
    return str;
}

// Populates N-array with default value.
function withDefaultValue(length, defaultValue) {
    var array = new Array(length);
    for (var x=0; x<array.length; x++)
        array[x]=defaultValue;
    return array;
};

// Processes the input text and builds a hashtable of operator -> [ keyword, keyword ].
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

// Adding operator search to the table.
function addSearchOperators(table_id) {
    jQuery.fn.dataTableExt.afnFiltering.push(
	function( settings, data, dataIndex ) {
	    
	    query = $('input[aria-controls="' + table_id + '"]').val();
	    
	    var mapping = $.map($('#' + table_id + ' th'), function(v, i) {return [$(v).text().toLowerCase().replace(/\s+/g, '_'), i];}) ;
	    
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
		    default_ = default_ || (the_data.match( new RegExp("\\b" + query_term, "i")) != null);
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
};    

// This is where the magic happens.
function populate_table(table_id, dt_sorting, search_qs){
    var data_src = $("#" + table_id).attr('data-src');
    var counter_dom = $("#" + table_id + "-count");
    var dt_columns = withDefaultValue($('#' + table_id + ' th').length, null);


    $.when($.ajax({url: data_src})).then(
	function(csv){
	    var json = $.csv.toObjects(csv);
	    var data_count = 0;
	    console.log(json);
	    $.each(json, function(i, obj){
		if(obj.title != ""){
		    data_count++;
		    $("#" + table_id + " tbody").append(can.view(table_id + "-template", obj));
		}
	    });
	    
	    counter_dom.html(data_count);
	    
	    // initialize datatables
	    data_table = $('#' + table_id).dataTable( {
		"aaSorting": dt_sorting,
		"aoColumns": dt_columns,
		"bInfo": false,
		"bPaginate": false
	    });
	    
	    $('td.expandable p').expander({
		slicePoint: 500,
		preserveWords: true,
		expandPrefix: '',
		expandText: ' [...]'
	    });
	    
	    // Floating header; uncomment to turn it on.
	    // new $.fn.dataTable.FixedHeader(data_table);
	    
	    $("div.dataTables_filter input").unbind();
	    $("div.dataTables_filter input").keypress(function( event ) {
		if ( event.which == 13 ) {
		    event.preventDefault();
		    ga('send', {
			'hitType': 'event',                // Required.
			'eventCategory': 'UI',             // Required.
			'eventAction': 'user search',      // Required.
			'eventLabel': $('#' + table_id + '_filter input').val(),
			'eventValue': 1
		    });
		    console.log("Sending GA event.");
		}
		data_table.fnFilter("");
		$counter_dom.html($('#' + table_id + ' tr').length);
	    });
	    
	    var search_tips = $('<div id="' + table_id + '-search-tips" style="font-size:60%;">Search operators you can use to filter for a given column: </div>');
	    operators = $.map($('#' + table_id + ' th'), function(v, i) {return "<u>" + $(v).text().toLowerCase().replace(/\s+/g, '_') + ":</u>" ;}) ;
	    search_tips.append(operators.join("&nbsp;"));
	    $('#' + table_id + '_filter').append(search_tips);
	    
	    $('input[aria-controls="' + table_id + '"]').css('width', '400px')
	    
	    // allows linking directly to searches
	    if ($.address.parameter(search_qs) != undefined) {
		data_table.fnFilter( $.address.parameter(search_qs) );
		$('#' + table_id + '_filter input').ScrollTo();
	    }
	    
	    // when someone types a search value, it updates the URL
	    $('#' + table_id + '_filter input').keyup(function(e){
		$.address.parameter(search_qs, $('#' + table_id + '_filter input').val());
		return false;
	    });

	    addSearchOperators(table_id);
	    
	}
    )
}







