/*

 Test the document.location taint sources, see Table 1 in the paper
 -----------------------------------------------------------------------
 |Category     | Taint Source               | Permission               |
 |DOM property | URL, Domain, Title, Cookie | Content script injection |
 -----------------------------------------------------------------------

 */

// Test URL = https://yuanbin.xyz/test (Use web recording)

let password_input = document.getElementById("pass");
let val = password_input.value;             // = "mypasswd"


