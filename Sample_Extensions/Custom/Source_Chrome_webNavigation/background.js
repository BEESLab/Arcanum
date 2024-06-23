
let test_URL1 = "https://www.google.com/";
let test_URL2 = "https://www.gatech.edu/";

chrome.webNavigation.onCompleted.addListener(function(e){
   let url_val = e.url;
   chrome.webNavigation.getFrame(
       {tabId: e.tabId, processId: e.processId, frameId: e.frameId},
       function(details){
          if (details.url == test_URL1) {
              let fram_url_val = details.url;
          }
       }
   );

    chrome.webNavigation.getAllFrames(
        {tabId: e.tabId},
        function(details){
            for (var i = 0; i< details.length; i++){
                if (details[i].url == test_URL2) {
                    let frame_url_val = details.url;
                    break;
                }
            }
        }
    );
});