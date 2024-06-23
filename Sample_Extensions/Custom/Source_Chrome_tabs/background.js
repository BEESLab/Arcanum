// var activeTabId;
//
// chrome.tabs.onActivated.addListener(function(activeInfo) {
//     activeTabId = activeInfo.tabId;
// });
//
// function getActiveTab(callback) {
//     // chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
//     //     var tab = tabs[0];
//     //
//     //     if (tab) {
//     //         callback(tab);
//     //     } else {
//     //         chrome.tabs.get(activeTabId, function (tab) {
//     //             if (tab) {
//     //                 callback(tab);
//     //             } else {
//     //                 console.log('No active tab identified.');
//     //             }
//     //         });
//     //
//     //     }
//     // });
// }
//
// chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//     var currTab = tabs[0];
//     console.log(currTab);
//     if (currTab) { // Sanity check
//         /* do stuff */
//     }
// });



// chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab)=>{
//     // console.log(changeInfo);
//     if (changeInfo.status == "loading") {
//         // console.log(tabId);
//         console.log(tab);
//         // chrome.tabs.query({
//         //     "windowId": tab.windowId
//         // }, (tabs) => {
//         //     if (tabs.length > 0) {
//         //         console.log(tabs[0].url);
//         //         console.log(tabs[0].title);
//         //     }
//         // })
//     }
// });

chrome.tabs.onCreated.addListener(async tab => {
    // console.log(tab);
    let val_pendingUrl = tab.pendingUrl;
    let val_url = tab.url;
    let val_title = tab.title;
    console.log(val_pendingUrl);
    console.log(val_url);
    console.log(val_title);
    // Set URL
    let toUpdate = {
        url: "https://gatech.edu"
    };
    chrome.tabs.update(tab.id, toUpdate, function(tab_updated){
        console.log(tab_updated);
        console.log(tab_updated.pendingUrl); // https://github.com
        console.log(tab_updated.url);
        console.log(tab_updated.title);
    });

    // Update the tab (redirect to URL)
    // tab_updated = await chrome.tabs.update(tab.id, toUpdate);
    // console.log(tab_updated);
    // console.log(tab_updated.pendingUrl); // https://github.com
    // console.log(tab_updated.url);
    // console.log(tab_updated.title);

});