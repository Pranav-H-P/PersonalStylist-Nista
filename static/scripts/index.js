const signUpLink = document.getElementById("signUpLink");
const chatLink = document.getElementById("goToChat");


var userData = localStorage.getItem("user")


if (userData === null){ // check if user has registered

    signUpLink.classList.remove("hide");

}else{

    chatLink.classList.remove("hide");

}

