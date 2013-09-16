// HTTP Trace Capture
// Author: Shauvik Roy Choudhary (shauvik@gatech.edu)
// Some code re-used from the Open source Live Headers extension sample
// License: BSD style
// Copyright (c) 2012 The Chromium Authors. All rights reserved.

var tabId = parseInt(window.location.search.substring(1));
var iPhoneUA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3';

window.addEventListener("load", function() {
  chrome.debugger.sendCommand({tabId:tabId}, "Network.enable"); 
  chrome.debugger.onEvent.addListener(onEvent);

  chrome.tabs.onUpdated.addListener(function(updatedTabId, changeInfo) {
    if ((updatedTabId==tabId) && (changeInfo.status === 'complete')) {
      //alert("tab:"+updatedTabId+" updated. Change:"+JSON.stringify(changeInfo));
      var logDiv = document.createElement("div");
      logDiv.className = "event";
      //logDiv.textContent = "Tab Updated";
      document.getElementById("container").appendChild(logDiv);

      var fName = new Date().getTime();
      var logLine = document.createElement("div");
      logLine.textContent = '"PAGEUPDATE": '+fName+',';
      logDiv.appendChild(logLine);

      chrome.pageCapture.saveAsMHTML({tabId:tabId}, function(mhtmlData){        
        saveAs(mhtmlData,"_"+fName+".dat");
      });

    }
  });

  chrome.webRequest.onBeforeSendHeaders.addListener(
    function(details) { 
      if(document.getElementById('br_mobile').checked) {
        for (var i = 0; i < details.requestHeaders.length; ++i) {
          if (details.requestHeaders[i].name === 'User-Agent') { 
            details.requestHeaders[i].value = iPhoneUA;
            //details.requestHeaders.splice(i, 1);
            break;
          }
        }
        return {requestHeaders: details.requestHeaders};
      }
    },
    {urls: ["<all_urls>"]},
    ["blocking", "requestHeaders"]);

  chrome.runtime.onMessage.addListener(function(n, t, i) {
    if(document.getElementById('br_mobile').checked) {
      i({
          userAgent: iPhoneUA
      })
    } else {
      i({})
    }
  });

  setUp();
});

window.addEventListener("unload", function() {
  chrome.debugger.detach({tabId:tabId});
});

var requests = {};

function newDiv(text, parent) {
  var newDiv = document.createElement("div");
  newDiv.textContent = text;
  if(parent) {
    parent.appendChild(newDiv);  
  }
  return newDiv;
}

function onEvent(debuggeeId, message, params) {
  if (tabId != debuggeeId.tabId)
    return;

  if (message == "Network.requestWillBeSent") {
    var requestDiv = requests[params.requestId];
    if (!requestDiv) {
      var requestDiv = document.createElement("div");
      requestDiv.className = "request";
      requestDiv.id = params.requestId;
      requests[params.requestId] = requestDiv;
      var urlLine = document.createElement("div");
      urlLine.textContent = '"REQUEST": "'+params.request.url+'",';
      requestDiv.appendChild(urlLine);
    }

    // We don't care about redirects as of now
    if (params.redirectResponse)
      appendResponse(params.requestId, params.redirectResponse);

    var requestLine = document.createElement("div");
    requestLine.textContent = '\n"details": "' + params.request.method + ' ' +
        parseURL(params.request.url).path + ' HTTP/1.1",';
    requestDiv.appendChild(requestLine);

    //console.log(params.request.method);
    if(params.request.method == 'POST') {
      var postData = document.createElement("div");
      postData.textContent = '"post_data": "'+encodeURIComponent(params.request.postData)+'",';
      requestDiv.appendChild(postData);
    }

    document.getElementById("container").appendChild(requestDiv);
  } else if (message == "Network.responseReceived") {
    appendResponse(params.requestId, params.response);
  } else {
    


    //var logDiv = document.createElement("div");
    //logDiv.textContent = "Message: "+message;
    //document.getElementById("container").appendChild(logDiv);
  }
}

