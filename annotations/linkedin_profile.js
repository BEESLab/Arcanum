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


//right two
window.addEventListener("load", function (){ //right two
    waitForElm('.pv-text-details__right-panel-item-text.hoverable-link-text.break-words.text-body-small.t-black').then((elm) => {
        console.log("right two");
    //for profile
    let cardview = document.getElementsByClassName("artdeco-card ember-view pv-top-card")[0];
    cardview.setAttribute("data-taint",1);
    console.log(cardview.innerText);
});
}); // 1, check done


//message
window.addEventListener("load", function (){ //right two
    waitForElm('.msg-overlay-list-bubble__conversations-list').then((elm) => {
        console.log("message ok");
    //for profile
    let message = document.getElementsByClassName("msg-overlay-list-bubble__conversations-list")[0];
    message.setAttribute("data-taint",1);
    console.log(message.innerText);
});
}); // 1, check done


window.addEventListener("load", function (){ //right two
    waitForElm('.pvs-header__container').then((elm) => {
        console.log("headers ok");
    //for profile
    let headers = document.getElementsByClassName("pvs-header__container");
    for (let i = 0; i < headers.length; i++) {
        // console.log(i);
        headers[i].setAttribute("data-taint", "1");
        // console.log(headers[i].innerText);
    }
    console.log("headers count=" + headers.length);
});
}); // 19, check done


window.addEventListener("load", function (){ //right two
    waitForElm(".artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column.pvs-list--ignore-first-item-top-padding").then((elm) => {
        console.log("list item ok");
    //for profile
    let listitem = document.getElementsByClassName("artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column pvs-list--ignore-first-item-top-padding");
    for (let i = 0; i < listitem.length; i++) {
        // console.log(i);
        listitem[i].setAttribute("data-taint", "1");
        // console.log(listitem[i].innerText);
    }
    console.log("listitem count=" + listitem.length);
});
}); // 25 check done


window.addEventListener("load", function (){ //right two
    waitForElm(".pv-shared-text-with-see-more.full-width.t-14.t-normal.t-black.display-flex.align-items-center").then((elm) => {
        console.log("see more ok");
    //for profile
    let seemore = document.getElementsByClassName("pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center");
    for (let i = 0; i < seemore.length; i++) {
        // console.log(i);
        seemore[i].setAttribute("data-taint", "1");
        // console.log(seemore[i].innerText);
    }
    console.log("see more count=" + seemore.length);
});
}); // 8 check done


window.addEventListener("load", function (){ //right two
    waitForElm(".pv-profile-info-section.artdeco-card.p4.mb2").then((elm) => {
        console.log("language_card ok");
    //for profile
    let language_card = document.getElementsByClassName("pv-profile-info-section artdeco-card p4 mb2")[0];
    language_card.setAttribute("data-taint","1");
    console.log(language_card.innerText);
});
}); // 1 check done



window.addEventListener("load", function (){ //right two
    waitForElm(".profile-creator-shared-feed-update__mini-container").then((elm) => {
        console.log("reply ok");
        let reply = document.getElementsByClassName("profile-creator-shared-feed-update__mini-container");
    for (let i = 0; i < reply.length; i++) {
        console.log(i);
        reply[i].setAttribute("data-taint", "1");
        console.log(reply[i].innerText);
    }
});
}); // 2 check done


window.addEventListener("load", function (){ //right two
    waitForElm(".artdeco-entity-lockup__content.ember-view.overflow-hidden.ml1.align-self-flex-start").then((elm) => {
        console.log("bar ok");
        let bar = document.getElementsByClassName("artdeco-entity-lockup__content ember-view overflow-hidden ml1 align-self-flex-start")[0];
        bar.setAttribute("data-taint", "1");
        console.log(bar.innerText);
});
}); // 1 check done, empty


window.addEventListener("load", function (){ //right two
    waitForElm(".SIZE_300_250.type.da.da--sl.exp.var-da--f300x250.exp-ac--toggle-click").then((elm) => {
        console.log("days ok");
    let days = document.getElementsByClassName("SIZE_300_250 type da da--sl exp var-da--f300x250 exp-ac--toggle-click ")[0];
    days.setAttribute("data-taint", "1");
    console.log(days.innerText);
});
}); // 1 check done, empty

window.addEventListener("load", function (){ //right two
    waitForElm("#ads-container").then((elm) => {
        console.log("promo ok");
    let promo = document.getElementById("ads-container");
    promo.setAttribute("data-taint", "1");
    console.log(promo.innerText);
});
}); // 1 check done, empty

