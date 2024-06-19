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

//all post
window.addEventListener("load", function (){ //
    waitForElm('.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z').then((elm) => {
        console.log("all post ok");
            //for profile
            let res = document.getElementsByClassName("x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z");
            console.log(res.length);
            for (let i = 0; i < res.length; i++){
                    console.log(i);
                    res[i].setAttribute("data-taint","1")
            }
    });
});

//x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r

window.addEventListener("load", function (){ //
    waitForElm('.x1ey2m1c.xds687c.x5yr21d.x10l6tqk.x17qophe.x13vifvy.xh8yej3.xl1xv1r').then((elm) => {
        console.log("all post again!!!!!!!!!!!");
        //for profile

        let res = document.getElementsByClassName("x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z");
        console.log(res.length);
        for (let i = 0; i < res.length; i++){
            console.log(i);
            res[i].setAttribute("data-taint","1")
        }
    });
});


window.addEventListener("load", function (){ // ok
    waitForElm('.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x14z4hjw.x1x48ksl.x579bpy.xjkpybl.x1xlr1w8.xzsf02u.x1yc453h').then((elm) => {
        console.log("head yes");
        //head, name #friends
        document.getElementsByClassName("x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x1x48ksl x579bpy xjkpybl x1xlr1w8 xzsf02u x1yc453h")[0].setAttribute("data-taint","1");
        document.getElementsByClassName("x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xi81zsa x1s688f")[0].setAttribute("data-taint","1");
        console.log('head done')
});
}); // 2


window.addEventListener("load", function (){ // ok
    waitForElm('.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.xamitd3.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn').then((elm) => {
        console.log("bio yes");
            //bio
            let res = document.getElementsByClassName("x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xamitd3 xsyo7zv x16hj40l x10b6aqq x1yrsyyn");
            for (let i = 0; i < res.length; i++){
                res[i].setAttribute("data-taint","1")
                console.log(res[i]);
            }
    console.log('bio done')
});
}); // check done, 8


window.addEventListener("load", function (){ // ok, ajax
    waitForElm('.x78zum5.xdt5ytf.x12upk82').then((elm) => {
        // console.log("#friends yes");
            //#friends
            document.getElementsByClassName("x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x41vudc x1lkfr7t x1lbecb7 xo1l8bm xi81zsa x1yc453h")[0].setAttribute("data-taint","1");
            let res = document.getElementsByClassName("x78zum5 xdt5ytf x1xmf6yo x80cylo");
            for (let i = 0; i < res.length; i++){ // friend name
                res[i].setAttribute("data-taint","1")
            }
});
}); // 1+2, check done

window.addEventListener("load", function (){ // ok, ajax
    waitForElm('.x78zum5.xw3qccf.x3hqpx7').then((elm) => {
        // console.log("events");
            //events
            document.getElementsByClassName("x78zum5 xw3qccf x3hqpx7")[0].setAttribute("data-taint","1");
            document.getElementsByClassName("x78zum5 xw3qccf x3hqpx7")[1].setAttribute("data-taint","1");

});
}); // 2, check done

