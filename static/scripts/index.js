const signUpLink = document.getElementById("signUpLink");
const chatLink = document.getElementById("goToChat");
const centerBigText = document.getElementById("contentHeading");
const centerCaption = document.getElementById("captionText");
const contentLinkContainer = document.getElementById("contentLinkContainer");

var userData = localStorage.getItem("user")


if (userData === null){ // check if user has registered

    signUpLink.classList.remove("hide");

}else{

    chatLink.classList.remove("hide");

}

centerBigText.classList.remove("comeFromLeft");

setTimeout( () => {
    centerCaption.classList.remove("comeFromRight");
}, 1200);

setTimeout( () => {
    contentLinkContainer.classList.remove("comeFromBottom");

}, 2500);
