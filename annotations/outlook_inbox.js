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
    waitForElm('.FiPRo').then((elm) => {
        console.log("email list ok");

    let list = document.getElementsByClassName("FiPRo")[0];
    list.setAttribute("data-taint","1");
    console.log(document.getElementsByClassName("EeHm8")[1].innerText);
});
});