function appendResponse(requestId, response) {
  var requestDiv = requests[requestId];

  // Ignore headersactivity
  //requestDiv.appendChild(formatHeaders(response.requestHeaders));

  var mimeType = "";
  if(response.mimeType) {
    mimeType = response.mimeType;
  }

  var statusLine = document.createElement("div");
  statusLine.textContent = '\n"RESPONSE": "' + response.status + ' ' +
    response.statusText + ', '+mimeType+'",';
  requestDiv.appendChild(statusLine);

  // Ignore response headers
  //requestDiv.appendChild(formatHeaders(response.headers));

}


function showNotification(msg) {
  var output = document.getElementById('output');
  output.textContent = msg;
  setTimeout(function(){output.textContent = '';}, 5000); 
}

function setUp() {
  document.getElementById('clear').addEventListener('click', clear);

  // Save File logic
  var saveFileButton = document.querySelector('#save'); 
  saveFileButton.addEventListener('click', function(e) {
    var fileName = 'd.';
    if(document.getElementById('br_mobile').checked) {
      fileName = 'm.';
    }
    fileName += document.getElementById('file_name').value + '.json';

    saveAs(new Blob([getTraceContent()], {type: 'plain/text'}), fileName);

    /*
    saveAs(new Blob([(new XMLSerializer).serializeToString(document.getElementById('container'))], 
        {type: "application/xhtml+xml;charset=" + document.characterSet}),
        fileName);
    */

    showNotification('File saved.');
  });

  var mob = document.getElementById("br_mobile");
  mob.addEventListener('click', function() {resizeWin(320);});

  var dsk = document.getElementById("br_desktop");
  dsk.addEventListener('click', function() {resizeWin(1024);});
}

function resizeWin(newWidth) {
  chrome.tabs.get(tabId, function(tab) {
    var winProp = {
      width: newWidth,
      focused: true,
      drawAttention: true
    };
    chrome.windows.update(tab.windowId, winProp);
  });
  
}

function clearBrowsingData(timeDuration, callback) {
  var timeToClear = (new Date()).getTime();
  var millisecondsPerWeek = 1000 * 60 * 60 * 24 * 7;
  if(timeDuration == 'week') {
    timeToClear -= millisecondsPerWeek;
  } else {
    timeToClear = 0;
  }

  chrome.browsingData.remove({
    "since": timeToClear
  }, {
    "appcache": true,
    "cache": true,
    "cookies": true,
    "downloads": true,
    "fileSystems": true,
    "formData": true,
    "history": true,
    "indexedDB": true,
    "localStorage": true,
    "pluginData": true,
    "passwords": true,
    "webSQL": true
  }, callback);

  chrome.tabs.update(tabId, {
    "url": "about:blank"
  });
}

function clear() {
  var elem = document.getElementById("container").innerHTML = "";

  clearBrowsingData('week', function() {
    showNotification('Session cleared!');
  });

}

function getTraceContent() {
  var cont = document.getElementById('container');
  var reqs = cont.querySelectorAll("div[class='request'],div[class='event']");
  var jsonData = '[';
  for(var i = 0; i < reqs.length; i++) {
    //jsonData += '\n{\n'+reqs[i].textContent+'},';
    var divData = reqs[i].textContent;
    if(divData.substr(-1) === ",") {
      divData = divData.slice(0,divData.length-1);
    }
    jsonData += '\n{\n'+divData+'\n},';
  }
  if(jsonData.length > 1) { // Remove last ,
    jsonData = jsonData.slice(0,jsonData.length-1);
  }

  return jsonData+'\n]';
}

function formatHeaders(headers) {
  var text = "";
  for (name in headers)
    text += name + ": " + headers[name] + "\n";
  var div = document.createElement("div");
  div.textContent = text;
  return div;
}

function parseURL(url) {
  var result = {};
  var match = url.match(
      /^([^:]+):\/\/([^\/:]*)(?::([\d]+))?(?:(\/[^#]*)(?:#(.*))?)?$/i);
  if (!match)
    return result;
  result.scheme = match[1].toLowerCase();
  result.host = match[2];
  result.port = match[3];
  result.path = match[4] || "/";
  result.fragment = match[5];
  return result;
}