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

var callback = function(mutationsList) {
    for(var mutation of mutationsList) {
        console.log("mutation found!!!");
        document.getElementsByClassName('l6')[0].setAttribute("data-taint","1");
        document.getElementsByClassName("l2 pfiaof")[0].setAttribute("data-taint","1");
    }
};

var callbackmain = function(mutationsList) {
    for(var mutation of mutationsList) {
        console.log("UI mutation found!!!");
        document.getElementsByClassName("UI")[0].setAttribute("data-taint","1");
    }
};

window.addEventListener("load", function (){ //
    waitForElm(".zA.yO").then((elm) => {
        console.log("email list ok");

    let email_list = document.getElementsByClassName("UI")[0];
    email_list.setAttribute("data-taint","1");
    // console.log(email_list.innerText);
    var observer = new MutationObserver(callbackmain);
    observer.observe(email_list, {
            childList: true,
            subtree: true
    });
});
});

window.addEventListener("load", function (){ //
    waitForElm(".gb_d.gb_Aa.gb_D").then((elm) => {
        console.log("account ok");

        let account = document.getElementsByClassName("gb_d gb_Aa gb_D")[0];
        account.setAttribute("data-taint","1");
        console.log(account.innerHTML);
    });
});

window.addEventListener("load", function (){ //
    waitForElm(".l6").then((elm) => {
        console.log("end ok");

        let end = document.getElementsByClassName("l2 pfiaof")[0];
        end.setAttribute("data-taint","1");
        console.log(end.innerText);

        let lastactive = document.getElementsByClassName("l6")[0];
        lastactive.setAttribute("data-taint","1");
        console.log(lastactive.outerHTML);

        console.log(end);
        var observer = new MutationObserver(callback);
        observer.observe(end, {
            childList: true,
            subtree: true
        });

    });
});

window.addEventListener("load", function (){ //
    waitForElm(".aKs").then((elm) => {
        console.log("promotion ok");

        let bar = document.getElementsByClassName("aAA J-KU-Jg J-KU-Jg-K9")[0];
        bar.setAttribute("data-taint","1");
        console.log(bar.innerText);



    });
});
