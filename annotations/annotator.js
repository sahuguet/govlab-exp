function fn_NO_COMMENT(size, comment_id) {
    return '<span style="font-size:' +  size + 'px;"> <i id="' + comment_id + '-icon" class="fa fa-comments-o"></i></span>';
};
function fn_OK_COMMENT(size, comment_id) {
    return '<span style="font-size:' +  size + 'px;"> <i id="' + comment_id + '-icon" class="fa fa-comments"></i></span>';
};


var __HR__ = "<hr style='background-color: #333; border: none; height:0.5px;'/>";

var myDataRef = null;
var obj = null;


$(document).ready(function() {
    console.log("Document fully loaded ...");

    

    
    var fb_database = $('#annotator').attr('gl-fb-database');
    console.log("The firebase DB is `" + fb_database + "`.");

    myDataRef = new Firebase(fb_database);

    var annotation_class = $('#annotator').attr('gl-annotation-class');
    console.log("jQuery class of elements to be annotated: `" + annotation_class + "`.");
    console.log("Count: " + $(annotation_class).length + ".");

    // We had the <div> that wil play the role of the tooltip.
    $('body').prepend('<div style="display:none;" class="tooltiptext"><div style="height:400px;"></div></div>');
    
    // We create a unique id for all commentable sections.
    $(annotation_class).each( function(index, value) {
	var item = $(value);
	var comment_id = CryptoJS.MD5(item.text()).toString();  
	item.attr('id', comment_id);
	
	// We add the comment button and the business logic.
	var commentItem = $(fn_NO_COMMENT(12, comment_id));
	commentItem.attr('id', item.attr('id') + '-comment');
	item.append(commentItem);
	commentItem.click(function() { showComments(item.attr('id')); });
	commentItem.qtip({
            content: {
		text: "No comment so far." + __HR__
            },
            hide: {
		event: 'click' 
            },
	    position2: {
		target: 'mouse'
	    }
	}); // .click()
	showComments(comment_id);
	
	
    }); // .each()
    
    
}); // document.ready()

function showComments(comment_id) {
    console.log("Fetching comment for id=" + comment_id);
    myDataRef.child(comment_id).once('value', function (snapshot) {
	obj = snapshot.val();
	var numberOfComments = Object.keys(obj?obj:[]).length;
	
	// We update the icon accordingly.
	$('#' + comment_id + '-icon').removeClass('fa-comments fa-comments-o');
	if (numberOfComments > 0) {
	    $('#' + comment_id + '-icon').addClass('fa-comments');
	} else {
	    $('#' + comment_id + '-icon').addClass('fa-comments-o');
	};

	console.log(numberOfComments +  " comment(s) for this paragraph.");
	console.log(obj);
	
	var content = numberOfComments +  " comment(s) for this paragraph.";
	content += __HR__;
	for( var cid in obj) {
            content += printComment(obj[cid]);
            content += __HR__;
	}
	content += addCommentSection(comment_id);
	$('#' + comment_id + '-comment').qtip('options', 'content.text', content);
    }, function (errorObject) {
	console.log('The read failed: ' + errorObject.code);
    });
}

// TODO: use Moustache templates.
function printComment(comment) {
    // comment = { 'author': 'arnaud', 'ts': Date.now(), 'comment': 'This is a <b>comment</b>.' }
    return "<div>" + comment['comment'] + "<br/>" + "by " + comment['author'] + " at " + comment['ts'] + "</div>";
}


function submitComment(comment_id) {
    console.log("Submitting comment");
    var comment = myDataRef.child(comment_id);
    var content = $('#' + comment_id + '-new').val();
    comment.push({ 'author': 'anonymous', 'ts': Date.now(), 'comment': content });
    console.log("Comment submitted.");
}

function addCommentSection(comment_id) {
    // We create a piece of HTML with corresponding callback to store a comment.
    return '<div><textarea id="' + comment_id + '-new"></textarea><button onclick="submitComment(\'' + comment_id + '\');" type="button">Submit comment</button></div>';
}
