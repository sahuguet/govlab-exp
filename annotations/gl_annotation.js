function injectScript(src) {
    var s = document.createElement("script");
    s.type = "text/javascript";
    s.src = src;
    s.async = false;
    document.head.appendChild(s);
    console.log(src + ' loaded ...');
}

function injectCSS(href) {
   var s = document.createElement("link");
    s.type = "text/css";
    s.rel = "stylesheet"
    s.href = href;
    document.head.appendChild(s);
    console.log(href + ' loaded ...');
}

[
    'http://craigsworks.com/projects/qtip2/packages/nightly/jquery.qtip.css',
    'http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css',
].forEach(injectCSS);

[
    'https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js',
    'http://craigsworks.com/projects/qtip2/packages/nightly/jquery.qtip.js',
    'https://cdn.firebase.com/js/client/1.0.17/firebase.js',
    'https://cdn.firebase.com/v0/firebase-simple-login.js',
    'http://crypto-js.googlecode.com/svn/tags/3.0.2/build/rollups/md5.js',
    'annotator.js'
].forEach(injectScript);

/* Useful references:
- http://www.html5rocks.com/en/tutorials/speed/script-loading/
- 
*/
