const signUpLink = document.getElementById("signUpLink");
const chatLink = document.getElementById("goToChat");

const centerBigText = document.getElementById("contentHeading");
const centerCaption = document.getElementById("captionText");

const contentLinkContainer = document.getElementById("contentLinkContainer");



let userData = JSON.parse(localStorage.getItem("user")) // check if this exists in localStorage
                                                        // (if user has signed up already)


if (userData === null){ // check if user has registered

    signUpLink.classList.remove("hide");

}else{

    chatLink.classList.remove("hide");

}


setTimeout( () => { // wait for bit for it to load
    centerBigText.classList.remove("comeFromLeft"); // trigger css transition effect
}, 250)


setTimeout( () => {
    centerCaption.classList.remove("comeFromRight");
}, 1200); // trigger css transition effect after delay

setTimeout( () => {
    contentLinkContainer.classList.remove("comeFromBottom");

}, 2500);
