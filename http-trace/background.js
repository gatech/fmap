// HTTP Trace Capture
// Author: Shauvik Roy Choudhary (shauvik@gatech.edu)
// Some code re-used from the Open source Live Headers extension sample
// License: BSD style 
// Copyright (c) 2012 The Chromium Authors. All rights reserved.


chrome.browserAction.onClicked.addListener(function() {
  chrome.windows.getCurrent(function(win) {
    chrome.tabs.getSelected(win.id, actionClicked);
  });
});

var version = "1.0";

function actionClicked(tab) {
  chrome.tabs.create({"url":"about:blank"}, function(newTab) {
    chrome.debugger.attach({tabId:newTab.id}, version, onAttach.bind(null, newTab.id));
    chrome.debugger.onDetach.addListener(function(debugee, reason){
      alert("ALERT: HTTP Trace Capture debugger is detached from :"+JSON.stringify(debugee)+", Reason:"+reason
        +"\n\n Did you close it by mistake? Please re-open the debugger by clicking on the extension button.");
    });
  });
}

function onAttach(tabId) {
  if (chrome.runtime.lastError) {
    alert(chrome.runtime.lastError.message);
    return;
  }

  chrome.windows.create(
      {url: "headers.html?" + tabId, type: "popup", width: 725});
}
