//#!/usr/bin/env phantomjs

var sys = require("system");

function main() {
	if (sys.args.length < 4) {
	    console.log('Usage: screenshot.js <path> <html_filename> <screenshot_filename>');
	    console.log('You passed', sys.args);
	    phantom.exit();
	}
	
	var path = sys.args[1];
	var html = 'file://'+path+'/'+sys.args[2];
	var screenshot = path+'/'+sys.args[3];
	
	console.log("Capturing", html, "as", screenshot);
		
	var page = require('webpage').create();
	page.open(html, function () {
	    page.render(screenshot);
	    console.log("Saved", screenshot);
	    phantom.exit();
	});
}

//main();

var page = require('webpage').create();
page.open("http://yahoo.com", function () {
	setTimeout(function(){
	    page.render("sc.png");
	    console.log("Saved");
	    phantom.exit();
	}, 2000);
});