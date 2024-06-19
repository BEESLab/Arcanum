function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
        return resolve(document.querySelector(selector));
    }
    const observer = new MutationObserver(mutations => {
        if (document.querySelector(selector)) {
        resolve(document.querySelector(selector));
        observer.disconnect();
    }
});
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
}

//deliver
window.addEventListener("load", function (){ //
    waitForElm('#glow-ingress-block').then((elm) => {
        console.log("deliver ok");
    //for profile
    let addr = document.getElementById("glow-ingress-block");
    addr.setAttribute("data-taint",1);
});
}); // 1

window.addEventListener("load", function (){ //
    waitForElm('#nav-link-accountList-nav-line-1').then((elm) => {
        console.log("name ok");
    //for profile
    let name = document.getElementById("nav-link-accountList-nav-line-1");
    console.log(name.innerText);
    name.setAttribute("data-taint",1);
});
}); // 1

window.addEventListener("load", function (){ //
    waitForElm('#address-ui-widgets-FullName').then((elm) => {
        console.log("address ok");
    //for profile
    let addr_list = document.getElementsByClassName("a-box-inner a-padding-none");
    for (let i = 0; i < addr_list.length; i++){
        console.log(i);
        addr_list[i].setAttribute("data-taint","1")
        // console.log(addr_list[i].innerText);
    }
});
}); // 3

window.addEventListener("load", function (){ //
    waitForElm('#icp-nav-flyout').then((elm) => {
        console.log("language ok");

    let language = document.getElementById("icp-nav-flyout");
    language.setAttribute("data-taint",1);
    console.log(language.innerText);

});
});

