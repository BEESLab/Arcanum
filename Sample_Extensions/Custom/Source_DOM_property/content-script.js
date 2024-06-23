/*

 Test the document.location taint sources, see Table 1 in the paper
 -----------------------------------------------------------------------
 |Category     | Taint Source               | Permission               |
 |DOM property | URL, Domain, Title, Cookie | Content script injection |
 -----------------------------------------------------------------------

 */

// Test URL = https://www.google.com/search?q=Gatech

let URL_value = document.URL;       // = "https://www.google.com/search?q=Gatech"
let domain_value = document.domain; // = "www.google.com"
let title_value = document.title;   // = "Gatech - Google Search"

// Since cookie could be inconsistent, we set a fixed key-value pair before testing.
document.cookie = "username=Qinge Xie;"
let cookie_value = document.cookie; // = "....username=Qinge Xie;....."


