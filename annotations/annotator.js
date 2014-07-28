var __HR__ = "<hr style='background-color: #333; border: none; height:0.5px;'/>";

$(document).ready(function() {
    console.log("Document fully loaded ...");
    
    // We had the <div> that wil play the role of the tooltip.
    $('body').prepend('<div style="display:none;" class="tooltiptext"><div style="height:400px;"></div></div>');
    
    // We create a unique id for all commentable sections.
    $('p, .ok_ul').each( function(index, value) {
	var item = $(value);
	item.attr('id', CryptoJS.MD5(item.text()).toString());
	
	// We add the comment button and the business logic.
	var commentItem = $('<span style="font-size:12px;"> <i class="fa fa-comments"></i></span>');
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
	
	// We fetch the data from the database.
	
    }); // .each()
    
    
}); // document.ready()


var myDataRef = new Firebase('https://w7h4l3wf4ie.firebaseio-demo.com/nhs-report');
var obj = null;

function showComments(comment_id) {
    console.log("Fetching comment for id=" + comment_id);
    myDataRef.child(comment_id).once('value', function (snapshot) {
	obj = snapshot.val();
	console.log(Object.keys(obj?obj:[]).length +  " comment(s) for this paragraph.");
	console.log(obj);
	
	var content = Object.keys(obj?obj:[]).length +  " comment(s) for this paragraph.";
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
