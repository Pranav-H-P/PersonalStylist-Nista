const textBox = document.getElementById("textInput");
const sendButton = document.getElementById("sendButton");

const logoText = document.getElementById('logoText');
const content = document.getElementById("mainContent");


setTimeout( () => { // wait for a bit for it to load
    content.classList.remove('comeFromBottom'); // trigger css transition effect
    
}, 250);


logoText.addEventListener('click', () => {
    window.location.href = "/";
});

textBox.addEventListener('keydown', e => {
    
    const userAgent = navigator.userAgent;
    if (!userAgent.match(/Mobile|Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i)){ // exclude mobile users from this

        if (e.key === 'Enter' && !e.shiftKey ) { // Enter key sends message on PC, shift+enter creates new line
        
        e.preventDefault(); // Prevent the default behavior of the Enter key (new line)
        
        sendButton.click();
        }
    }
});
  
sendButton.addEventListener('click', () => {

    console.log("sending to server");

});
