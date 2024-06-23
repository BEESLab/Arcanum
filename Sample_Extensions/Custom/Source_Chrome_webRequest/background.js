
/*
    "https://yuanbin.xyz" is our custom test site for testing the taint of "set-cookie"
    and "cookie" values in requestHeaders and responseHeaders.
    Since we don't want to maintain this site forever, we use web recording here.

    Similarly, all web requests when visit another test site https://gatech.edu could change,
    so we use web recording for testing taint of url, ip, and initiator of chrome.webRequest.onCompleted.
 */
chrome.webRequest.onCompleted.addListener(
    function(details) {
        // console.log(details);
        if (details.url == "https://www.gatech.edu/sites/default/files/favicon.ico") {  // Select one web request in the recording for test
            let val_url = details.url;              // = "https://www.gatech.edu/sites/default/files/favicon.ico"
            let val_ip = details.ip;                // As we are using recording, the expected ip is "127.0.0.1"
            let val_initiator = details.initiator;  // = "https://www.gatech.edu"
        }
        if (details.url == "https://yuanbin.xyz/test/") {
            for (var i = 0; i < details.responseHeaders.length; i++){
                if (details.responseHeaders[i].name.toLowerCase() == "set-cookie") {
                    let val_setcookie = details.responseHeaders[i].value; // = "user=QingeXie"
                    break;
                }
            }
        }
    }, {
        urls: [
            "https://yuanbin.xyz/*",
            "https://*.gatech.edu/*",
        ],},
    ["responseHeaders", "extraHeaders"]);


chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        for (var i = 0; i < details.requestHeaders.length; i++){
            if (details.requestHeaders[i].name.toLowerCase() == "cookie") {
                let val_cookie = details.requestHeaders[i].value;  // = "user=QingeXie"
                break;
            }
        }
    },
    {
        urls: [
            "https://yuanbin.xyz/*",
        ],},
    ["requestHeaders","extraHeaders"]);