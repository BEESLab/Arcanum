/*

 Test the document.location taint sources, see Table 1 in the paper
 ---------------------------------------------------------------------------
 |Category     | Taint Source                      | Permission            |
 |Chrome.cookies API | Domain, Path, Name, Value   |  "cookies" permission |
 ---------------------------------------------------------------------------

 We instrumented two method call: chrome.cookies.get() and chrome.cookies.getAll()
 */

chrome.cookies.set({
   "name": "foo",
   "url": "https://www.cookiesget_example.com",
   "value": "foo_val",
   "path": "/"
}, function (cookie) {
   // console.log(JSON.stringify(cookie));
   chrome.cookies.get({"url":"https://www.cookiesget_example.com/","name":"foo"},function (cookie){
      // console.log(cookie);
      let value_cookie_domain = cookie.domain;  // = "www.cookiesget_example.com"
      let value_cookie_name = cookie.name;      // = "foo"
      let value_cookie_value = cookie.value;    // = "foo_val"
      let value_cookie_path = cookie.path;      // = "/"
   });
});

chrome.cookies.set({
   "name": "bar",
   "url": "https://www.cookiesgetall_example.com/",
   "value": "bar_val",
   "path": "/"
}, function (cookie) {
   // console.log(JSON.stringify(cookie));
   chrome.cookies.getAll({"domain":"cookiesgetall_example.com"},function (cookies){
      // console.log(cookies[0]);
      let value_cookie_domain = cookies[0].domain;  // = "www.cookiesgetall_example.com"
      let value_cookie_name = cookies[0].name;      // = "bar"
      let value_cookie_value = cookies[0].value;    // = "bar_val"
      let value_cookie_path = cookies[0].path;      // = "/"
   });
});
