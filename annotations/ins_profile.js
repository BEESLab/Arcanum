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
window.addEventListener("load", function (){ //
    waitForElm('.xl565be.x1m39q7l.x1uw6ca5.x2pgyrj').then((elm) => {
        console.log("profile head ok");

    let head = document.getElementsByClassName("x1qjc9v5 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x5n08af x78zum5 xdt5ytf xs83m0k xk390pu xdj266r x11i5rnm xat24cr x1mh8g0r xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xg1prrt x1quol0o x139hhg0 x1qgnrqa")[0];
    head.setAttribute("data-taint","1");
    console.log(head.innerText);
});
});

window.addEventListener("load", function (){ //
    waitForElm('._aagu').then((elm) => {
        console.log("post list ok");

    document.getElementsByClassName("_aagu")[0].setAttribute("data-taint","1");
    document.getElementsByClassName("_aagu")[1].setAttribute("data-taint","1");

});
});