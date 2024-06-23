/*

 Test the document.location taint sources, see Table 1 in the paper
 -----------------------------------------------------------------------------------------------------------
 |Category     | Taint Source                                                   | Permission               |
 |DOM location | Href, Protocol, Host, Hostname, Pathname, Search, Origin, Hash | Content script injection |
 -----------------------------------------------------------------------------------------------------------

 (Note that the document.location.toString() method actually invokes .href property, so its return value is also tainted. )
 */

// Test URL = https://www.google.com/search?q=Gatech

let href_value = document.location.href;            // = "https://www.google.com/search?q=Gatech"
let protocol_value = document.location.protocol;    // = "https"
let host_value = document.location.host;            // = "www.google.com"
let hostname_value = document.location.hostname;    // = "www.google.com"
let pathname_value = document.location.pathname;    // = "/search"
let search_value = document.location.search;        // = "?q=Gatech"
let origin_value = document.location.origin;        // = "https://www.google.com"
let tostring_value = document.location.toString();  // = "https://www.google.com/search?q=Gatech"





