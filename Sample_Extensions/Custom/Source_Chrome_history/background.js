/*

 Test the document.location taint sources, see Table 1 in the paper
 ------------------------------------------------------------
 |Category     | Taint Source       | Permission            |
 |Chrome.history API | URL, Title   |  "history" permission |
 ------------------------------------------------------------

 We instrumented two method call: chrome.history.getVisits() and chrome.history.search()
 and one event call: chrome.history.onVisited().
 */


// Retrieves information about visits to a URL.
// Note: Testing this in unmodified Chrome may trigger an error as we've modified UrlDetails to also include the url field.
chrome.history.getVisits({url: "https://www.google.com/search?q=Gatech"}, function (urlDetails) {
    // console.log(urlDetails);
    if (urlDetails.length >= 1) {
        let url_value = urlDetails[0].url;
    }
});

chrome.history.search({text:"scp.cc.gatech.edu"}, function (historyItems) {
    // console.log(historyItems);
    if (historyItems.length >= 1){
        let url_value = historyItems[0].url;
        let title_value = historyItems[0].title;
    }
});

// Fired when a URL is visited, providing the HistoryItem data for that URL
// Invoke EventEmitter::Fire()
chrome.history.onVisited.addListener(function(historyItem) {
    // console.log(historyItem.url);
    // console.log(historyItem.title);
    let url_value = historyItem.url;
    let title_value = historyItem.title;

});


