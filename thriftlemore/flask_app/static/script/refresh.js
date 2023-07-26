function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}

function refresh() {
    document.getElementById('logo').className = 'logo'
    console.log('it does')
}

function reset() {
    document.getElementById('logo').className = 'logo bounce';
    console.log('its off now')
}

// var delayInMilliseconds = 1000; //1 second
// setTimeout(refresh() {
//   //your code to be executed after 1 second
// }, delayInMilliseconds);

// function refresh_header() {
//     let reroll = "display-1 is-italic d-flex justify-content-center logo bounce";
//     document.getElementById('title').className = reroll;

//         if (reroll == "display-1 is-italic d-flex justify-content-center logo bounce") {
//             reroll = "display-1 is-italic d-flex justify-content-center";
//         }
//         else {
//             reroll = "display-1 is-italic d-flex justify-content-center logo bounce";
//         }
//     console.log(reroll)
//     document.getElementById('title').className = reroll;
// }