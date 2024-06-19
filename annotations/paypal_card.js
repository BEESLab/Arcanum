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
    waitForElm(".fiDetailsSection").then((elm) => {
        // alert("right list ok");
        console.log("right list ok");
        let right_list = document.getElementsByClassName("fiDetailsSection");
        for (let i = 0; i < right_list.length; i++){
            right_list[i].setAttribute("data-taint","1");
            console.log(i);
            console.log(right_list[i].innerText);
            // alert(right_list[i].innerText);
        }

    });
});

window.addEventListener("load", function (){ //
    waitForElm(".fiListItem-col.table-col-xs").then((elm) => {
        // alert("left list ok");
        console.log("left list ok");
        let left_list = document.getElementsByClassName("fiListItem-col table-col-xs");
        for (let i = 0; i < left_list.length; i++){
            left_list[i].setAttribute("data-taint","1");
            console.log(i);
            console.log(left_list[i].innerText);
            // alert(left_list[i].innerText);
        }

    });
});

window.addEventListener("load", function (){ //
    waitForElm(".cardImage-container.cardImage-container_large").then((elm) => {
        // alert("card image ok");
        console.log("card image ok");
        let card_img = document.getElementsByClassName("cardImage-container cardImage-container_large")[0];
        card_img.setAttribute("data-taint","1");
        // alert(card_img.innerHTML);

    });
});

window.addEventListener("load", function (){ //
    waitForElm(".ppvx_text--body.fiDetails-instrumentName").then((elm) => {
        // alert("instrumentName ok");
        console.log("instrumentName ok");
        let instrumentName = document.getElementsByClassName("ppvx_text--body fiDetails-instrumentName")[0];
        instrumentName.setAttribute("data-taint","1");
        // alert(instrumentName.innerHTML);

    });
});

window.addEventListener("load", function (){ //
    waitForElm(".editNickName").then((elm) => {
        // alert("editNickName ok");
        console.log("editNickName ok");
        let editNickName = document.getElementsByClassName("editNickName")[0];
        editNickName.setAttribute("data-taint","1");
        // alert(editNickName.innerHTML);

    });
});

